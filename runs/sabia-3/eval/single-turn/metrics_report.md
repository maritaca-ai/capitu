# Relatório de Avaliação - Capitu

**Modelo:** sabia-3

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 77.00% (154/200) |
| Acurácia Flexível (prompt) | 81.00% |
| Acurácia por Instrução | 86.42% (350/405) |
| Pontuação Final | 0.9071 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 154 | 77.0% |
| Parcialmente corretos | 36 | 18.0% |
| 0% corretos | 10 | 5.0% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 88.6% | 88.6% | 70 |
| Medium | 81.4% | 90.0% | 70 |
| Hard | 58.3% | 83.1% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 68.6% | 7 | 70 |
| words | 83.9% | 7 | 56 |
| structure | 84.4% | 5 | 32 |
| count | 85.6% | 12 | 118 |
| punctuation | 90.0% | 3 | 10 |
| format | 96.8% | 5 | 31 |
| forbidden | 100.0% | 6 | 88 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| O Cortiço | 70.0% | 0.91 | 20 |
| A Hora da Estrela | 72.7% | 0.99 | 33 |
| Grande Sertão: Veredas | 73.1% | 1.00 | 26 |
| Vidas Secas | 73.1% | 0.97 | 26 |
| Dom Casmurro | 76.5% | 1.00 | 17 |
| Capitães da Areia | 81.8% | 0.99 | 22 |
| Iracema | 83.3% | 0.96 | 24 |
| Macunaíma | 84.4% | 0.95 | 32 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `words:max_word_repeat` | 0.0% |
| 3 | `pattern:terminacao_inho_inha_min` | 0.0% |
| 4 | `count:character_count_range` | 0.0% |
| 5 | `structure:start_end_same_word` | 33.3% |
| 6 | `structure:acrostic` | 40.0% |
| 7 | `words:word_frequency` | 50.0% |
| 8 | `pattern:terminacao_ando_endo_indo_limit` | 57.1% |
| 9 | `count:word_count_range` | 59.3% |
| 10 | `count:max_word_count` | 66.7% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `format:all_lowercase` | 100.0% |
| 2 | `structure:no_repeat_sentence_start` | 100.0% |
| 3 | `punctuation:include_quote` | 100.0% |
| 4 | `words:include_words` | 100.0% |
| 5 | `pattern:terminacao_mente_min` | 100.0% |
| 6 | `forbidden:words_list` | 100.0% |
| 7 | `format:all_caps` | 100.0% |
| 8 | `forbidden:no_numbers` | 100.0% |
| 9 | `structure:end_with_word` | 100.0% |
| 10 | `format:title_case_start` | 100.0% |

## Métricas de Coerência

| Métrica | Valor |
|---------|-------|
| Média | 0.9705 |
| Mínimo | 0.3097 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.1037 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 235.1 |
| Palavras únicas (média) | 147.4 |
| Diversidade vocabular | 62.70% |
| Frases (média) | 10.1 |
| Palavras por frase | 23.3 |

