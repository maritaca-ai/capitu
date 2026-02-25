# Relatório de Avaliação - Capitu

**Modelo:** qwen/qwen3-14b

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 74.00% (74/100) |
| Acurácia por Instrução | 94.00% (564/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 74 | 74.0% |
| Parcialmente corretos | 25 | 25.0% |
| 0% corretos | 1 | 1.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 85.0% | 2 | 60 |
| count | 87.8% | 3 | 148 |
| punctuation | 91.7% | 1 | 36 |
| structure | 96.1% | 2 | 76 |
| words | 98.1% | 4 | 159 |
| forbidden | 100.0% | 3 | 121 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:word_count_range` | 75.8% |
| 2 | `structure:no_repeat_sentence_start` | 84.2% |
| 3 | `pattern:terminacao_mente_limit` | 84.2% |
| 4 | `pattern:terminacao_ando_endo_indo_limit` | 86.4% |
| 5 | `count:min_paragraph_count` | 87.5% |
| 6 | `words:connective` | 91.7% |
| 7 | `punctuation:include_quote` | 91.7% |
| 8 | `structure:start_with_word` | 100.0% |
| 9 | `words:contrast_marker` | 100.0% |
| 10 | `forbidden:no_questions` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `forbidden:word` | 100.0% |
| 2 | `forbidden:no_first_person` | 100.0% |
| 3 | `words:temporal_marker` | 100.0% |
| 4 | `count:min_word_count` | 100.0% |
| 5 | `words:include_word` | 100.0% |
| 6 | `forbidden:no_questions` | 100.0% |
| 7 | `words:contrast_marker` | 100.0% |
| 8 | `structure:start_with_word` | 100.0% |
| 9 | `punctuation:include_quote` | 91.7% |
| 10 | `words:connective` | 91.7% |

