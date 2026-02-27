
"""Binary of evaluating instruction following. See README.md."""

import collections
import dataclasses
import json
import logging
from typing import Any, Dict, Optional, Sequence, Union

import openai

import instructions_registry
import instructions_util


@dataclasses.dataclass
class InputExample:
  key: int
  instruction_id_list: list[str]
  prompt: str
  kwargs: list[Dict[str, Optional[Union[str, int]]]]


@dataclasses.dataclass
class OutputExample:
  instruction_id_list: list[str]
  prompt: str
  response: str
  follow_all_instructions: bool
  follow_instruction_list: list[bool]


@dataclasses.dataclass
class CoherenceResult:
  score: float
  source: str
  explanation: str


@dataclasses.dataclass
class ScoredOutputExample:
  key: int
  instruction_id_list: list[str]
  prompt: str
  response: str
  follow_all_instructions: bool
  follow_instruction_list: list[bool]
  instruction_score: float
  coherence_score: float
  final_score: float
  coherence_source: str
  coherence_explanation: str
  unique_word_count: int


@dataclasses.dataclass
class UsageTracker:
  """Tracks token, cost, and response length statistics for an LLM."""

  model_name: Optional[str] = None
  pricing: Optional[Dict[str, Any]] = None
  prompt_tokens: int = 0
  completion_tokens: int = 0
  reasoning_tokens: int = 0
  total_tokens: int = 0
  prompt_cost: float = 0.0
  completion_cost: float = 0.0
  total_cost: float = 0.0
  response_chars: int = 0
  response_count: int = 0

  def __post_init__(self):
    pricing = self.pricing or {}
    unit = (pricing.get("unit") or "1k").lower()
    self._divisor = 1000 if unit == "1k" else 1_000_000
    self._prompt_price = pricing.get("prompt", 0.0)
    self._completion_price = pricing.get("completion", 0.0)

  def log_completion(
      self,
      prompt_tokens: int,
      completion_tokens: int,
      reasoning_tokens: int = 0,
      response_text: str = "",
  ):
    prompt_tokens = prompt_tokens or 0
    completion_tokens = completion_tokens or 0
    reasoning_tokens = reasoning_tokens or 0
    reasoning_tokens = min(reasoning_tokens, completion_tokens)
    total_tokens = prompt_tokens + completion_tokens

    self.prompt_tokens += prompt_tokens
    self.completion_tokens += completion_tokens
    self.reasoning_tokens += reasoning_tokens
    self.total_tokens += total_tokens

    prompt_cost = (prompt_tokens * self._prompt_price) / self._divisor
    completion_cost = (completion_tokens * self._completion_price) / self._divisor
    self.prompt_cost += prompt_cost
    self.completion_cost += completion_cost
    self.total_cost += prompt_cost + completion_cost

    self.response_chars += len(response_text or "")
    self.response_count += 1

  def as_dict(self):
    avg_chars = (
        self.response_chars / self.response_count if self.response_count else 0.0
    )
    avg_prompt_tokens = (
        self.prompt_tokens / self.response_count if self.response_count else 0.0
    )
    avg_completion_tokens = (
        self.completion_tokens / self.response_count
        if self.response_count
        else 0.0
    )
    avg_reasoning_tokens = (
        self.reasoning_tokens / self.response_count if self.response_count else 0.0
    )
    return {
        "model_name": self.model_name,
        "prompt_tokens": self.prompt_tokens,
        "completion_tokens": self.completion_tokens,
        "reasoning_tokens": self.reasoning_tokens,
        "total_tokens": self.total_tokens,
        "prompt_cost": self.prompt_cost,
        "completion_cost": self.completion_cost,
        "total_cost": self.total_cost,
        "response_count": self.response_count,
        "avg_response_chars": avg_chars,
        "avg_prompt_tokens": avg_prompt_tokens,
        "avg_completion_tokens": avg_completion_tokens,
        "avg_reasoning_tokens": avg_reasoning_tokens,
    }


def read_prompt_list(input_jsonl_filename):
  """Read inputs from jsonl."""
  inputs = []
  with open(input_jsonl_filename, "r") as f:
    for l in f:
      example = json.loads(l)
      inputs.append(
          InputExample(key=int(example["key"]),
                       instruction_id_list=example["instruction_id_list"],
                       prompt=example["prompt"],
                       kwargs=example["kwargs"]))
  return inputs


def write_outputs(output_jsonl_filename, outputs):
  """Writes outputs to jsonl."""
  assert outputs
  with open(output_jsonl_filename, "w") as f:
    for o in outputs:
      f.write(
          json.dumps(
              {
                  attr_name: o.__getattribute__(attr_name)
                  for attr_name in [
                      name for name in dir(o) if not name.startswith("_")
                  ]
              }
          )
      )
      f.write("\n")


def test_instruction_following_strict(
    inp,
    prompt_to_response,
):
  """Tests response to see if instrutions are followed."""
  response = prompt_to_response[inp.prompt]
  instruction_list = inp.instruction_id_list
  is_following_list = []

  for index, instruction_id in enumerate(instruction_list):
    instruction_cls = instructions_registry.INSTRUCTION_DICT[instruction_id]
    instruction = instruction_cls(instruction_id)
    inp.kwargs[index] = {key: value for key, value in inp.kwargs[index].items() if value is not None}
    instruction.build_description(**inp.kwargs[index])
    args = instruction.get_instruction_args()
    if args and "prompt" in args:
      instruction.build_description(prompt=inp.prompt)

    if response.strip() and instruction.check_following(response):
      is_following_list.append(True)
    else:
      is_following_list.append(False)

  return OutputExample(
      instruction_id_list=inp.instruction_id_list,
      prompt=inp.prompt,
      response=response,
      follow_all_instructions=all(is_following_list),
      follow_instruction_list=is_following_list,
  )


def test_instruction_following_loose(
    inp,
    prompt_to_response,
):
  """Tests response for an upper bound for following instructions."""
  response = prompt_to_response[inp.prompt]
  r = response.split("\n")
  response_remove_first = "\n".join(r[1:]).strip()
  response_remove_last = "\n".join(r[:-1]).strip()
  response_remove_both = "\n".join(r[1:-1]).strip()
  revised_response = response.replace("*", "")
  revised_response_remove_first = response_remove_first.replace("*", "")
  revised_response_remove_last = response_remove_last.replace("*", "")
  revised_response_remove_both = response_remove_both.replace("*", "")
  all_responses = [
      response,
      revised_response,
      response_remove_first,
      response_remove_last,
      response_remove_both,
      revised_response_remove_first,
      revised_response_remove_last,
      revised_response_remove_both,
  ]
  instruction_list = inp.instruction_id_list
  is_following_list = []

  for index, instruction_id in enumerate(instruction_list):
    instruction_cls = instructions_registry.INSTRUCTION_DICT[instruction_id]
    instruction = instruction_cls(instruction_id)
    inp.kwargs[index] = {key: value for key, value in inp.kwargs[index].items() if value is not None}
    instruction.build_description(**inp.kwargs[index])
    args = instruction.get_instruction_args()
    if args and "prompt" in args:
      instruction.build_description(prompt=inp.prompt)

    is_following = False
    for r in all_responses:
      if r.strip() and instruction.check_following(r):
        is_following = True
        break

    is_following_list.append(is_following)

  return OutputExample(
      instruction_id_list=inp.instruction_id_list,
      prompt=inp.prompt,
      response=response,
      follow_all_instructions=all(is_following_list),
      follow_instruction_list=is_following_list,
  )


def read_prompt_to_response_dict(input_jsonl_filename):
  """Creates dictionary matching prompt and response."""
  return_dict = {}
  with open(input_jsonl_filename, "r") as f:
    for l in f:
      example = json.loads(l)
      return_dict[example["prompt"]] = example["response"]
  return return_dict


def print_report(outputs):
  """Prints a report on accuracy scores."""

  prompt_total = 0
  prompt_correct = 0
  instruction_total = 0
  instruction_correct = 0

  tier0_total = collections.defaultdict(int)
  tier0_correct = collections.defaultdict(int)

  tier1_total = collections.defaultdict(int)
  tier1_correct = collections.defaultdict(int)

  for example in outputs:
    follow_instruction_list = example.follow_instruction_list
    instruction_id_list = example.instruction_id_list

    prompt_total += 1
    if all(follow_instruction_list):
      prompt_correct += 1

    instruction_total += len(instruction_id_list)
    instruction_correct += sum(follow_instruction_list)

    for instruction_id, followed_or_not in zip(
        instruction_id_list, follow_instruction_list
    ):
      instruction_id = instruction_id.split(":")[0]
      tier0_total[instruction_id] += 1
      if followed_or_not:
        tier0_correct[instruction_id] += 1

    for instruction_id, followed_or_not in zip(
        instruction_id_list, follow_instruction_list
    ):
      tier1_total[instruction_id] += 1
      if followed_or_not:
        tier1_correct[instruction_id] += 1

  print(f"prompt-level: {prompt_correct / prompt_total}")
  print(f"instruction-level: {instruction_correct / instruction_total}")
  print()
  for instruction_id in sorted(tier0_total.keys()):
    accuracy = tier0_correct[instruction_id] / tier0_total[instruction_id]
    print(f"{instruction_id} {accuracy}")
  print()
  for instruction_id in sorted(tier1_total.keys()):
    accuracy = tier1_correct[instruction_id] / tier1_total[instruction_id]
    print(f"{instruction_id} {accuracy}")


def load_book_context(book_context_path: str):
  """Loads book context snippets to ground the coherence evaluation."""
  try:
    with open(book_context_path, "r") as f:
      return json.load(f)
  except FileNotFoundError:
    logging.warning(
        "Book context file not found at %s. Coherence eval will lack grounding.",
        book_context_path,
    )
    return []


def _select_book_context(prompt: str, book_context, max_items: int = 3):
  """Pick relevant book snippets based on the prompt text."""
  if not book_context:
    return []
  prompt_lower = prompt.lower()
  selected = []
  for entry in book_context:
    names = [entry.get("title", "").lower()] + entry.get("aliases", [])
    if any(name in prompt_lower for name in names if name):
      selected.append(entry)
  if not selected:
    selected = book_context[:max_items]
  return selected[:max_items]


def _build_coherence_prompt(prompt: str, response: str, context_snippets):
  """Creates a compact prompt for the LLM scorer."""
  context_json = json.dumps(context_snippets, ensure_ascii=False)
  return (
      "Avalie a coerência e clareza do texto de resposta em português brasileiro. "
      "Use apenas o contexto fornecido sobre as obras, sem depender de conhecimento externo. "
      "Retorne um JSON com os campos 'coherence_score' (float entre 0 e 1) "
      "e 'justification' (frase curta). "
      f"\n\nPrompt original:\n{prompt}"
      f"\n\nResposta do modelo:\n{response}"
      f"\n\nContexto das obras:\n{context_json}"
  )


def build_openai_client(api_base: Optional[str] = None,
                        api_key: Optional[str] = None,
                        api_version: Optional[str] = None):
  """Creates an OpenAI-compatible client with optional base/key/version."""
  try:
    if api_base and "azure" in (api_base or ""):
      return openai.AzureOpenAI(
          api_key=api_key,
          azure_endpoint=api_base,
          api_version=api_version or "2024-08-01-preview",
      )
    return openai.OpenAI(api_key=api_key, base_url=api_base)
  except Exception as e:  # pylint: disable=broad-except
    logging.warning("Failed to instantiate OpenAI client: %s", e)
    return None


def _llm_coherence_score(
    prompt: str,
    response: str,
    context_snippets,
    llm_client: Any,
    llm_model: Optional[str],
    temperature: float = 0.0,
    usage_tracker: Optional[UsageTracker] = None,
) -> Optional[CoherenceResult]:
  """Calls an LLM to score coherence; returns None if unavailable."""
  if not llm_client or not llm_model:
    return None

  try:
    completion = llm_client.chat.completions.create(
        model=llm_model,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um avaliador de textos. "
                    "Dê notas de coerência/clareza entre 0 e 1 com base no contexto fornecido. "
                    "Responda apenas em JSON válido."
                ),
            },
            {
                "role": "user",
                "content": _build_coherence_prompt(prompt, response, context_snippets),
            },
        ],
        max_tokens=120,
        response_format={"type": "json_object"},
    )
    content = completion.choices[0].message.content
    if usage_tracker and getattr(completion, "usage", None):
      completion_details = getattr(completion.usage, "completion_tokens_details", None)
      reasoning_tokens = getattr(completion_details, "reasoning_tokens", 0) if completion_details else 0
      usage_tracker.log_completion(
          prompt_tokens=getattr(completion.usage, "prompt_tokens", 0),
          completion_tokens=getattr(completion.usage, "completion_tokens", 0),
          reasoning_tokens=reasoning_tokens,
          response_text=content or "",
      )
    parsed = json.loads(content)
    score = float(parsed.get("coherence_score", 0.0))
    score = max(0.0, min(score, 1.0))
    justification = parsed.get("justification", "")
    return CoherenceResult(
        score=score,
        source="llm",
        explanation=justification,
    )
  except Exception as e:  # pylint: disable=broad-except
    logging.warning("LLM coherence scoring failed, fallback to heuristic: %s", e)
    return None


def _heuristic_coherence_score(
    response: str,
    unique_target: int = 90,
    desired_length: int = 120,
) -> CoherenceResult:
  """Lightweight heuristic when LLM scoring is unavailable."""
  unique_words = instructions_util.count_unique_words(response)
  length = instructions_util.count_words(response)
  unique_ratio = min(unique_words / unique_target, 1.0) if unique_target else 0.0
  length_ratio = min(length / desired_length, 1.0) if desired_length else 0.0
  score = (unique_ratio + length_ratio) / 2 if (unique_target and desired_length) else 0.0
  explanation = (
      f"Heurística: {unique_words} palavras únicas (meta {unique_target}), "
      f"{length} palavras totais (meta {desired_length})."
  )
  return CoherenceResult(score=score, source="heuristic", explanation=explanation)


def evaluate_coherence(
    prompt: str,
    response: str,
  book_context,
  llm_client: Any = None,
  llm_model: Optional[str] = None,
  llm_temperature: float = 0.0,
  unique_target: int = 90,
    desired_length: int = 120,
  usage_tracker: Optional[UsageTracker] = None,
) -> CoherenceResult:
  """Scores coherence using LLM when available; otherwise uses heuristic."""
  context_snippets = _select_book_context(prompt, book_context)
  llm_result = _llm_coherence_score(
      prompt=prompt,
      response=response,
      context_snippets=context_snippets,
      llm_client=llm_client,
      llm_model=llm_model,
      temperature=llm_temperature,
      usage_tracker=usage_tracker,
  )
  if llm_result:
    return llm_result
  return _heuristic_coherence_score(
      response=response,
      unique_target=unique_target,
      desired_length=desired_length,
  )


def score_instruction_and_coherence(
    inp: InputExample,
    strict_output: OutputExample,
    book_context,
    llm_client: Any = None,
    llm_model: Optional[str] = None,
    llm_temperature: float = 0.0,
    unique_target: int = 90,
    desired_length: int = 120,
    llm_usage_tracker: Optional[UsageTracker] = None,
) -> ScoredOutputExample:
  """Builds a scored example combining instruction and coherence metrics."""
  response = strict_output.response
  unique_word_count = instructions_util.count_unique_words(response)
  coherence_result = evaluate_coherence(
    prompt=inp.prompt,
    response=response,
    book_context=book_context,
    llm_client=llm_client,
    llm_model=llm_model,
      llm_temperature=llm_temperature,
      unique_target=unique_target,
      desired_length=desired_length,
      usage_tracker=llm_usage_tracker,
  )

  if strict_output.follow_instruction_list:
    instruction_score = (
        sum(strict_output.follow_instruction_list)
        / len(strict_output.follow_instruction_list)
    )
  else:
    instruction_score = 0.0

  final_score = (2 * instruction_score + coherence_result.score) / 3.0

  return ScoredOutputExample(
      key=inp.key,
      instruction_id_list=inp.instruction_id_list,
      prompt=inp.prompt,
      response=response,
      follow_all_instructions=strict_output.follow_all_instructions,
      follow_instruction_list=strict_output.follow_instruction_list,
      instruction_score=instruction_score,
      coherence_score=coherence_result.score,
      final_score=final_score,
      coherence_source=coherence_result.source,
      coherence_explanation=coherence_result.explanation,
      unique_word_count=unique_word_count,
  )


def print_score_report(outputs: Sequence[ScoredOutputExample]):
  """Prints aggregate statistics for the new scoring scheme."""
  if not outputs:
    print("No scored outputs to report.")
    return

  avg_instruction = sum(o.instruction_score for o in outputs) / len(outputs)
  avg_coherence = sum(o.coherence_score for o in outputs) / len(outputs)
  avg_final = sum(o.final_score for o in outputs) / len(outputs)

  print("=" * 64)
  print("Pontuações médias (cumprimento + coerência):")
  print(f"instrução: {avg_instruction:.4f}")
  print(f"coerência: {avg_coherence:.4f}")
  print(f"média final: {avg_final:.4f}")
