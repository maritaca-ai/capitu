# Relatório de Avaliação - Capitu

**Modelo:** gpt-5-mini

**Dataset:** data/input_questions_multiturn.jsonl

**Modo:** Multi-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 96.00% (96/100) |
| Acurácia por Instrução | 99.33% (596/600) |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 96 | 96.0% |
| Parcialmente corretos | 4 | 4.0% |
| 0% corretos | 0 | 0.0% |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| punctuation | 97.2% | 1 | 36 |
| pattern | 98.3% | 2 | 60 |
| count | 99.3% | 3 | 148 |
| words | 99.4% | 4 | 159 |
| structure | 100.0% | 2 | 76 |
| forbidden | 100.0% | 3 | 121 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `pattern:terminacao_ando_endo_indo_limit` | 95.5% |
| 2 | `punctuation:include_quote` | 97.2% |
| 3 | `words:contrast_marker` | 98.3% |
| 4 | `count:word_count_range` | 98.5% |
| 5 | `structure:start_with_word` | 100.0% |
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
| 3 | `forbidden:no_first_person` | 100.0% |
| 4 | `structure:no_repeat_sentence_start` | 100.0% |
| 5 | `words:temporal_marker` | 100.0% |
| 6 | `count:min_word_count` | 100.0% |
| 7 | `count:min_paragraph_count` | 100.0% |
| 8 | `words:include_word` | 100.0% |
| 9 | `words:connective` | 100.0% |
| 10 | `forbidden:no_questions` | 100.0% |

