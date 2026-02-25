# Relatório de Avaliação - Capitu

**Modelo:** sabiazinho-3

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 80.00% (160/200) |
| Acurácia Flexível (prompt) | 80.00% |
| Acurácia por Instrução | 87.41% (354/405) |
| Pontuação Final | 0.9023 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 160 | 80.0% |
| Parcialmente corretos | 33 | 16.5% |
| 0% corretos | 7 | 3.5% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 94.3% | 94.3% | 70 |
| Medium | 82.9% | 90.0% | 70 |
| Hard | 60.0% | 83.1% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 78.6% | 7 | 70 |
| count | 83.1% | 12 | 118 |
| words | 83.9% | 7 | 56 |
| structure | 87.5% | 5 | 32 |
| format | 96.8% | 5 | 31 |
| forbidden | 97.7% | 6 | 88 |
| punctuation | 100.0% | 3 | 10 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| O Cortiço | 65.0% | 0.82 | 20 |
| Dom Casmurro | 70.6% | 0.89 | 17 |
| A Hora da Estrela | 75.8% | 0.96 | 33 |
| Vidas Secas | 76.9% | 0.92 | 26 |
| Capitães da Areia | 77.3% | 0.95 | 22 |
| Grande Sertão: Veredas | 84.6% | 0.97 | 26 |
| Iracema | 87.5% | 0.90 | 24 |
| Macunaíma | 93.8% | 0.88 | 32 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `words:max_word_repeat` | 0.0% |
| 3 | `pattern:terminacao_inho_inha_min` | 37.5% |
| 4 | `structure:acrostic` | 40.0% |
| 5 | `words:word_frequency` | 50.0% |
| 6 | `count:exact_line_count` | 60.0% |
| 7 | `count:word_count_range` | 63.0% |
| 8 | `pattern:terminacao_ando_endo_indo_limit` | 64.3% |
| 9 | `structure:start_end_same_word` | 66.7% |
| 10 | `pattern:terminacao_mente_limit` | 80.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `format:all_lowercase` | 100.0% |
| 2 | `structure:no_repeat_sentence_start` | 100.0% |
| 3 | `count:character_count_range` | 100.0% |
| 4 | `punctuation:include_quote` | 100.0% |
| 5 | `words:include_words` | 100.0% |
| 6 | `pattern:terminacao_mente_min` | 100.0% |
| 7 | `forbidden:words_list` | 100.0% |
| 8 | `format:all_caps` | 100.0% |
| 9 | `structure:end_with_word` | 100.0% |
| 10 | `format:title_case_start` | 100.0% |

## Métricas de Coerência

| Métrica | Valor |
|---------|-------|
| Média | 0.9168 |
| Mínimo | 0.0292 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.1901 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 177.3 |
| Palavras únicas (média) | 116.9 |
| Diversidade vocabular | 65.90% |
| Frases (média) | 7.9 |
| Palavras por frase | 22.4 |

