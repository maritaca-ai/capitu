# Relatório de Avaliação - Capitu

**Modelo:** sabia-3.1

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 74.00% (148/200) |
| Acurácia Flexível (prompt) | 79.50% |
| Acurácia por Instrução | 85.43% (346/405) |
| Pontuação Final | 0.8922 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 148 | 74.0% |
| Parcialmente corretos | 45 | 22.5% |
| 0% corretos | 7 | 3.5% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 90.0% | 90.0% | 70 |
| Medium | 75.7% | 87.9% | 70 |
| Hard | 53.3% | 82.1% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 72.9% | 7 | 70 |
| structure | 75.0% | 5 | 32 |
| count | 82.2% | 12 | 118 |
| words | 89.3% | 7 | 56 |
| format | 90.3% | 5 | 31 |
| forbidden | 97.7% | 6 | 88 |
| punctuation | 100.0% | 3 | 10 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| Dom Casmurro | 52.9% | 0.93 | 17 |
| O Cortiço | 60.0% | 0.86 | 20 |
| Vidas Secas | 69.2% | 0.94 | 26 |
| A Hora da Estrela | 72.7% | 0.97 | 33 |
| Grande Sertão: Veredas | 76.9% | 0.98 | 26 |
| Capitães da Areia | 77.3% | 0.96 | 22 |
| Macunaíma | 81.2% | 0.90 | 32 |
| Iracema | 91.7% | 0.94 | 24 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `words:max_word_repeat` | 0.0% |
| 3 | `structure:acrostic` | 20.0% |
| 4 | `count:max_word_count` | 33.3% |
| 5 | `structure:start_end_same_word` | 33.3% |
| 6 | `pattern:terminacao_inho_inha_min` | 37.5% |
| 7 | `count:word_count_range` | 48.1% |
| 8 | `count:character_count_range` | 50.0% |
| 9 | `pattern:terminacao_mente_limit` | 60.0% |
| 10 | `structure:no_repeat_sentence_start` | 66.7% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `format:all_lowercase` | 100.0% |
| 2 | `punctuation:include_quote` | 100.0% |
| 3 | `words:include_words` | 100.0% |
| 4 | `pattern:terminacao_mente_min` | 100.0% |
| 5 | `forbidden:words_list` | 100.0% |
| 6 | `format:all_caps` | 100.0% |
| 7 | `forbidden:no_numbers` | 100.0% |
| 8 | `format:title_case_start` | 100.0% |
| 9 | `words:word_frequency` | 100.0% |
| 10 | `count:exact_sentence_count` | 100.0% |

## Métricas de Coerência

| Métrica | Valor |
|---------|-------|
| Média | 0.9374 |
| Mínimo | 0.1069 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.1623 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 205.1 |
| Palavras únicas (média) | 131.9 |
| Diversidade vocabular | 64.29% |
| Frases (média) | 9.4 |
| Palavras por frase | 21.7 |

