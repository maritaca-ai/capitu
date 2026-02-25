# Relatório de Avaliação - Capitu

**Modelo:** google/gemini-3-pro-preview

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 95.00% (95/100) |
| Acurácia por Instrução | 99.17% (595/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 95 | 95.0% |
| Parcialmente corretos | 5 | 5.0% |
| 0% corretos | 0 | 0.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| words | 97.5% | 4 | 159 |
| pattern | 98.3% | 2 | 60 |
| structure | 100.0% | 2 | 76 |
| forbidden | 100.0% | 3 | 121 |
| count | 100.0% | 3 | 148 |
| punctuation | 100.0% | 1 | 36 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `words:connective` | 91.7% |
| 2 | `words:temporal_marker` | 95.2% |
| 3 | `pattern:terminacao_ando_endo_indo_limit` | 95.5% |
| 4 | `structure:start_with_word` | 100.0% |
| 5 | `words:contrast_marker` | 100.0% |
| 6 | `forbidden:no_questions` | 100.0% |
| 7 | `words:include_word` | 100.0% |
| 8 | `count:min_paragraph_count` | 100.0% |
| 9 | `count:min_word_count` | 100.0% |
| 10 | `punctuation:include_quote` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `pattern:terminacao_mente_limit` | 100.0% |
| 2 | `forbidden:word` | 100.0% |
| 3 | `count:word_count_range` | 100.0% |
| 4 | `forbidden:no_first_person` | 100.0% |
| 5 | `structure:no_repeat_sentence_start` | 100.0% |
| 6 | `punctuation:include_quote` | 100.0% |
| 7 | `count:min_word_count` | 100.0% |
| 8 | `count:min_paragraph_count` | 100.0% |
| 9 | `words:include_word` | 100.0% |
| 10 | `forbidden:no_questions` | 100.0% |

