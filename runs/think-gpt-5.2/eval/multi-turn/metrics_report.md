# Relatório de Avaliação - Capitu

**Modelo:** gpt-5.2

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 83.00% (83/100) |
| Acurácia por Instrução | 94.50% (567/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 83 | 83.0% |
| Parcialmente corretos | 16 | 16.0% |
| 0% corretos | 1 | 1.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| punctuation | 16.7% | 1 | 36 |
| count | 98.0% | 3 | 148 |
| structure | 100.0% | 2 | 76 |
| words | 100.0% | 4 | 159 |
| pattern | 100.0% | 2 | 60 |
| forbidden | 100.0% | 3 | 121 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `punctuation:include_quote` | 16.7% |
| 2 | `count:word_count_range` | 97.0% |
| 3 | `count:min_word_count` | 98.5% |
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
| 1 | `pattern:terminacao_mente_limit` | 100.0% |
| 2 | `forbidden:word` | 100.0% |
| 3 | `forbidden:no_first_person` | 100.0% |
| 4 | `structure:no_repeat_sentence_start` | 100.0% |
| 5 | `words:temporal_marker` | 100.0% |
| 6 | `count:min_paragraph_count` | 100.0% |
| 7 | `words:include_word` | 100.0% |
| 8 | `words:connective` | 100.0% |
| 9 | `forbidden:no_questions` | 100.0% |
| 10 | `pattern:terminacao_ando_endo_indo_limit` | 100.0% |

