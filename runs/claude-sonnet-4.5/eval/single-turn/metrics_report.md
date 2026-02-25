# Relatório de Avaliação - Capitu

**Modelo:** anthropic/claude-sonnet-4.5

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 86.00% (172/200) |
| Acurácia Flexível (prompt) | 93.00% |
| Acurácia por Instrução | 90.62% (367/405) |
| Pontuação Final | 0.9432 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 172 | 86.0% |
| Parcialmente corretos | 22 | 11.0% |
| 0% corretos | 6 | 3.0% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 92.9% | 92.9% | 70 |
| Medium | 92.9% | 95.7% | 70 |
| Hard | 70.0% | 86.2% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| structure | 59.4% | 5 | 32 |
| pattern | 87.1% | 7 | 70 |
| count | 87.3% | 12 | 118 |
| words | 98.2% | 7 | 56 |
| forbidden | 100.0% | 6 | 88 |
| format | 100.0% | 5 | 31 |
| punctuation | 100.0% | 3 | 10 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| O Cortiço | 70.0% | 0.97 | 20 |
| Grande Sertão: Veredas | 80.8% | 1.00 | 26 |
| Dom Casmurro | 82.4% | 0.99 | 17 |
| Iracema | 87.5% | 0.98 | 24 |
| A Hora da Estrela | 87.9% | 1.00 | 33 |
| Vidas Secas | 88.5% | 0.97 | 26 |
| Capitães da Areia | 90.9% | 0.99 | 22 |
| Macunaíma | 93.8% | 0.99 | 32 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `structure:acrostic` | 0.0% |
| 3 | `count:exact_line_count` | 0.0% |
| 4 | `count:character_count_range` | 50.0% |
| 5 | `structure:start_with_word` | 56.2% |
| 6 | `count:exact_paragraph_count` | 57.1% |
| 7 | `structure:start_end_same_word` | 66.7% |
| 8 | `pattern:terminacao_mente_limit` | 76.0% |
| 9 | `words:max_word_repeat` | 80.0% |
| 10 | `pattern:terminacao_ando_endo_indo_limit` | 85.7% |

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
| Média | 0.9878 |
| Mínimo | 0.5944 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.0496 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 233.8 |
| Palavras únicas (média) | 157.4 |
| Diversidade vocabular | 67.31% |
| Frases (média) | 11.4 |
| Palavras por frase | 20.5 |

