# Relatório de Avaliação - Capitu

**Modelo:** sabia-4

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 84.50% (169/200) |
| Acurácia Flexível (prompt) | 83.50% |
| Acurácia por Instrução | 91.60% (371/405) |
| Pontuação Final | 0.9435 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 169 | 84.5% |
| Parcialmente corretos | 30 | 15.0% |
| 0% corretos | 1 | 0.5% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 98.6% | 98.6% | 70 |
| Medium | 85.7% | 92.9% | 70 |
| Hard | 66.7% | 88.2% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| count | 84.7% | 12 | 118 |
| words | 89.3% | 7 | 56 |
| pattern | 90.0% | 7 | 70 |
| punctuation | 90.0% | 3 | 10 |
| format | 96.8% | 5 | 31 |
| structure | 96.9% | 5 | 32 |
| forbidden | 100.0% | 6 | 88 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| Grande Sertão: Veredas | 76.9% | 0.99 | 26 |
| Iracema | 83.3% | 0.94 | 24 |
| Macunaíma | 84.4% | 0.94 | 32 |
| Vidas Secas | 84.6% | 0.96 | 26 |
| A Hora da Estrela | 84.8% | 0.99 | 33 |
| O Cortiço | 85.0% | 0.90 | 20 |
| Dom Casmurro | 88.2% | 1.00 | 17 |
| Capitães da Areia | 90.9% | 0.97 | 22 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `words:max_word_repeat` | 0.0% |
| 3 | `pattern:terminacao_inho_inha_min` | 37.5% |
| 4 | `count:word_count_range` | 48.1% |
| 5 | `words:word_frequency` | 50.0% |
| 6 | `punctuation:include_quote` | 50.0% |
| 7 | `structure:no_repeat_sentence_start` | 66.7% |
| 8 | `count:exact_line_count` | 80.0% |
| 9 | `pattern:terminacao_ando_endo_indo_limit` | 85.7% |
| 10 | `format:bullet_list` | 94.4% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `format:all_lowercase` | 100.0% |
| 2 | `structure:start_end_same_word` | 100.0% |
| 3 | `count:character_count_range` | 100.0% |
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
| Média | 0.9598 |
| Mínimo | 0.3542 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.1069 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 188.7 |
| Palavras únicas (média) | 126.4 |
| Diversidade vocabular | 66.99% |
| Frases (média) | 8.4 |
| Palavras por frase | 22.6 |

