#!/bin/bash
set -euo pipefail

RUNS_DIR="runs"
INPUT_SINGLE="data/input_questions.jsonl"
INPUT_MULTI="data/input_questions_multiturn.jsonl"
BOOK_CONTEXT="data/book_context.json"

MODELS=(
    "claude-haiku-4.5"
    "claude-sonnet-4.5"
    "gemini-3-flash"
    "gemini-3-pro"
    "gpt-5.2"
    "gpt-5-mini"
    "qwen3-14b"
    "qwen3-235b"
    "qwen3-32b"
    "qwen3-8b"
    "sabia-3"
    "sabia-3.1"
    "sabia-4"
    "sabiazinho-3"
    "sabiazinho-4"
    "think-gpt-5"
)

for model_name in "${MODELS[@]}"; do
    echo "=== Avaliando ${model_name} ==="
    runs_dir="${RUNS_DIR}/${model_name}"
    eval_dir="${runs_dir}/eval"
    
    # Single-turn
    if [[ -f "${runs_dir}/single-turn/responses.jsonl" ]]; then
        echo "  Single-turn..."
        python3 run_eval.py \
            --input_data "${INPUT_SINGLE}" \
            --input_response_data "${runs_dir}/single-turn/responses.jsonl" \
            --output_dir "${eval_dir}/single-turn" \
            --book_context_path "${BOOK_CONTEXT}" \
            --quiet
    fi
    
    # Multi-turn
    if [[ -f "${runs_dir}/multi-turn/responses.jsonl" ]]; then
        echo "  Multi-turn..."
        python3 run_eval.py \
            --input_data "${INPUT_MULTI}" \
            --input_response_data "${runs_dir}/multi-turn/responses.jsonl" \
            --output_dir "${eval_dir}/multi-turn" \
            --book_context_path "${BOOK_CONTEXT}" \
            --quiet
    fi
done

echo "=== Avaliação concluída ==="
