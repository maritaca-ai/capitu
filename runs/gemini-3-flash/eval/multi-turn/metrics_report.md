# Relatório de Avaliação - Capitu

**Modelo:** google/gemini-3-flash-preview

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 95.00% (95/100) |
| Acurácia por Instrução | 99.00% (594/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 95 | 95.0% |
| Parcialmente corretos | 5 | 5.0% |
| 0% corretos | 0 | 0.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 93.3% | 2 | 60 |
| forbidden | 99.2% | 3 | 121 |
| count | 99.3% | 3 | 148 |
| structure | 100.0% | 2 | 76 |
| words | 100.0% | 4 | 159 |
| punctuation | 100.0% | 1 | 36 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `pattern:terminacao_mente_limit` | 89.5% |
| 2 | `forbidden:no_first_person` | 95.5% |
| 3 | `count:word_count_range` | 98.5% |
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
| 2 | `structure:no_repeat_sentence_start` | 100.0% |
| 3 | `punctuation:include_quote` | 100.0% |
| 4 | `words:temporal_marker` | 100.0% |
| 5 | `count:min_word_count` | 100.0% |
| 6 | `count:min_paragraph_count` | 100.0% |
| 7 | `words:include_word` | 100.0% |
| 8 | `words:connective` | 100.0% |
| 9 | `forbidden:no_questions` | 100.0% |
| 10 | `pattern:terminacao_ando_endo_indo_limit` | 100.0% |

