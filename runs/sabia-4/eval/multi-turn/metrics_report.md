# Relatório de Avaliação - Capitu

**Modelo:** sabia-4

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 78.00% (78/100) |
| Acurácia por Instrução | 94.17% (565/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 78 | 78.0% |
| Parcialmente corretos | 18 | 18.0% |
| 0% corretos | 4 | 4.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| count | 83.1% | 3 | 148 |
| pattern | 90.0% | 2 | 60 |
| punctuation | 91.7% | 1 | 36 |
| structure | 98.7% | 2 | 76 |
| words | 100.0% | 4 | 159 |
| forbidden | 100.0% | 3 | 121 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:word_count_range` | 63.6% |
| 2 | `pattern:terminacao_ando_endo_indo_limit` | 72.7% |
| 3 | `punctuation:include_quote` | 91.7% |
| 4 | `count:min_paragraph_count` | 93.8% |
| 5 | `structure:no_repeat_sentence_start` | 94.7% |
| 6 | `structure:start_with_word` | 100.0% |
| 7 | `words:contrast_marker` | 100.0% |
| 8 | `forbidden:no_questions` | 100.0% |
| 9 | `words:connective` | 100.0% |
| 10 | `words:include_word` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `pattern:terminacao_mente_limit` | 100.0% |
| 2 | `forbidden:word` | 100.0% |
| 3 | `forbidden:no_first_person` | 100.0% |
| 4 | `words:temporal_marker` | 100.0% |
| 5 | `count:min_word_count` | 100.0% |
| 6 | `words:include_word` | 100.0% |
| 7 | `words:connective` | 100.0% |
| 8 | `forbidden:no_questions` | 100.0% |
| 9 | `words:contrast_marker` | 100.0% |
| 10 | `structure:start_with_word` | 100.0% |

