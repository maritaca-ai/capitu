# Relatório de Avaliação - Capitu

**Modelo:** google/gemini-3-flash-preview

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 89.00% (178/200) |
| Acurácia Flexível (prompt) | 93.00% |
| Acurácia por Instrução | 94.32% (382/405) |
| Pontuação Final | 0.9675 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 178 | 89.0% |
| Parcialmente corretos | 22 | 11.0% |
| 0% corretos | 0 | 0.0% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 100.0% | 100.0% | 70 |
| Medium | 95.7% | 97.9% | 70 |
| Hard | 68.3% | 89.7% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| format | 80.6% | 5 | 31 |
| words | 89.3% | 7 | 56 |
| structure | 90.6% | 5 | 32 |
| pattern | 95.7% | 7 | 70 |
| count | 95.8% | 12 | 118 |
| forbidden | 100.0% | 6 | 88 |
| punctuation | 100.0% | 3 | 10 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| Vidas Secas | 76.9% | 0.97 | 26 |
| O Cortiço | 80.0% | 0.91 | 20 |
| Capitães da Areia | 86.4% | 0.98 | 22 |
| A Hora da Estrela | 90.9% | 0.99 | 33 |
| Iracema | 91.7% | 0.97 | 24 |
| Grande Sertão: Veredas | 92.3% | 1.00 | 26 |
| Macunaíma | 93.8% | 0.98 | 32 |
| Dom Casmurro | 100.0% | 1.00 | 17 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `words:max_word_repeat` | 0.0% |
| 2 | `count:exact_word_count` | 33.3% |
| 3 | `structure:acrostic` | 40.0% |
| 4 | `count:character_count_range` | 50.0% |
| 5 | `format:bullet_list` | 66.7% |
| 6 | `count:exact_sentence_count` | 75.0% |
| 7 | `count:exact_line_count` | 80.0% |
| 8 | `pattern:terminacao_ando_endo_indo_limit` | 85.7% |
| 9 | `pattern:terminacao_inho_inha_min` | 87.5% |
| 10 | `words:connective` | 94.4% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `format:all_lowercase` | 100.0% |
| 2 | `structure:no_repeat_sentence_start` | 100.0% |
| 3 | `structure:start_end_same_word` | 100.0% |
| 4 | `punctuation:include_quote` | 100.0% |
| 5 | `words:include_words` | 100.0% |
| 6 | `pattern:terminacao_mente_min` | 100.0% |
| 7 | `forbidden:words_list` | 100.0% |
| 8 | `format:all_caps` | 100.0% |
| 9 | `forbidden:no_numbers` | 100.0% |
| 10 | `structure:end_with_word` | 100.0% |

## Métricas de Coerência

| Métrica | Valor |
|---------|-------|
| Média | 0.9774 |
| Mínimo | 0.3014 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.0878 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 210.9 |
| Palavras únicas (média) | 141.7 |
| Diversidade vocabular | 67.20% |
| Frases (média) | 9.8 |
| Palavras por frase | 21.4 |

