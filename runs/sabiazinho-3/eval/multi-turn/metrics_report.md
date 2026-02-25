# Relatório de Avaliação - Capitu

**Modelo:** sabiazinho-3

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 68.00% (68/100) |
| Acurácia por Instrução | 92.83% (557/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 68 | 68.0% |
| Parcialmente corretos | 31 | 31.0% |
| 0% corretos | 1 | 1.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 71.7% | 2 | 60 |
| count | 87.2% | 3 | 148 |
| words | 96.9% | 4 | 159 |
| structure | 98.7% | 2 | 76 |
| forbidden | 99.2% | 3 | 121 |
| punctuation | 100.0% | 1 | 36 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `pattern:terminacao_mente_limit` | 68.4% |
| 2 | `pattern:terminacao_ando_endo_indo_limit` | 77.3% |
| 3 | `count:word_count_range` | 77.3% |
| 4 | `count:min_paragraph_count` | 81.2% |
| 5 | `words:connective` | 86.1% |
| 6 | `structure:no_repeat_sentence_start` | 94.7% |
| 7 | `forbidden:no_first_person` | 95.5% |
| 8 | `count:min_word_count` | 98.5% |
| 9 | `structure:start_with_word` | 100.0% |
| 10 | `words:contrast_marker` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `forbidden:word` | 100.0% |
| 2 | `punctuation:include_quote` | 100.0% |
| 3 | `words:temporal_marker` | 100.0% |
| 4 | `words:include_word` | 100.0% |
| 5 | `forbidden:no_questions` | 100.0% |
| 6 | `words:contrast_marker` | 100.0% |
| 7 | `structure:start_with_word` | 100.0% |
| 8 | `count:min_word_count` | 98.5% |
| 9 | `forbidden:no_first_person` | 95.5% |
| 10 | `structure:no_repeat_sentence_start` | 94.7% |

