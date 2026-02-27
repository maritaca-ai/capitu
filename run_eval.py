#!/usr/bin/env python3
"""
Avaliador do Capitu com métricas detalhadas.
    python run_eval.py --input_data data/input_questions.jsonl \
        --input_response_data runs/exp1/responses.jsonl \
        --output_dir runs/exp1/eval
"""

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from tqdm import tqdm

import evaluation_lib
from metrics import MetricsCalculator, print_report, save_report_json, generate_markdown_report


@dataclass
class EvalConfig:
    """Configuração da avaliação."""
    input_data: str
    input_response_data: str
    output_dir: str
    book_context_path: str = "data/book_context.json"
    judge_model_name: Optional[str] = None
    judge_api_base: Optional[str] = None
    judge_api_key: Optional[str] = None
    llm_temperature: float = 0.0
    coherence_use_context: bool = True
    coherence_unique_target: int = 90
    coherence_desired_length: int = 120
    verbose: bool = True


def is_multi_turn_dataset(questions: list[dict]) -> bool:
    """Detecta se o dataset é multi-turn."""
    if not questions:
        return False
    return questions[0].get("is_multi_turn", False) or "turns" in questions[0]


def read_questions(path: str) -> list[dict]:
    """Lê questões do arquivo JSONL."""
    questions = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                questions.append(json.loads(line))
    return questions


def read_responses(path: str) -> dict:
    """Lê respostas do arquivo JSONL, indexadas por key."""
    responses = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data = json.loads(line)
                key = data.get("key")
                if key is not None:
                    responses[key] = data
    return responses


def evaluate_single_turn(
    questions: list[dict],
    responses: dict,
    config: EvalConfig,
    book_context: list,
    llm_client,
    llm_model: str,
    llm_usage_tracker,
):
    """Avalia dataset single-turn com métricas detalhadas."""

    prompt_to_response = {}
    key_to_response = {}
    for key, resp_data in responses.items():
        prompt = resp_data.get("prompt", "")
        response = resp_data.get("response", "")
        prompt_to_response[prompt] = response
        key_to_response[key] = resp_data

    inputs = evaluation_lib.read_prompt_list(config.input_data)

    calc = MetricsCalculator()

    print("\n" + "=" * 64)
    print("AVALIAÇÃO ESTRITA")
    print("=" * 64)

    strict_outputs = []
    for inp in tqdm(inputs, desc="Avaliando instruções (modo estrito)"):
        strict_outputs.append(
            evaluation_lib.test_instruction_following_strict(inp, prompt_to_response)
        )

    strict_output_file = os.path.join(config.output_dir, "eval_results_strict.jsonl")
    evaluation_lib.write_outputs(strict_output_file, strict_outputs)

    print("\nAvaliando instruções (modo flexível)...")
    loose_outputs = []
    for inp in tqdm(inputs, desc="Avaliando instruções (modo flexível)"):
        loose_outputs.append(
            evaluation_lib.test_instruction_following_loose(inp, prompt_to_response)
        )

    loose_output_file = os.path.join(config.output_dir, "eval_results_loose.jsonl")
    evaluation_lib.write_outputs(loose_output_file, loose_outputs)

    print("\nPontuando coerência...")
    scored_outputs = []
    for inp, strict_output in tqdm(
        zip(inputs, strict_outputs),
        total=len(inputs),
        desc="Pontuando coerência"
    ):
        scored_outputs.append(
            evaluation_lib.score_instruction_and_coherence(
                inp,
                strict_output,
                book_context=book_context,
                llm_client=llm_client,
                llm_model=llm_model,
                llm_temperature=config.llm_temperature,
                unique_target=config.coherence_unique_target,
                desired_length=config.coherence_desired_length,
                llm_usage_tracker=llm_usage_tracker,
            )
        )

    scored_output_file = os.path.join(config.output_dir, "eval_results_scored.jsonl")
    evaluation_lib.write_outputs(scored_output_file, scored_outputs)

    for q, strict_out, loose_out, scored_out in zip(questions, strict_outputs, loose_outputs, scored_outputs):
        response_text = prompt_to_response.get(q.get("prompt", ""), "")

        calc.add_single_turn_result(
            instruction_ids=strict_out.instruction_id_list,
            follow_list=strict_out.follow_instruction_list,
            follow_all=strict_out.follow_all_instructions,
            difficulty=q.get("difficulty", "unknown"),
            book=q.get("book", "unknown"),
            coherence_score=scored_out.get("coherence_score", 0.0) if isinstance(scored_out, dict) else getattr(scored_out, "coherence_score", 0.0),
            final_score=scored_out.get("final_score", 0.0) if isinstance(scored_out, dict) else getattr(scored_out, "final_score", 0.0),
            response_text=response_text,
            loose_follow_all=loose_out.follow_all_instructions,
        )

    report = calc.compute_report(
        model_name=responses.get(list(responses.keys())[0], {}).get("model_name", "") if responses else "",
        dataset_name=config.input_data,
        is_multi_turn=False,
    )

    return report, strict_outputs, loose_outputs, scored_outputs


def evaluate_multi_turn(
    questions: list[dict],
    responses: dict,
    config: EvalConfig,
):
    """Avalia dataset multi-turn com métricas detalhadas."""

    calc = MetricsCalculator()
    results = []

    for question in tqdm(questions, desc="Avaliando conversas multi-turn"):
        key = question.get("key")
        if key not in responses:
            print(f"Aviso: resposta não encontrada para key={key}")
            continue

        response_data = responses[key]
        response_turns = response_data.get("turns", [])

        conversation_result = {
            "key": key,
            "book": question.get("book", ""),
            "conversation_type": question.get("conversation_type", ""),
            "turns": [],
            "all_instructions_followed": True,
        }

        for turn_data, response_turn in zip(question.get("turns", []), response_turns):
            turn_num = turn_data["turn"]
            instruction_ids = turn_data.get("instruction_id_list", [])
            kwargs_list = turn_data.get("kwargs", [])
            response_text = response_turn.get("response", "")

            turn_input = evaluation_lib.InputExample(
                key=f"{key}_turn{turn_num}",
                instruction_id_list=instruction_ids,
                prompt=turn_data.get("prompt", ""),
                kwargs=kwargs_list,
            )

            prompt_to_response = {turn_input.prompt: response_text}
            turn_result = evaluation_lib.test_instruction_following_strict(
                turn_input, prompt_to_response
            )

            turn_passed = turn_result.follow_all_instructions
            if not turn_passed:
                conversation_result["all_instructions_followed"] = False

            conversation_result["turns"].append({
                "turn": turn_num,
                "instructions": instruction_ids,
                "followed": turn_result.follow_instruction_list,
                "all_followed": turn_passed,
            })

        calc.add_multi_turn_result(
            turns=conversation_result["turns"],
            all_correct=conversation_result["all_instructions_followed"],
        )

        results.append(conversation_result)

    output_file = os.path.join(config.output_dir, "eval_results_multiturn.jsonl")
    with open(output_file, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    report = calc.compute_report(
        model_name=responses.get(list(responses.keys())[0], {}).get("model_name", "") if responses else "",
        dataset_name=config.input_data,
        is_multi_turn=True,
    )

    return report, results


def main():
    parser = argparse.ArgumentParser(description="Avaliador do Capitu com métricas detalhadas.")
    parser.add_argument("--input_data", required=True, help="Arquivo JSONL com questões.")
    parser.add_argument("--input_response_data", required=True, help="Arquivo JSONL com respostas.")
    parser.add_argument("--output_dir", required=True, help="Diretório de saída.")
    parser.add_argument("--book_context_path", default="data/book_context.json", help="Contexto dos livros.")
    parser.add_argument("--judge_model_name", default=None, help="Modelo julgador para coerência.")
    parser.add_argument("--judge_api_base", default=None, help="URL base da API do julgador.")
    parser.add_argument("--judge_api_key", default=None, help="Chave da API do julgador.")
    parser.add_argument("--llm_temperature", type=float, default=0.0, help="Temperatura do julgador.")
    parser.add_argument("--coherence_use_context", action="store_true", default=True, help="Usar contexto dos livros (padrão: True).")
    parser.add_argument("--no_coherence_context", action="store_true", help="Não usar contexto dos livros.")
    parser.add_argument("--coherence_unique_target", type=int, default=90, help="Meta de palavras únicas.")
    parser.add_argument("--coherence_desired_length", type=int, default=120, help="Meta de comprimento.")
    parser.add_argument("--quiet", action="store_true", help="Reduzir output (menos detalhes).")
    args = parser.parse_args()

    if not os.path.exists(args.input_data):
        print(f"Erro: arquivo de questões não encontrado: {args.input_data}")
        return
    if not os.path.exists(args.input_response_data):
        print(f"Erro: arquivo de respostas não encontrado: {args.input_response_data}")
        return

    use_context = not args.no_coherence_context

    config = EvalConfig(
        input_data=args.input_data,
        input_response_data=args.input_response_data,
        output_dir=args.output_dir,
        book_context_path=args.book_context_path,
        judge_model_name=args.judge_model_name,
        judge_api_base=args.judge_api_base,
        judge_api_key=args.judge_api_key,
        llm_temperature=args.llm_temperature,
        coherence_use_context=use_context,
        coherence_unique_target=args.coherence_unique_target,
        coherence_desired_length=args.coherence_desired_length,
        verbose=not args.quiet,
    )

    os.makedirs(config.output_dir, exist_ok=True)

    questions = read_questions(config.input_data)
    responses = read_responses(config.input_response_data)

    question_keys = {q.get("key") for q in questions}
    response_keys = set(responses.keys())
    missing_responses = question_keys - response_keys
    if missing_responses:
        print(f"Aviso: {len(missing_responses)} questões sem resposta correspondente")
        if config.verbose:
            print(f"  Keys faltando: {sorted(list(missing_responses))[:10]}{'...' if len(missing_responses) > 10 else ''}")

    print(f"Questões carregadas: {len(questions)}")
    print(f"Respostas carregadas: {len(responses)}")

    is_multi_turn = is_multi_turn_dataset(questions)
    print(f"Modo detectado: {'multi-turn' if is_multi_turn else 'single-turn'}")

    raw_book_context = evaluation_lib.load_book_context(config.book_context_path)
    book_context = raw_book_context if config.coherence_use_context else []

    llm_model = config.judge_model_name
    llm_client = None
    if config.judge_api_base and config.judge_api_key:
        llm_client = evaluation_lib.build_openai_client(
            api_base=config.judge_api_base,
            api_key=config.judge_api_key,
        )
    elif llm_model:
        llm_client = evaluation_lib.build_openai_client()

    llm_usage_tracker = None
    if llm_client and llm_model:
        llm_usage_tracker = evaluation_lib.UsageTracker(model_name=llm_model)

    if is_multi_turn:
        report, results = evaluate_multi_turn(questions, responses, config)
    else:
        report, strict_outputs, loose_outputs, scored_outputs = evaluate_single_turn(
            questions, responses, config, book_context,
            llm_client, llm_model, llm_usage_tracker
        )

    print_report(report, verbose=config.verbose)

    if llm_usage_tracker:
        usage_path = os.path.join(config.output_dir, "judge_usage.json")
        with open(usage_path, "w", encoding="utf-8") as f:
            json.dump(llm_usage_tracker.as_dict(), f, ensure_ascii=False, indent=2)

    report_json_path = Path(config.output_dir) / "metrics_report.json"
    save_report_json(report, report_json_path)
    print(f"\nRelatório JSON salvo em: {report_json_path}")

    report_md_path = Path(config.output_dir) / "metrics_report.md"
    generate_markdown_report(report, report_md_path)
    print(f"Relatório Markdown salvo em: {report_md_path}")

    print("\n" + "=" * 64)
    print("AVALIAÇÃO CONCLUÍDA")
    print("=" * 64)
    print(f"Todos os resultados salvos em: {config.output_dir}")


if __name__ == "__main__":
    main()
