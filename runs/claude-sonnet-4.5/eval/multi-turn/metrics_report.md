# Relatório de Avaliação - Capitu

**Modelo:** anthropic/claude-sonnet-4.5

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 87.00% (87/100) |
| Acurácia por Instrução | 95.83% (575/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 87 | 87.0% |
| Parcialmente corretos | 9 | 9.0% |
| 0% corretos | 4 | 4.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 83.3% | 2 | 60 |
| structure | 84.2% | 2 | 76 |
| count | 98.0% | 3 | 148 |
| words | 100.0% | 4 | 159 |
| forbidden | 100.0% | 3 | 121 |
| punctuation | 100.0% | 1 | 36 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `pattern:terminacao_mente_limit` | 76.3% |
| 2 | `structure:start_with_word` | 78.9% |
| 3 | `pattern:terminacao_ando_endo_indo_limit` | 95.5% |
| 4 | `count:word_count_range` | 95.5% |
| 5 | `words:contrast_marker` | 100.0% |
| 6 | `forbidden:no_questions` | 100.0% |
| 7 | `words:connective` | 100.0% |
| 8 | `words:include_word` | 100.0% |
| 9 | `count:min_paragraph_count` | 100.0% |
| 10 | `count:min_word_count` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `forbidden:word` | 100.0% |
| 2 | `forbidden:no_first_person` | 100.0% |
| 3 | `structure:no_repeat_sentence_start` | 100.0% |
| 4 | `punctuation:include_quote` | 100.0% |
| 5 | `words:temporal_marker` | 100.0% |
| 6 | `count:min_word_count` | 100.0% |
| 7 | `count:min_paragraph_count` | 100.0% |
| 8 | `words:include_word` | 100.0% |
| 9 | `words:connective` | 100.0% |
| 10 | `forbidden:no_questions` | 100.0% |

