# Relatório de Avaliação - Capitu

**Modelo:** gpt-5.2

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 73.00% (73/100) |
| Acurácia por Instrução | 92.00% (552/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 73 | 73.0% |
| Parcialmente corretos | 25 | 25.0% |
| 0% corretos | 2 | 2.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| punctuation | 25.0% | 1 | 36 |
| count | 86.5% | 3 | 148 |
| forbidden | 99.2% | 3 | 121 |
| structure | 100.0% | 2 | 76 |
| words | 100.0% | 4 | 159 |
| pattern | 100.0% | 2 | 60 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `punctuation:include_quote` | 25.0% |
| 2 | `count:word_count_range` | 72.7% |
| 3 | `forbidden:no_first_person` | 95.5% |
| 4 | `count:min_word_count` | 97.0% |
| 5 | `structure:start_with_word` | 100.0% |
| 6 | `words:contrast_marker` | 100.0% |
| 7 | `pattern:terminacao_ando_endo_indo_limit` | 100.0% |
| 8 | `forbidden:no_questions` | 100.0% |
| 9 | `words:connective` | 100.0% |
| 10 | `words:include_word` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `pattern:terminacao_mente_limit` | 100.0% |
| 2 | `forbidden:word` | 100.0% |
| 3 | `structure:no_repeat_sentence_start` | 100.0% |
| 4 | `words:temporal_marker` | 100.0% |
| 5 | `count:min_paragraph_count` | 100.0% |
| 6 | `words:include_word` | 100.0% |
| 7 | `words:connective` | 100.0% |
| 8 | `forbidden:no_questions` | 100.0% |
| 9 | `pattern:terminacao_ando_endo_indo_limit` | 100.0% |
| 10 | `words:contrast_marker` | 100.0% |

