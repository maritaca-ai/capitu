# Relatório de Avaliação - Capitu

**Modelo:** sabia-3.1

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 64.00% (64/100) |
| Acurácia por Instrução | 91.67% (550/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 64 | 64.0% |
| Parcialmente corretos | 35 | 35.0% |
| 0% corretos | 1 | 1.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 66.7% | 2 | 60 |
| count | 83.8% | 3 | 148 |
| structure | 94.7% | 2 | 76 |
| forbidden | 99.2% | 3 | 121 |
| words | 99.4% | 4 | 159 |
| punctuation | 100.0% | 1 | 36 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `pattern:terminacao_ando_endo_indo_limit` | 54.5% |
| 2 | `count:word_count_range` | 63.6% |
| 3 | `pattern:terminacao_mente_limit` | 73.7% |
| 4 | `structure:no_repeat_sentence_start` | 78.9% |
| 5 | `words:temporal_marker` | 95.2% |
| 6 | `forbidden:no_first_person` | 95.5% |
| 7 | `structure:start_with_word` | 100.0% |
| 8 | `words:contrast_marker` | 100.0% |
| 9 | `forbidden:no_questions` | 100.0% |
| 10 | `words:connective` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `forbidden:word` | 100.0% |
| 2 | `punctuation:include_quote` | 100.0% |
| 3 | `count:min_word_count` | 100.0% |
| 4 | `count:min_paragraph_count` | 100.0% |
| 5 | `words:include_word` | 100.0% |
| 6 | `words:connective` | 100.0% |
| 7 | `forbidden:no_questions` | 100.0% |
| 8 | `words:contrast_marker` | 100.0% |
| 9 | `structure:start_with_word` | 100.0% |
| 10 | `forbidden:no_first_person` | 95.5% |

