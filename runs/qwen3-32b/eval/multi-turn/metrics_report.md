# Relatório de Avaliação - Capitu

**Modelo:** qwen/qwen3-32b

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 60.00% (60/100) |
| Acurácia por Instrução | 91.00% (546/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 60 | 60.0% |
| Parcialmente corretos | 39 | 39.0% |
| 0% corretos | 1 | 1.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| count | 81.1% | 3 | 148 |
| pattern | 81.7% | 2 | 60 |
| punctuation | 91.7% | 1 | 36 |
| structure | 93.4% | 2 | 76 |
| words | 95.6% | 4 | 159 |
| forbidden | 100.0% | 3 | 121 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:word_count_range` | 63.6% |
| 2 | `pattern:terminacao_mente_limit` | 73.7% |
| 3 | `structure:no_repeat_sentence_start` | 78.9% |
| 4 | `words:connective` | 91.7% |
| 5 | `punctuation:include_quote` | 91.7% |
| 6 | `count:min_word_count` | 93.9% |
| 7 | `words:include_word` | 95.2% |
| 8 | `words:temporal_marker` | 95.2% |
| 9 | `pattern:terminacao_ando_endo_indo_limit` | 95.5% |
| 10 | `structure:start_with_word` | 98.2% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `forbidden:word` | 100.0% |
| 2 | `forbidden:no_first_person` | 100.0% |
| 3 | `count:min_paragraph_count` | 100.0% |
| 4 | `forbidden:no_questions` | 100.0% |
| 5 | `words:contrast_marker` | 98.3% |
| 6 | `structure:start_with_word` | 98.2% |
| 7 | `pattern:terminacao_ando_endo_indo_limit` | 95.5% |
| 8 | `words:temporal_marker` | 95.2% |
| 9 | `words:include_word` | 95.2% |
| 10 | `count:min_word_count` | 93.9% |

