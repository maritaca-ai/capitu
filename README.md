# CAPITU: A Benchmark for Evaluating Instruction-Following in Brazilian Portuguese with Literary Context

**Giovana Kerche Bonás, Roseval Malaquias Junior, Marcos Piau, Thiago Laitz, Thales Sales Almeida, Hugo Abonizio, Celio Larcher, Ramon Pires, Rodrigo Nogueira**

Maritaca AI &bull; Jusbrasil

---

## Overview

CAPITU is a benchmark for evaluating instruction-following capabilities of Large Language Models (LLMs) in Brazilian Portuguese. Unlike existing benchmarks that focus on English or use generic prompts, CAPITU contextualizes all tasks within eight canonical works of Brazilian literature, combining **59 automatically verifiable instruction types** across **7 categories** with culturally grounded content.

The benchmark includes **200 single-turn prompts** and **100 multi-turn conversations** (3 turns each), evaluated across **18 state-of-the-art models**. All instruction types are deterministically verifiable without requiring LLM judges or human evaluation.

Key contributions:
- A Portuguese-specific instruction taxonomy with morphological constraints native to the language (-ando/-endo/-indo, -inho/-inha, -mente)
- Culturally contextualized prompts grounded in 8 Brazilian literary classics
- Multi-turn evaluation with constraint accumulation across turns
- Comprehensive baseline results for 18 models with cost-performance analysis

## Results

| Model | Provider | Strict (%) | Instr. (%) | Conv. (%) | Cost ($) |
|-------|----------|:----------:|:----------:|:---------:|:--------:|
| GPT-5.2† | OpenAI | **98.5** | 99.3 | 83.0 | 5.04 |
| GPT-5† | OpenAI | 98.0 | 99.0 | 90.0 | 8.76 |
| GPT-5-mini† | OpenAI | 98.0 | 99.0 | **96.0** | 1.36 |
| Gemini-3-Pro† | Google | 92.5 | 95.3 | 95.0 | 10.80 |
| GPT-5.2 | OpenAI | 91.5 | 95.1 | 73.0 | 2.51 |
| Gemini-3-Flash | Google | 89.0 | 94.3 | 95.0 | 0.48 |
| Sabiazinho-4 | Maritaca AI | 87.0 | 93.1 | 87.0 | 0.13 |
| Claude-Sonnet-4.5 | Anthropic | 86.0 | 90.6 | 87.0 | 3.69 |
| Sabiá-4 | Maritaca AI | 84.5 | 91.6 | 78.0 | 0.64 |
| Qwen3-235b-a22b† | Alibaba | 84.0 | 87.7 | 64.0 | 3.72 |
| Qwen3-32B† | Alibaba | 82.5 | 90.1 | 60.0 | 0.46 |
| Qwen3-8B† | Alibaba | 81.5 | 90.4 | 72.0 | 0.25 |
| Qwen3-14B† | Alibaba | 81.0 | 89.4 | 74.0 | 0.39 |
| Qwen3-235b-a22b | Alibaba | 79.5 | 89.4 | 60.0 | 0.22 |
| Sabiá-3 | Maritaca AI | 77.0 | 86.4 | 64.0 | 0.45 |
| Sabiá-3.1 | Maritaca AI | 74.0 | 85.4 | 64.0 | 0.42 |
| Claude-Haiku-4.5 | Anthropic | 73.5 | 82.5 | 72.0 | 1.12 |

†Reasoning/thinking mode enabled. **Strict**: prompt-level accuracy (all instructions correct). **Instr.**: instruction-level accuracy. **Conv.**: multi-turn conversation accuracy (all turns correct). **Cost**: total API cost for the full evaluation (USD).

## Installation

```bash
git clone https://github.com/maritaca-ai/capitu.git
cd capitu

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

### Requirements

- Python 3.12+
- Dependencies: `nltk`, `immutabledict`, `openai`, `tqdm`, `matplotlib`, `numpy`, `wandb`

### Verifying the installation

```bash
pip install pytest
python -m pytest instructions_test.py -v
```

## Quick Start

### 1. Generate prompts

```bash
# Single-turn: 200 prompts (70 easy, 70 medium, 60 hard)
python generate_questions.py \
    --output data/input_questions.jsonl \
    --easy 70 --medium 70 --hard 60

# Multi-turn: 100 conversations with 3 turns each
python generate_questions.py \
    --output data/input_questions_multiturn.jsonl \
    --multi_turn --turns 100
```

### 2. Generate model responses

```bash
python generate_responses.py \
    --model_name "sabiazinho-4" \
    --api_base "https://chat.maritaca.ai/api" \
    --api_key "$MARITACA_API_KEY" \
    --input_data data/input_questions.jsonl \
    --output_path runs/sabiazinho-4/single-turn/responses.jsonl \
    --parallel 5
```

The script accepts any OpenAI-compatible API (OpenAI, OpenRouter, Azure, vLLM, Ollama, etc.).

### 3. Evaluate

```bash
python run_eval.py \
    --input_data data/input_questions.jsonl \
    --input_response_data runs/sabiazinho-4/single-turn/responses.jsonl \
    --output_dir runs/sabiazinho-4/eval/single-turn \
    --book_context_path data/book_context.json
```

### 4. Evaluate with coherence scoring (optional)

```bash
python run_eval.py \
    --input_data data/input_questions.jsonl \
    --input_response_data runs/sabiazinho-4/single-turn/responses.jsonl \
    --output_dir runs/sabiazinho-4/eval/single-turn \
    --book_context_path data/book_context.json \
    --judge_model_name "gpt-4o-mini" \
    --judge_api_base "https://api.openai.com/v1" \
    --judge_api_key "$OPENAI_API_KEY"
```

Results are saved to the output directory as `metrics_report.json`, `metrics_report.md`, and per-prompt evaluation files.

## Evaluation Methodology

### Automatic verification

All 59 instruction types are **deterministically verifiable** using string operations, regular expressions, and curated lexicons. No LLM judges or human evaluators are required for instruction compliance verification.

### Evaluation modes

| Mode | Description |
|------|-------------|
| **Strict accuracy** | Prompt passes only if ALL instructions are satisfied on the original response |
| **Loose accuracy** | Tests response variants (first/last line removed, markdown stripped) to accommodate formatting artifacts |
| **Instruction-level accuracy** | Individual instruction satisfaction rate across all prompts |
| **Conversation accuracy** | Multi-turn: ALL turns must satisfy their accumulated constraints |

### Coherence evaluation (optional)

An LLM judge (e.g., GPT-4o-mini) scores factual coherence against literary metadata on a 0-1 scale. The combined score is computed as:

```
Final Score = (2 × Instruction Compliance + Coherence) / 3
```

This weighting prioritizes constraint satisfaction while penalizing degenerate solutions.

## Benchmark Design

### Instruction categories

| Category | Count | Examples |
|----------|:-----:|---------|
| **Count** | 17 | Word count range, exact sentence count, min paragraph count |
| **Words** | 11 | Include specific word, connectives, temporal markers |
| **Pattern** | 8 | Terminações -ando/-endo/-indo, -inho/-inha, -mente |
| **Forbidden** | 7 | No first person, no questions, forbidden word |
| **Structure** | 6 | Start/end with word, acrostic, no repeat sentence start |
| **Punctuation** | 5 | Include quote, use semicolon, only declarative |
| **Format** | 5 | Bullet list, numbered list, all caps, title case |
| **Total** | **59** | |

### Difficulty levels

| Level | Instructions per prompt | Single-turn prompts |
|-------|:-----------------------:|:-------------------:|
| Easy | 1 | 70 |
| Medium | 2 | 70 |
| Hard | 3-4 | 60 |

### Literary works

| Title | Author | Year | Movement |
|-------|--------|:----:|----------|
| Dom Casmurro | Machado de Assis | 1899 | Realism |
| O Cortiço | Aluísio Azevedo | 1890 | Naturalism |
| Iracema | José de Alencar | 1865 | Romanticism |
| Grande Sertão: Veredas | Guimarães Rosa | 1956 | Modernism |
| Macunaíma | Mário de Andrade | 1928 | Modernism |
| Vidas Secas | Graciliano Ramos | 1938 | Regionalism |
| Capitães da Areia | Jorge Amado | 1937 | Modernism |
| A Hora da Estrela | Clarice Lispector | 1977 | Modernism |

### Multi-turn evaluation

Multi-turn conversations consist of 3 progressive turns where each turn adds new instructions to the accumulated constraints from previous turns.

| Turn | New instructions | Cumulative |
|:----:|:----------------:|:----------:|
| 1 | 1-2 | 1-2 |
| 2 | 1-2 | 2-4 |
| 3 | 1-2 | 3-6 |

## Batch Evaluation

To evaluate all paper models at once:

```bash
# Configure API keys as environment variables
export OPENAI_API_KEY="..."
export OPENROUTER_API_KEY="..."
export MARITACA_API_KEY="..."

# Run all models (generate + evaluate)
bash run_paper_models.sh all

# Or run for a specific model
bash run_paper_models.sh all --model sabiazinho-4

# Re-run evaluation only (without regenerating responses)
bash rerun_eval.sh
```

## Project Structure

```
capitu/
├── data/
│   ├── input_questions.jsonl          # Single-turn prompts (200)
│   ├── input_questions_multiturn.jsonl # Multi-turn conversations (100)
│   └── book_context.json              # Literary metadata for the 8 works
├── configs/
│   └── judges/                        # Judge model configurations
├── models/
│   └── models.py                      # OpenAI-compatible API client
├── runs/                              # Experiment results per model
│
│  # Core pipeline
├── generate_questions.py              # Prompt generation with instruction sampling
├── generate_responses.py              # Model response generation via API
├── run_eval.py                        # Evaluation with strict/loose scoring
├── instructions.py                    # 59 instruction checker implementations
├── instructions_registry.py           # Instruction ID → checker class mapping
├── instructions_util.py               # Portuguese linguistic utilities
├── evaluation_lib.py                  # Evaluation orchestration and coherence scoring
├── metrics.py                         # Metric aggregation and reporting
│
│  # Analysis and integration
├── collect_results.py                 # Cross-model result aggregation
├── upload_to_wandb.py                 # Upload metrics to Weights & Biases
│
│  # Orchestration
├── run_paper_models.sh                # Run all 18 paper models
├── rerun_eval.sh                      # Re-evaluate existing responses
│
│  # Validation
├── sample_for_validation.py           # Sample cases for manual audit
├── generate_validation_reports.py     # Human review documents
├── instructions_test.py               # Unit tests for all checkers
│
└── requirements.txt                   # Python dependencies
```

## Data Format

### Single-turn prompt

```json
{
  "key": 0,
  "prompt": "Analise a construção do narrador em Dom Casmurro...",
  "instruction_id_list": ["count:word_count_range", "forbidden:no_first_person"],
  "kwargs": [{"min_words": 120, "max_words": 180}, {}],
  "difficulty": "medium",
  "book": "Dom Casmurro",
  "num_instructions": 2
}
```

### Multi-turn conversation

```json
{
  "key": 0,
  "is_multi_turn": true,
  "conversation_type": "expansion",
  "book": "Dom Casmurro",
  "turns": [
    {"turn": 1, "prompt": "...", "instruction_id_list": [...], "kwargs": [...]},
    {"turn": 2, "prompt": "...", "instruction_id_list": [...], "kwargs": [...]},
    {"turn": 3, "prompt": "...", "instruction_id_list": [...], "kwargs": [...]}
  ],
  "total_instructions": 6
}
```

## Comparison with Related Benchmarks

| Aspect | IFEval | IFBench | Multi-IF | **CAPITU** |
|--------|--------|---------|----------|------------|
| Language | English | English | 8 languages | **Brazilian Portuguese** |
| Domain | Generic | Generic | Generic | **Brazilian literature** |
| Instruction types | 25 | 58 | 25 | **59** |
| Turns | Single | Single+Multi | Multi (3) | **Single+Multi** |
| Verification | Automatic | Automatic | Automatic | **Automatic** |
| Cultural context | No | No | No | **8 literary works** |
| Morphological constraints | No | No | No | **Yes (PT-specific)** |

## Citation

```bibtex

```

## License

Based on [IFEval](https://github.com/google-research/google-research/tree/master/instruction_following_eval) by Google Research, adapted and extended for Brazilian Portuguese.

## References

- Zhou et al. (2023). [Instruction-Following Evaluation for Large Language Models](https://arxiv.org/abs/2311.07911). *arXiv:2311.07911*.
- Pyatkin et al. (2025). [IFBench: Generalizing Verifiable Instruction Following](https://arxiv.org/abs/2507.02833). *arXiv:2507.02833*.
- He et al. (2024). [Multi-IF: Benchmarking LLMs on Multi-Turn and Multilingual Instructions Following](https://arxiv.org/abs/2410.15553). *arXiv:2410.15553*.
