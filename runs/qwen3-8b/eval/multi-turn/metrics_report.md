# Relatório de Avaliação - Capitu

**Modelo:** qwen/qwen3-8b

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 72.00% (72/100) |
| Acurácia por Instrução | 93.83% (563/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 72 | 72.0% |
| Parcialmente corretos | 28 | 28.0% |
| 0% corretos | 0 | 0.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| count | 85.1% | 3 | 148 |
| pattern | 90.0% | 2 | 60 |
| punctuation | 94.4% | 1 | 36 |
| structure | 96.1% | 2 | 76 |
| forbidden | 98.3% | 3 | 121 |
| words | 98.7% | 4 | 159 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:word_count_range` | 68.2% |
| 2 | `pattern:terminacao_ando_endo_indo_limit` | 81.8% |
| 3 | `structure:no_repeat_sentence_start` | 84.2% |
| 4 | `punctuation:include_quote` | 94.4% |
| 5 | `pattern:terminacao_mente_limit` | 94.7% |
| 6 | `words:temporal_marker` | 95.2% |
| 7 | `forbidden:no_first_person` | 95.5% |
| 8 | `words:connective` | 97.2% |
| 9 | `count:min_word_count` | 98.5% |
| 10 | `forbidden:no_questions` | 98.6% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `forbidden:word` | 100.0% |
| 2 | `count:min_paragraph_count` | 100.0% |
| 3 | `words:include_word` | 100.0% |
| 4 | `words:contrast_marker` | 100.0% |
| 5 | `structure:start_with_word` | 100.0% |
| 6 | `forbidden:no_questions` | 98.6% |
| 7 | `count:min_word_count` | 98.5% |
| 8 | `words:connective` | 97.2% |
| 9 | `forbidden:no_first_person` | 95.5% |
| 10 | `words:temporal_marker` | 95.2% |

