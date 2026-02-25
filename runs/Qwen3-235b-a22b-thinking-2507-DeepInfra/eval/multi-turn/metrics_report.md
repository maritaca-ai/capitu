# Relatório de Avaliação - Capitu

**Modelo:** qwen/qwen3-235b-a22b-thinking-2507

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 64.00% (64/100) |
| Acurácia por Instrução | 90.17% (541/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 64 | 64.0% |
| Parcialmente corretos | 30 | 30.0% |
| 0% corretos | 6 | 6.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 68.3% | 2 | 60 |
| count | 77.0% | 3 | 148 |
| punctuation | 97.2% | 1 | 36 |
| structure | 97.4% | 2 | 76 |
| forbidden | 98.3% | 3 | 121 |
| words | 99.4% | 4 | 159 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:word_count_range` | 48.5% |
| 2 | `pattern:terminacao_ando_endo_indo_limit` | 63.6% |
| 3 | `pattern:terminacao_mente_limit` | 71.1% |
| 4 | `structure:no_repeat_sentence_start` | 89.5% |
| 5 | `words:temporal_marker` | 95.2% |
| 6 | `forbidden:word` | 96.7% |
| 7 | `punctuation:include_quote` | 97.2% |
| 8 | `forbidden:no_questions` | 98.6% |
| 9 | `structure:start_with_word` | 100.0% |
| 10 | `words:contrast_marker` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `forbidden:no_first_person` | 100.0% |
| 2 | `count:min_word_count` | 100.0% |
| 3 | `count:min_paragraph_count` | 100.0% |
| 4 | `words:include_word` | 100.0% |
| 5 | `words:connective` | 100.0% |
| 6 | `words:contrast_marker` | 100.0% |
| 7 | `structure:start_with_word` | 100.0% |
| 8 | `forbidden:no_questions` | 98.6% |
| 9 | `punctuation:include_quote` | 97.2% |
| 10 | `forbidden:word` | 96.7% |

