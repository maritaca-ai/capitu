# Relatório de Avaliação - Capitu

**Modelo:** anthropic/claude-haiku-4.5

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 72.00% (72/100) |
| Acurácia por Instrução | 90.17% (541/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 72 | 72.0% |
| Parcialmente corretos | 17 | 17.0% |
| 0% corretos | 11 | 11.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| structure | 67.1% | 2 | 76 |
| pattern | 76.7% | 2 | 60 |
| count | 87.8% | 3 | 148 |
| punctuation | 97.2% | 1 | 36 |
| words | 99.4% | 4 | 159 |
| forbidden | 100.0% | 3 | 121 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `structure:start_with_word` | 57.9% |
| 2 | `count:word_count_range` | 72.7% |
| 3 | `pattern:terminacao_mente_limit` | 73.7% |
| 4 | `pattern:terminacao_ando_endo_indo_limit` | 81.8% |
| 5 | `structure:no_repeat_sentence_start` | 94.7% |
| 6 | `words:connective` | 97.2% |
| 7 | `punctuation:include_quote` | 97.2% |
| 8 | `words:contrast_marker` | 100.0% |
| 9 | `forbidden:no_questions` | 100.0% |
| 10 | `words:include_word` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `forbidden:word` | 100.0% |
| 2 | `forbidden:no_first_person` | 100.0% |
| 3 | `words:temporal_marker` | 100.0% |
| 4 | `count:min_word_count` | 100.0% |
| 5 | `count:min_paragraph_count` | 100.0% |
| 6 | `words:include_word` | 100.0% |
| 7 | `forbidden:no_questions` | 100.0% |
| 8 | `words:contrast_marker` | 100.0% |
| 9 | `punctuation:include_quote` | 97.2% |
| 10 | `words:connective` | 97.2% |

