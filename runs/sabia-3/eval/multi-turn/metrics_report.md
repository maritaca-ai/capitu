# Relatório de Avaliação - Capitu

**Modelo:** sabia-3

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 64.00% (64/100) |
| Acurácia por Instrução | 92.00% (552/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 64 | 64.0% |
| Parcialmente corretos | 35 | 35.0% |
| 0% corretos | 1 | 1.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 76.7% | 2 | 60 |
| count | 85.1% | 3 | 148 |
| structure | 89.5% | 2 | 76 |
| words | 98.1% | 4 | 159 |
| forbidden | 99.2% | 3 | 121 |
| punctuation | 100.0% | 1 | 36 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `structure:no_repeat_sentence_start` | 57.9% |
| 2 | `count:word_count_range` | 66.7% |
| 3 | `pattern:terminacao_ando_endo_indo_limit` | 68.2% |
| 4 | `pattern:terminacao_mente_limit` | 81.6% |
| 5 | `words:connective` | 91.7% |
| 6 | `forbidden:no_questions` | 98.6% |
| 7 | `structure:start_with_word` | 100.0% |
| 8 | `words:contrast_marker` | 100.0% |
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
| 8 | `words:contrast_marker` | 100.0% |
| 9 | `structure:start_with_word` | 100.0% |
| 10 | `forbidden:no_questions` | 98.6% |

