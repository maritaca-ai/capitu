#!/usr/bin/env python3
"""
Gerador de respostas para o Capitu.

Suporta:
- Single-turn: uma pergunta por resposta
- Multi-turn: conversas com múltiplos turnos progressivos

Uso:
    # Single-turn
    python generate_responses.py --model_name "gpt-4o-mini" --api_base "https://api.openai.com/v1" \
        --input_data "data/input_questions.jsonl" --output_path "runs/exp1/responses.jsonl"

    # Multi-turn
    python generate_responses.py --model_name "gpt-4o-mini" --api_base "https://api.openai.com/v1" \
        --input_data "data/input_questions_multiturn.jsonl" --output_path "runs/exp1/responses_multiturn.jsonl"
"""

import argparse
import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import Optional

from tqdm import tqdm

from models.models import AssistantModel


@dataclass
class ResponseRecord:
    """Registro de uma resposta single-turn."""
    key: int
    prompt: str
    response: str
    model_name: str
    latency_s: float
    response_chars: int
    response_words: int
    difficulty: Optional[str] = None
    book: Optional[str] = None
    instruction_ids: Optional[list] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    reasoning_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    prompt_cost: Optional[float] = None
    completion_cost: Optional[float] = None
    total_cost: Optional[float] = None
    system_prompt: Optional[str] = None  


@dataclass
class MultiTurnResponseRecord:
    """Registro de uma conversa multi-turn."""
    key: int
    conversation_type: str
    book: str
    theme: str
    turns: list
    total_instructions: int
    model_name: str
    total_latency_s: float
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_cost: float = 0.0


def parse_parallel(value: str) -> int:
    """Valida argumento --parallel como inteiro positivo."""
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError(
            f"Valor inválido para --parallel: '{value}'. Esperado inteiro positivo."
        ) from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("--parallel deve ser >= 1")
    return parsed


def read_questions(input_path: str) -> list[dict]:
    """Lê questões do arquivo JSONL."""
    questions = []
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                questions.append(json.loads(line))
    return questions


def is_multi_turn_dataset(questions: list[dict]) -> bool:
    """Detecta se o dataset é multi-turn."""
    if not questions:
        return False
    return questions[0].get("is_multi_turn", False) or "turns" in questions[0]


def read_existing_responses(path: str, is_multi_turn: bool = False) -> dict:
    """Lê respostas existentes para retomada."""
    existing = {}
    if not Path(path).exists():
        return existing
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                key = data.get("key")
                if key is not None:
                    existing[key] = data
            except json.JSONDecodeError:
                continue
    return existing


class ResponseGenerator:
    """Gerador de respostas com suporte a single e multi-turn."""

    def __init__(
        self,
        model: AssistantModel,
        model_name: str,
        sleep_interval: float = 0.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        self.model = model
        self.model_name = model_name
        self.sleep_interval = sleep_interval
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._lock = Lock()

    def _call_with_retry(self, messages: list) -> tuple:
        """Chama o modelo com retry em caso de falha."""
        last_error = None
        max_attempts = self.max_retries
        for attempt in range(max_attempts):
            try:
                return self.model.generate_response(messages)
            except Exception as e:
                last_error = e
                is_rate_limit = "429" in str(e) or "rate" in str(e).lower()
                if attempt < max_attempts - 1:
                    if is_rate_limit:
                        wait_time = 60 * (attempt + 1)  # 60s, 120s, 180s...
                        print(f"\n[Rate limit] Aguardando {wait_time}s antes de tentar novamente (tentativa {attempt+1}/{max_attempts})...")
                    else:
                        wait_time = self.retry_delay * (2 ** attempt)
                    time.sleep(wait_time)
        raise last_error

    def generate_single_turn(self, question: dict) -> ResponseRecord:
        """Gera resposta para uma questão single-turn."""
        prompt = question["prompt"]

        original_system = self.model.system_prompt
        if "system_prompt" in question:
            self.model.system_prompt = question["system_prompt"]

        start = time.perf_counter()
        try:
            content, usage = self._call_with_retry([{"role": "user", "content": prompt}])
        finally:
            self.model.system_prompt = original_system
        latency_s = time.perf_counter() - start

        if self.sleep_interval:
            time.sleep(self.sleep_interval)

        record = ResponseRecord(
            key=question.get("key", 0),
            prompt=prompt,
            response=content or "",
            model_name=self.model_name,
            latency_s=latency_s,
            response_chars=len(content or ""),
            response_words=len((content or "").split()),
            difficulty=question.get("difficulty"),
            book=question.get("book"),
            instruction_ids=question.get("instruction_id_list"),
            system_prompt=question.get("system_prompt"),
        )

        if usage:
            record.prompt_tokens = usage.get("prompt_tokens")
            record.completion_tokens = usage.get("completion_tokens")
            record.reasoning_tokens = usage.get("reasoning_tokens")
            record.total_tokens = usage.get("total_tokens")
            record.prompt_cost = usage.get("prompt_cost")
            record.completion_cost = usage.get("completion_cost")
            record.total_cost = usage.get("cost")

        return record

    def generate_multi_turn(self, question: dict) -> MultiTurnResponseRecord:
        """Gera respostas para uma conversa multi-turn."""
        conversation_history = []
        turn_responses = []
        total_latency = 0.0
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_cost = 0.0

        for turn_data in question["turns"]:
            turn_num = turn_data["turn"]
            prompt = turn_data["prompt"]

            conversation_history.append({"role": "user", "content": prompt})

            start = time.perf_counter()
            content, usage = self._call_with_retry(conversation_history)
            latency_s = time.perf_counter() - start

            if self.sleep_interval:
                time.sleep(self.sleep_interval)

            conversation_history.append({"role": "assistant", "content": content or ""})

            turn_record = {
                "turn": turn_num,
                "prompt": prompt,
                "response": content or "",
                "latency_s": latency_s,
                "response_chars": len(content or ""),
                "response_words": len((content or "").split()),
                "instruction_id_list": turn_data.get("instruction_id_list", []),
                "new_instructions": turn_data.get("new_instructions", []),
            }

            if usage:
                turn_record["prompt_tokens"] = usage.get("prompt_tokens", 0)
                turn_record["completion_tokens"] = usage.get("completion_tokens", 0)
                turn_record["total_tokens"] = usage.get("total_tokens", 0)
                turn_record["cost"] = usage.get("cost", 0.0)
                total_prompt_tokens += usage.get("prompt_tokens", 0)
                total_completion_tokens += usage.get("completion_tokens", 0)
                total_cost += usage.get("cost", 0.0)

            turn_responses.append(turn_record)
            total_latency += latency_s

        return MultiTurnResponseRecord(
            key=question.get("key", 0),
            conversation_type=question.get("conversation_type", "unknown"),
            book=question.get("book", ""),
            theme=question.get("theme", ""),
            turns=turn_responses,
            total_instructions=question.get("total_instructions", 0),
            model_name=self.model_name,
            total_latency_s=total_latency,
            total_prompt_tokens=total_prompt_tokens,
            total_completion_tokens=total_completion_tokens,
            total_cost=total_cost,
        )


def compute_stats(records: list, is_multi_turn: bool = False) -> dict:
    """Calcula estatísticas das respostas geradas."""
    if not records:
        return {}

    if is_multi_turn:
        total_turns = sum(len(r.get("turns", [])) if isinstance(r, dict) else len(r.turns) for r in records)
        total_latency = sum(r.get("total_latency_s", 0) if isinstance(r, dict) else r.total_latency_s for r in records)
        total_prompt_tokens = sum(r.get("total_prompt_tokens", 0) if isinstance(r, dict) else r.total_prompt_tokens for r in records)
        total_completion_tokens = sum(r.get("total_completion_tokens", 0) if isinstance(r, dict) else r.total_completion_tokens for r in records)
        total_cost = sum(r.get("total_cost", 0) if isinstance(r, dict) else r.total_cost for r in records)

        return {
            "conversations": len(records),
            "total_turns": total_turns,
            "avg_turns_per_conversation": total_turns / len(records),
            "total_latency_s": total_latency,
            "avg_latency_per_turn_s": total_latency / total_turns if total_turns else 0,
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "total_cost": total_cost,
        }
    else:
        total_chars = sum(r.get("response_chars", 0) if isinstance(r, dict) else r.response_chars for r in records)
        total_words = sum(r.get("response_words", 0) if isinstance(r, dict) else r.response_words for r in records)
        total_latency = sum(r.get("latency_s", 0) if isinstance(r, dict) else r.latency_s for r in records)
        total_prompt_tokens = sum((r.get("prompt_tokens") or 0) if isinstance(r, dict) else (r.prompt_tokens or 0) for r in records)
        total_completion_tokens = sum((r.get("completion_tokens") or 0) if isinstance(r, dict) else (r.completion_tokens or 0) for r in records)
        total_cost = sum((r.get("total_cost") or 0) if isinstance(r, dict) else (r.total_cost or 0) for r in records)

        return {
            "responses": len(records),
            "avg_response_chars": total_chars / len(records),
            "avg_response_words": total_words / len(records),
            "total_latency_s": total_latency,
            "avg_latency_s": total_latency / len(records),
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "total_cost": total_cost,
        }


def main():
    parser = argparse.ArgumentParser(
        description="Gera respostas para o Capitu usando um modelo via API."
    )
    parser.add_argument("--model_name", required=True, help="Nome do modelo a ser usado.")
    parser.add_argument("--api_base", required=True, help="URL base da API.")
    parser.add_argument("--api_key", default="dummy_key", help="Chave da API.")
    parser.add_argument("--system_prompt", default=None, help="System prompt opcional.")
    parser.add_argument("--input_data", required=True, help="Arquivo JSONL com questões.")
    parser.add_argument("--output_path", required=True, help="Arquivo de saída JSONL.")
    parser.add_argument("--sleep", type=float, default=0.0, help="Intervalo entre chamadas (rate limit).")
    parser.add_argument("--append", action="store_true", help="Retoma geração existente.")
    parser.add_argument("--parallel", type=parse_parallel, default=1, help="Chamadas paralelas (apenas single-turn).")
    parser.add_argument("--max_retries", type=int, default=3, help="Tentativas em caso de erro (padrão: 3).")
    parser.add_argument("--prompt_price", type=float, default=None, help="Preço por 1k tokens de prompt (USD).")
    parser.add_argument("--completion_price", type=float, default=None, help="Preço por 1k tokens de completion (USD).")
    parser.add_argument(
        "--pricing_unit",
        choices=["1k", "1m"],
        default="1k",
        help="Unidade de precificação (1k ou 1m tokens).",
    )
    parser.add_argument("--provider", default=None, help="Provedor específico no OpenRouter (ex: DeepInfra, Together).")
    parser.add_argument("--reasoning_effort", default=None, choices=["low", "medium", "high"], help="Nível de esforço de raciocínio (para modelos com reasoning).")
    args = parser.parse_args()

    if not Path(args.input_data).exists():
        print(f"Erro: arquivo de entrada não encontrado: {args.input_data}")
        return

    questions = read_questions(args.input_data)
    if not questions:
        print("Nenhuma questão encontrada no arquivo de entrada.")
        return

    is_multi_turn = is_multi_turn_dataset(questions)
    print(f"Modo detectado: {'multi-turn' if is_multi_turn else 'single-turn'}")
    print(f"Total de {'conversas' if is_multi_turn else 'questões'}: {len(questions)}")

    existing = {}
    if args.append:
        existing = read_existing_responses(args.output_path, is_multi_turn)
        print(f"Respostas existentes carregadas: {len(existing)}")

    pending = [q for q in questions if q.get("key") not in existing]
    print(f"Questões pendentes: {len(pending)}")

    if not pending:
        print("Todas as questões já foram processadas.")
        return

    pricing = None
    if args.prompt_price is not None or args.completion_price is not None:
        pricing = {
            "prompt": args.prompt_price or 0.0,
            "completion": args.completion_price or 0.0,
            "unit": args.pricing_unit,
        }

    model = AssistantModel(
        model_name=args.model_name,
        api_base=args.api_base,
        api_key=args.api_key,
        system_prompt=args.system_prompt,
        pricing=pricing,
        provider=args.provider,
        reasoning_effort=args.reasoning_effort,
    )
    generator = ResponseGenerator(model, args.model_name, args.sleep, args.max_retries)

    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if args.append else "w"

    records = []
    lock = Lock()
    cumulative_cost = [0.0]  

    def update_cost_display(pbar, cost):
        cumulative_cost[0] += cost
        pbar.set_postfix({"custo": f"${cumulative_cost[0]:.4f}"}, refresh=True)

    with open(output_path, mode, encoding="utf-8") as f_out:
        if is_multi_turn:
            pbar = tqdm(pending, desc="Gerando conversas multi-turn")
            for question in pbar:
                record = generator.generate_multi_turn(question)
                record_dict = asdict(record)
                f_out.write(json.dumps(record_dict, ensure_ascii=False) + "\n")
                f_out.flush()
                records.append(record_dict)
                update_cost_display(pbar, record_dict.get("total_cost", 0))
        else:
            if args.parallel > 1:
                with ThreadPoolExecutor(max_workers=args.parallel) as executor:
                    futures = {executor.submit(generator.generate_single_turn, q): q for q in pending}
                    pbar = tqdm(as_completed(futures), total=len(pending), desc="Gerando respostas")
                    for future in pbar:
                        record = future.result()
                        record_dict = asdict(record)
                        with lock:
                            f_out.write(json.dumps(record_dict, ensure_ascii=False) + "\n")
                            f_out.flush()
                            records.append(record_dict)
                            update_cost_display(pbar, record_dict.get("total_cost") or 0)
            else:
                pbar = tqdm(pending, desc="Gerando respostas")
                for question in pbar:
                    record = generator.generate_single_turn(question)
                    record_dict = asdict(record)
                    f_out.write(json.dumps(record_dict, ensure_ascii=False) + "\n")
                    f_out.flush()
                    records.append(record_dict)
                    update_cost_display(pbar, record_dict.get("total_cost") or 0)

    stats = compute_stats(records, is_multi_turn)
    stats["model_name"] = args.model_name
    stats["is_multi_turn"] = is_multi_turn

    stats_path = output_path.with_name("generation_stats.json")
    stats_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n" + "=" * 64)
    print("GERAÇÃO CONCLUÍDA")
    print("=" * 64)
    print(f"Arquivo de saída: {output_path}")
    print(f"Estatísticas salvas em: {stats_path}")
    print(f"Novas respostas geradas: {len(records)}")

    if is_multi_turn:
        print(f"Total de turnos: {stats.get('total_turns', 0)}")
        print(f"Média de turnos por conversa: {stats.get('avg_turns_per_conversation', 0):.1f}")
    else:
        print(f"Média de palavras por resposta: {stats.get('avg_response_words', 0):.1f}")
        print(f"Média de caracteres por resposta: {stats.get('avg_response_chars', 0):.1f}")

    print(f"Latência total: {stats.get('total_latency_s', 0):.2f}s")
    if stats.get("total_cost", 0) > 0:
        print(f"Custo total estimado: ${stats.get('total_cost', 0):.4f}")


if __name__ == "__main__":
    main()
