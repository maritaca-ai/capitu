# Relatório de Avaliação - Capitu

**Modelo:** sabiazinho-4

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 87.00% (87/100) |
| Acurácia por Instrução | 96.83% (581/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 87 | 87.0% |
| Parcialmente corretos | 12 | 12.0% |
| 0% corretos | 1 | 1.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| count | 90.5% | 3 | 148 |
| structure | 96.1% | 2 | 76 |
| pattern | 96.7% | 2 | 60 |
| words | 100.0% | 4 | 159 |
| forbidden | 100.0% | 3 | 121 |
| punctuation | 100.0% | 1 | 36 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:word_count_range` | 78.8% |
| 2 | `structure:no_repeat_sentence_start` | 84.2% |
| 3 | `pattern:terminacao_mente_limit` | 94.7% |
| 4 | `structure:start_with_word` | 100.0% |
| 5 | `words:contrast_marker` | 100.0% |
| 6 | `pattern:terminacao_ando_endo_indo_limit` | 100.0% |
| 7 | `forbidden:no_questions` | 100.0% |
| 8 | `words:connective` | 100.0% |
| 9 | `words:include_word` | 100.0% |
| 10 | `count:min_paragraph_count` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `forbidden:word` | 100.0% |
| 2 | `forbidden:no_first_person` | 100.0% |
| 3 | `punctuation:include_quote` | 100.0% |
| 4 | `words:temporal_marker` | 100.0% |
| 5 | `count:min_word_count` | 100.0% |
| 6 | `count:min_paragraph_count` | 100.0% |
| 7 | `words:include_word` | 100.0% |
| 8 | `words:connective` | 100.0% |
| 9 | `forbidden:no_questions` | 100.0% |
| 10 | `pattern:terminacao_ando_endo_indo_limit` | 100.0% |

