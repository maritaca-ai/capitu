# Relatório de Avaliação - Capitu

**Modelo:** qwen/qwen3-235b-a22b-2507

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 60.00% (60/100) |
| Acurácia por Instrução | 90.33% (542/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 60 | 60.0% |
| Parcialmente corretos | 38 | 38.0% |
| 0% corretos | 2 | 2.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 61.7% | 2 | 60 |
| count | 86.5% | 3 | 148 |
| structure | 88.2% | 2 | 76 |
| punctuation | 88.9% | 1 | 36 |
| forbidden | 98.3% | 3 | 121 |
| words | 100.0% | 4 | 159 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `pattern:terminacao_ando_endo_indo_limit` | 50.0% |
| 2 | `structure:no_repeat_sentence_start` | 57.9% |
| 3 | `pattern:terminacao_mente_limit` | 68.4% |
| 4 | `count:word_count_range` | 71.2% |
| 5 | `punctuation:include_quote` | 88.9% |
| 6 | `count:min_paragraph_count` | 93.8% |
| 7 | `forbidden:no_first_person` | 95.5% |
| 8 | `forbidden:word` | 96.7% |
| 9 | `structure:start_with_word` | 98.2% |
| 10 | `words:contrast_marker` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `words:temporal_marker` | 100.0% |
| 2 | `count:min_word_count` | 100.0% |
| 3 | `words:include_word` | 100.0% |
| 4 | `words:connective` | 100.0% |
| 5 | `forbidden:no_questions` | 100.0% |
| 6 | `words:contrast_marker` | 100.0% |
| 7 | `structure:start_with_word` | 98.2% |
| 8 | `forbidden:word` | 96.7% |
| 9 | `forbidden:no_first_person` | 95.5% |
| 10 | `count:min_paragraph_count` | 93.8% |

