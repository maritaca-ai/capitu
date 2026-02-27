# Relatório de Avaliação - Capitu

**Modelo:** gpt-5

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 90.00% (90/100) |
| Acurácia por Instrução | 98.00% (588/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 90 | 90.0% |
| Parcialmente corretos | 10 | 10.0% |
| 0% corretos | 0 | 0.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| punctuation | 69.4% | 1 | 36 |
| forbidden | 99.2% | 3 | 121 |
| structure | 100.0% | 2 | 76 |
| words | 100.0% | 4 | 159 |
| pattern | 100.0% | 2 | 60 |
| count | 100.0% | 3 | 148 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `punctuation:include_quote` | 69.4% |
| 2 | `forbidden:no_first_person` | 95.5% |
| 3 | `structure:start_with_word` | 100.0% |
| 4 | `words:contrast_marker` | 100.0% |
| 5 | `pattern:terminacao_ando_endo_indo_limit` | 100.0% |
| 6 | `forbidden:no_questions` | 100.0% |
| 7 | `words:connective` | 100.0% |
| 8 | `words:include_word` | 100.0% |
| 9 | `count:min_paragraph_count` | 100.0% |
| 10 | `count:min_word_count` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `pattern:terminacao_mente_limit` | 100.0% |
| 2 | `forbidden:word` | 100.0% |
| 3 | `count:word_count_range` | 100.0% |
| 4 | `structure:no_repeat_sentence_start` | 100.0% |
| 5 | `words:temporal_marker` | 100.0% |
| 6 | `count:min_word_count` | 100.0% |
| 7 | `count:min_paragraph_count` | 100.0% |
| 8 | `words:include_word` | 100.0% |
| 9 | `words:connective` | 100.0% |
| 10 | `forbidden:no_questions` | 100.0% |

