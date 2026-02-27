#!/usr/bin/env bash
# =============================================================================
# CAPITU Benchmark - Script para rodar todos os modelos do paper
# =============================================================================
# Este script gera respostas e avalia todos os modelos mencionados no paper:
# - GPT-5.2, GPT-5-mini (OpenAI)
# - Claude Sonnet 4.5, Claude Haiku 4.5 (Anthropic via OpenRouter)
# - Gemini 3 Pro, Gemini 3 Flash (Google via OpenRouter)
# - Qwen3 8B, 14B, 32B, 235B (via OpenRouter)
# - Sabiá-3, Sabiá-3.1, Sabiá-4, Sabiazinho-3, Sabiazinho-4 (Maritaca AI)
#
# Uso:
#   bash run_paper_models.sh [generate|eval|all] [--model MODEL_NAME]
#
# =============================================================================

set -uo pipefail 

# OpenAI API (GPT-5.2, GPT-5-mini)
OPENAI_API_KEY="${OPENAI_API_KEY:-sua-chave-openai}"
OPENAI_API_BASE="https://api.openai.com/v1"

# OpenRouter API (Claude, Gemini, Qwen - API compatível com OpenAI)
# Preços são retornados diretamente na resposta da API
OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-sua-chave-openrouter}"
OPENROUTER_API_BASE="https://openrouter.ai/api/v1"

# Maritaca AI API (Sabiá, Sabiazinho)
MARITACA_API_KEY="${MARITACA_API_KEY:-sua-chave-maritaca}"
MARITACA_API_BASE="https://chat.maritaca.ai/api"

# Modelo juiz (usa GPT-4o-mini por padrão para avaliar coerência)
JUDGE_MODEL_NAME="gpt-4o-mini"
JUDGE_API_BASE="${OPENAI_API_BASE}"
JUDGE_API_KEY="${OPENAI_API_KEY}"

RUNS_DIR="${RUNS_DIR:-runs}"
INPUT_SINGLE="data/input_questions.jsonl"
INPUT_MULTI="data/input_questions_multiturn.jsonl"
BOOK_CONTEXT="data/book_context.json"
PARALLEL="${PARALLEL:-4}"


declare -a MODELS=(
    # === OpenAI Models (direto) ===
    "gpt-5.2|${OPENAI_API_BASE}|${OPENAI_API_KEY}|1.75|14.00|1m"
    "gpt-5-mini|${OPENAI_API_BASE}|${OPENAI_API_KEY}|0.25|2|1m"

    # === Anthropic Models (via OpenRouter) ===
    "anthropic/claude-sonnet-4.5|${OPENROUTER_API_BASE}|${OPENROUTER_API_KEY}|3.00|15.00|1m"
    "anthropic/claude-haiku-4.5|${OPENROUTER_API_BASE}|${OPENROUTER_API_KEY}|1.00|5|1m"

    # === Google Models (via OpenRouter) ===
    "google/gemini-3-pro-preview|${OPENROUTER_API_BASE}|${OPENROUTER_API_KEY}|2.00|12.00|1m"
    "google/gemini-3-flash-preview|${OPENROUTER_API_BASE}|${OPENROUTER_API_KEY}|0.50|3.00|1m"

    # === Qwen Models (via OpenRouter) ===
    "qwen/qwen3-8b|${OPENROUTER_API_BASE}|${OPENROUTER_API_KEY}|0.05|0.40|1m"
    "qwen/qwen3-14b|${OPENROUTER_API_BASE}|${OPENROUTER_API_KEY}|0.06|0.24|1m"
    "qwen/qwen3-32b|${OPENROUTER_API_BASE}|${OPENROUTER_API_KEY}|0.08|0.28|1m"
    "qwen/qwen3-235b-a22b-2507|${OPENROUTER_API_BASE}|${OPENROUTER_API_KEY}|0.075|0.463|1m"

    # === Maritaca AI Models (Portuguese-specialized) ===
    "sabia-3|${MARITACA_API_BASE}|${MARITACA_API_KEY}|0.97|1.92|1m" 
    "sabia-3.1|${MARITACA_API_BASE}|${MARITACA_API_KEY}|0.97|1.92|1m"
    "sabia-4|${MARITACA_API_BASE}|${MARITACA_API_KEY}|0.97|3.83|1m" 
    "sabiazinho-3|${MARITACA_API_BASE}|${MARITACA_API_KEY}|0.21|0.59|1m" 
    "sabiazinho-4|${MARITACA_API_BASE}|${MARITACA_API_KEY}|0.21|0.78|1m" 
)

declare -A MODEL_DISPLAY_NAMES=(
    # OpenAI
    ["gpt-5.2"]="gpt-5.2"
    ["gpt-5-mini"]="gpt-5-mini"
    # Anthropic (via OpenRouter)
    ["anthropic/claude-sonnet-4.5"]="claude-sonnet-4.5"
    ["anthropic/claude-haiku-4.5"]="claude-haiku-4.5"
    # Google (via OpenRouter)
    ["google/gemini-3-pro-preview"]="gemini-3-pro"
    ["google/gemini-3-flash-preview"]="gemini-3-flash"
    # Qwen (via OpenRouter)
    ["qwen/qwen3-8b"]="qwen3-8b"
    ["qwen/qwen3-14b"]="qwen3-14b"
    ["qwen/qwen3-32b"]="qwen3-32b"
    ["qwen/qwen3-235b-a22b-2507"]="qwen3-235b"
    # Maritaca AI
    ["sabia-3"]="sabia-3"
    ["sabia-3.1"]="sabia-3.1"
    ["sabia-4"]="sabia-4"
    ["sabiazinho-3"]="sabiazinho-3"
    ["sabiazinho-4"]="sabiazinho-4"
)


log_info() {
    echo -e "\n\033[1;34m[INFO]\033[0m $1"
}

log_success() {
    echo -e "\033[1;32m[OK]\033[0m $1"
}

log_error() {
    echo -e "\033[1;31m[ERRO]\033[0m $1"
}

log_warning() {
    echo -e "\033[1;33m[AVISO]\033[0m $1"
}

log_separator() {
    echo ""
    echo "========================================================================"
    echo "$1"
    echo "========================================================================"
}

get_display_name() {
    local model_name="$1"
    echo "${MODEL_DISPLAY_NAMES[$model_name]:-$model_name}"
}


generate_responses() {
    local model_name="$1"
    local api_base="$2"
    local api_key="$3"
    local prompt_price="$4"
    local completion_price="$5"
    local pricing_unit="$6"

    local display_name
    display_name=$(get_display_name "${model_name}")
    local output_dir="${RUNS_DIR}/${display_name}"
    mkdir -p "${output_dir}/single-turn" "${output_dir}/multi-turn"

    log_info "Gerando respostas single-turn para ${display_name}..."

    python3 generate_responses.py \
        --model_name "${model_name}" \
        --api_base "${api_base}" \
        --api_key "${api_key}" \
        --input_data "${INPUT_SINGLE}" \
        --output_path "${output_dir}/single-turn/responses.jsonl" \
        --parallel "${PARALLEL}" \
        --prompt_price "${prompt_price}" \
        --completion_price "${completion_price}" \
        --pricing_unit "${pricing_unit}" \
        --append

    log_success "Single-turn concluído para ${display_name}"

    if [[ -f "${INPUT_MULTI}" ]]; then
        log_info "Gerando respostas multi-turn para ${display_name}..."

        python3 generate_responses.py \
            --model_name "${model_name}" \
            --api_base "${api_base}" \
            --api_key "${api_key}" \
            --input_data "${INPUT_MULTI}" \
            --output_path "${output_dir}/multi-turn/responses.jsonl" \
            --prompt_price "${prompt_price}" \
            --completion_price "${completion_price}" \
            --pricing_unit "${pricing_unit}" \
            --append

        log_success "Multi-turn concluído para ${display_name}"
    else
        log_warning "Arquivo multi-turn não encontrado: ${INPUT_MULTI}"
    fi
}


evaluate_model() {
    local model_name="$1"

    local display_name
    display_name=$(get_display_name "${model_name}")
    local model_dir="${RUNS_DIR}/${display_name}"
    local eval_dir="${model_dir}/eval"
    mkdir -p "${eval_dir}/single-turn" "${eval_dir}/multi-turn"

    local judge_args=""
    if [[ -n "${JUDGE_MODEL_NAME}" && -n "${JUDGE_API_BASE}" && -n "${JUDGE_API_KEY}" ]]; then
        judge_args="--judge_model_name ${JUDGE_MODEL_NAME} --judge_api_base ${JUDGE_API_BASE} --judge_api_key ${JUDGE_API_KEY}"
        log_info "Usando juiz de coerência: ${JUDGE_MODEL_NAME}"
    else
        log_warning "Juiz de coerência não configurado. Avaliação será apenas de instruções."
    fi

    if [[ -f "${model_dir}/single-turn/responses.jsonl" ]]; then
        log_info "Avaliando single-turn para ${display_name}..."

        python3 run_eval.py \
            --input_data "${INPUT_SINGLE}" \
            --input_response_data "${model_dir}/single-turn/responses.jsonl" \
            --output_dir "${eval_dir}/single-turn" \
            --book_context_path "${BOOK_CONTEXT}" \
            ${judge_args}

        log_success "Avaliação single-turn concluída para ${display_name}"
    else
        log_error "Arquivo de respostas single-turn não encontrado: ${model_dir}/single-turn/responses.jsonl"
    fi

    if [[ -f "${model_dir}/multi-turn/responses.jsonl" ]]; then
        log_info "Avaliando multi-turn para ${display_name}..."

        python3 run_eval.py \
            --input_data "${INPUT_MULTI}" \
            --input_response_data "${model_dir}/multi-turn/responses.jsonl" \
            --output_dir "${eval_dir}/multi-turn" \
            --book_context_path "${BOOK_CONTEXT}" \
            ${judge_args}

        log_success "Avaliação multi-turn concluída para ${display_name}"
    else
        log_info "Arquivo de respostas multi-turn não encontrado, pulando..."
    fi
}


run_generation() {
    log_separator "INICIANDO GERAÇÃO DE RESPOSTAS PARA TODOS OS MODELOS DO PAPER"

    local total_models=${#MODELS[@]}
    local current=0
    local failed_models=()

    for model_config in "${MODELS[@]}"; do
        IFS='|' read -r model_name api_base api_key prompt_price completion_price pricing_unit <<< "${model_config}"
        ((current++))

        local display_name
        display_name=$(get_display_name "${model_name}")
        log_separator "[${current}/${total_models}] Modelo: ${display_name}"

        if ! generate_responses "${model_name}" "${api_base}" "${api_key}" \
            "${prompt_price}" "${completion_price}" "${pricing_unit}"; then
            log_error "Falha na geração para ${display_name}. Continuando com próximo modelo..."
            failed_models+=("${display_name}")
        fi
    done

    log_separator "GERAÇÃO CONCLUÍDA PARA TODOS OS MODELOS"

    if [[ ${#failed_models[@]} -gt 0 ]]; then
        log_warning "Modelos com falha na geração: ${failed_models[*]}"
    fi
}

run_evaluation() {
    log_separator "INICIANDO AVALIAÇÃO DE TODOS OS MODELOS"

    local total_models=${#MODELS[@]}
    local current=0
    local failed_models=()

    for model_config in "${MODELS[@]}"; do
        IFS='|' read -r model_name _ <<< "${model_config}"
        ((current++))

        local display_name
        display_name=$(get_display_name "${model_name}")
        log_separator "[${current}/${total_models}] Avaliando: ${display_name}"

        if ! evaluate_model "${model_name}"; then
            log_error "Falha na avaliação para ${display_name}. Continuando com próximo modelo..."
            failed_models+=("${display_name}")
        fi
    done

    if [[ ${#failed_models[@]} -gt 0 ]]; then
        log_warning "Modelos com falha na avaliação: ${failed_models[*]}"
    fi

    log_separator "AVALIAÇÃO CONCLUÍDA PARA TODOS OS MODELOS"
}


generate_summary() {
    log_separator "GERANDO RELATÓRIO CONSOLIDADO"

    local summary_file="${RUNS_DIR}/summary_all_models.md"

    cat > "${summary_file}" << 'EOF'
# CAPITU Benchmark - Resultados Consolidados

## Modelos Avaliados

| Modelo | Tipo | Parâmetros |
|--------|------|------------|
| GPT-5.2 | Proprietário | - |
| GPT-5-mini | Proprietário | - |
| Claude Sonnet 4.5 | Proprietário | - |
| Claude Haiku 4.5 | Proprietário | - |
| Gemini 3 Pro | Proprietário | - |
| Gemini 3 Flash | Proprietário | - |
| Qwen3 8B | Open-weight | 8B |
| Qwen3 14B | Open-weight | 14B |
| Qwen3 32B | Open-weight | 32B |
| Qwen3 235B | Open-weight | 235B |
| Sabiá-3 | PT-BR Especializado | - |
| Sabiá-3.1 | PT-BR Especializado | - |
| Sabiá-4 | PT-BR Especializado | - |
| Sabiazinho-3 | PT-BR Especializado | - |
| Sabiazinho-4 | PT-BR Especializado | - |

## Resultados Single-Turn

EOF

    echo "| Modelo | Strict (%) | Loose (%) | Instr. (%) | Coerência |" >> "${summary_file}"
    echo "|--------|------------|-----------|------------|-----------|" >> "${summary_file}"

    for model_config in "${MODELS[@]}"; do
        IFS='|' read -r model_name _ <<< "${model_config}"
        local display_name
        display_name=$(get_display_name "${model_name}")
        local report_file="${RUNS_DIR}/${display_name}/eval/single-turn/metrics_report.json"

        if [[ -f "${report_file}" ]]; then
            local strict loose instr coherence
            strict=$(jq -r '.strict_accuracy // "N/A"' "${report_file}")
            loose=$(jq -r '.loose_accuracy // "N/A"' "${report_file}")
            instr=$(jq -r '.instruction_accuracy // "N/A"' "${report_file}")
            coherence=$(jq -r '.avg_coherence_score // "N/A"' "${report_file}")
            echo "| ${display_name} | ${strict} | ${loose} | ${instr} | ${coherence} |" >> "${summary_file}"
        else
            echo "| ${display_name} | - | - | - | - |" >> "${summary_file}"
        fi
    done

    cat >> "${summary_file}" << 'EOF'

## Resultados Multi-Turn

EOF

    echo "| Modelo | Conv. (%) | Turn 1 (%) | Turn 2 (%) | Turn 3 (%) |" >> "${summary_file}"
    echo "|--------|-----------|------------|------------|------------|" >> "${summary_file}"

    for model_config in "${MODELS[@]}"; do
        IFS='|' read -r model_name _ <<< "${model_config}"
        local display_name
        display_name=$(get_display_name "${model_name}")
        local report_file="${RUNS_DIR}/${display_name}/eval/multi-turn/metrics_report.json"

        if [[ -f "${report_file}" ]]; then
            local conv t1 t2 t3
            conv=$(jq -r '.conversation_accuracy // "N/A"' "${report_file}")
            t1=$(jq -r '.turn_accuracy.turn_1 // "N/A"' "${report_file}")
            t2=$(jq -r '.turn_accuracy.turn_2 // "N/A"' "${report_file}")
            t3=$(jq -r '.turn_accuracy.turn_3 // "N/A"' "${report_file}")
            echo "| ${display_name} | ${conv} | ${t1} | ${t2} | ${t3} |" >> "${summary_file}"
        else
            echo "| ${display_name} | - | - | - | - |" >> "${summary_file}"
        fi
    done

    log_success "Relatório consolidado salvo em: ${summary_file}"
}

show_help() {
    cat << EOF
CAPITU Benchmark - Script para rodar todos os modelos do paper

Uso: $0 [comando] [opções]

Comandos:
  generate    Gera respostas para todos os modelos
  eval        Avalia respostas de todos os modelos (com juiz de coerência)
  all         Gera e avalia todos os modelos (padrão)
  summary     Gera relatório consolidado dos resultados
  list        Lista os modelos configurados
  help        Mostra esta ajuda

Opções:
  --model NAME    Roda apenas para o modelo especificado

Variáveis de ambiente:
  RUNS_DIR        Diretório base para resultados (padrão: runs)
  PARALLEL        Número de chamadas paralelas (padrão: 4)

Modelos do paper:
  - gpt-5.2, gpt-5-mini 
  - claude-sonnet-4.5, claude-haiku-4.5
  - gemini-3-pro, gemini-3-flash
  - qwen3-8b, qwen3-14b, qwen3-32b, qwen3-235b
  - sabia-3, sabia-3.1, sabia-4, sabiazinho-3, sabiazinho-4

EOF
}

list_models() {
    echo ""
    echo "Modelos configurados para o paper CAPITU:"
    echo ""
    printf "%-45s %-25s\n" "Nome da API" "Nome no Paper"
    echo "------------------------------------------------------------------------"
    for model_config in "${MODELS[@]}"; do
        IFS='|' read -r model_name api_base _ _ _ _ <<< "${model_config}"
        local display_name
        display_name=$(get_display_name "${model_name}")
        printf "%-45s %-25s\n" "${model_name}" "${display_name}"
    done
    echo ""
}

main() {
    local command="${1:-all}"
    local specific_model=""

    # Parse argumentos
    shift || true
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --model)
                specific_model="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    if [[ -n "${specific_model}" ]]; then
        local filtered_models=()
        for model_config in "${MODELS[@]}"; do
            IFS='|' read -r model_name _ <<< "${model_config}"
            local display_name
            display_name=$(get_display_name "${model_name}")
            if [[ "${model_name}" == "${specific_model}" ]] || [[ "${display_name}" == "${specific_model}" ]]; then
                filtered_models+=("${model_config}")
            fi
        done
        if [[ ${#filtered_models[@]} -eq 0 ]]; then
            log_error "Modelo '${specific_model}' não encontrado nas configurações"
            echo "Use '$0 list' para ver os modelos disponíveis"
            exit 1
        fi
        MODELS=("${filtered_models[@]}")
    fi

    case "${command}" in
        generate)
            run_generation
            ;;
        eval)
            run_evaluation
            ;;
        all)
            run_generation
            run_evaluation
            generate_summary
            ;;
        summary)
            generate_summary
            ;;
        list)
            list_models
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Comando desconhecido: ${command}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
