from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import openai
from collections import defaultdict
from threading import Lock

class BaseModel(ABC):
    def __init__(self, model_name: str, model_type: str, api_base: str, api_key: str,
                 pricing: Optional[Dict[str, Any]] = None):
        self.model_name = model_name
        self.model_type = model_type
        self.api_base = api_base
        self.api_key = api_key
        self.pricing = pricing or {}
        unit = (self.pricing.get("unit") or "1k").lower()
        self._pricing_divisor = 1000 if unit == "1k" else 1_000_000
        
        self.token_usage={
            "total":defaultdict(float),
            "last_call":defaultdict(float)
        }
        self._usage_lock = Lock()
        
        if "azure" in api_base:
            api_version = "2024-08-01-preview"

            self.client = openai.AzureOpenAI(
                api_key=api_key, azure_endpoint=api_base, api_version=api_version
            )
        else:
            self.client = openai.OpenAI(api_key=api_key, base_url=api_base)
        
    def update_token_usage(self, response: openai.ChatCompletion):
        usage = getattr(response, "usage", None)
        if usage is None:
            return {}

        prompt_tokens = getattr(usage, "prompt_tokens", 0) or 0
        completion_tokens = getattr(usage, "completion_tokens", 0) or 0
        completion_details = getattr(usage, "completion_tokens_details", None)
        reasoning_tokens = (
            getattr(completion_details, "reasoning_tokens", 0)
            if completion_details
            else getattr(usage, "reasoning_tokens", 0)
        )
        reasoning_tokens = reasoning_tokens or 0
        total_tokens = getattr(usage, "total_tokens", prompt_tokens + completion_tokens) or (
            prompt_tokens + completion_tokens
        )

        api_cost = None

        if hasattr(usage, "cost"):
            api_cost = getattr(usage, "cost", None)

        if api_cost is None and hasattr(response, "cost"):
            api_cost = getattr(response, "cost", None)

        if api_cost is None and hasattr(usage, "model_extra"):
            extra = getattr(usage, "model_extra", {}) or {}
            api_cost = extra.get("cost") or extra.get("total_cost")

        if api_cost is None and hasattr(response, "model_extra"):
            extra = getattr(response, "model_extra", {}) or {}
            api_cost = extra.get("cost") or extra.get("total_cost")

        if api_cost is not None:
            call_cost = float(api_cost)
            if total_tokens > 0:
                prompt_ratio = prompt_tokens / total_tokens
                prompt_cost = call_cost * prompt_ratio
                completion_cost = call_cost * (1 - prompt_ratio)
            else:
                prompt_cost = 0.0
                completion_cost = call_cost
        else:
            prompt_cost = self.pricing.get("prompt", 0.0) * prompt_tokens / self._pricing_divisor
            completion_cost = self.pricing.get("completion", 0.0) * completion_tokens / self._pricing_divisor
            call_cost = prompt_cost + completion_cost

        with self._usage_lock:
            self.token_usage["total"]["prompt_tokens"] += prompt_tokens
            self.token_usage["total"]["completion_tokens"] += completion_tokens
            self.token_usage["total"]["total_tokens"] += total_tokens
            self.token_usage["total"]["reasoning_tokens"] += reasoning_tokens
            self.token_usage["last_call"]["prompt_tokens"] = prompt_tokens
            self.token_usage["last_call"]["completion_tokens"] = completion_tokens
            self.token_usage["last_call"]["total_tokens"] = total_tokens
            self.token_usage["last_call"]["reasoning_tokens"] = reasoning_tokens

            self.token_usage["total"]["prompt_cost"] += prompt_cost
            self.token_usage["total"]["completion_cost"] += completion_cost
            self.token_usage["total"]["cost"] += call_cost
            self.token_usage["last_call"]["prompt_cost"] = prompt_cost
            self.token_usage["last_call"]["completion_cost"] = completion_cost
            self.token_usage["last_call"]["cost"] = call_cost

        return {
            "prompt_tokens": int(prompt_tokens),
            "completion_tokens": int(completion_tokens),
            "reasoning_tokens": int(reasoning_tokens),
            "total_tokens": int(total_tokens),
            "prompt_cost": float(prompt_cost),
            "completion_cost": float(completion_cost),
            "cost": float(call_cost),
            "cost_from_api": api_cost is not None,
        }
        
    def get_token_usage(self):
        return self.token_usage
    @abstractmethod
    def generate_response(self, conversation_history: List[Dict[str, Any]], **kwargs) -> str:
        pass

class AssistantModel(BaseModel):
    def __init__(self, model_name: str, api_base: str, api_key: str, system_prompt: Optional[str] = None,
                 pricing: Optional[Dict[str, float]] = None, provider: Optional[str] = None,
                 reasoning_effort: Optional[str] = None):
        super().__init__(model_name, "assistant", api_base, api_key, pricing=pricing)
        self.system_prompt = system_prompt
        self.provider = provider
        self.reasoning_effort = reasoning_effort

    def generate_response(self, conversation_history: List[Dict[str, Any]], **kwargs):        
        if self.system_prompt:
            messages=[
                {"role": "system", "content": self.system_prompt},
                *conversation_history
            ]
        else:
            messages=conversation_history
            
        kargs={
            "model":self.model_name,
            "messages":messages,
        }
        
        if "gpt-5" in self.model_name:
            kargs["max_completion_tokens"]=8_000
        else:
            kargs["max_tokens"]=8_000

        if self.reasoning_effort:
            extra = kargs.get("extra_body", {})
            extra["reasoning_effort"] = self.reasoning_effort
            kargs["extra_body"] = extra

        if self.provider:
            kargs["extra_body"] = {
                "provider": {
                    "order": [self.provider],
                    "allow_fallbacks": False
                }
            }

        response=self.client.chat.completions.create(
            **kargs
        )        
        call_usage = self.update_token_usage(response)
        return response.choices[0].message.content, call_usage
