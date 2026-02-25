# Relatório de Avaliação - Capitu

**Modelo:** anthropic/claude-haiku-4.5

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 73.50% (147/200) |
| Acurácia Flexível (prompt) | 84.00% |
| Acurácia por Instrução | 82.47% (334/405) |
| Pontuação Final | 0.8924 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 147 | 73.5% |
| Parcialmente corretos | 42 | 21.0% |
| 0% corretos | 11 | 5.5% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 85.7% | 85.7% | 70 |
| Medium | 84.3% | 91.4% | 70 |
| Hard | 46.7% | 74.9% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| structure | 37.5% | 5 | 32 |
| pattern | 65.7% | 7 | 70 |
| count | 79.7% | 12 | 118 |
| words | 94.6% | 7 | 56 |
| forbidden | 100.0% | 6 | 88 |
| format | 100.0% | 5 | 31 |
| punctuation | 100.0% | 3 | 10 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| Grande Sertão: Veredas | 61.5% | 1.00 | 26 |
| Macunaíma | 68.8% | 0.97 | 32 |
| O Cortiço | 70.0% | 0.95 | 20 |
| A Hora da Estrela | 72.7% | 1.00 | 33 |
| Vidas Secas | 73.1% | 0.98 | 26 |
| Iracema | 75.0% | 0.98 | 24 |
| Dom Casmurro | 82.4% | 1.00 | 17 |
| Capitães da Areia | 90.9% | 0.98 | 22 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `count:exact_paragraph_count` | 0.0% |
| 3 | `structure:acrostic` | 0.0% |
| 4 | `count:character_count_range` | 0.0% |
| 5 | `structure:start_with_word` | 18.8% |
| 6 | `count:exact_line_count` | 20.0% |
| 7 | `structure:start_end_same_word` | 33.3% |
| 8 | `pattern:terminacao_inho_inha_min` | 37.5% |
| 9 | `pattern:terminacao_mente_limit` | 40.0% |
| 10 | `words:word_frequency` | 50.0% |

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
| Média | 0.9831 |
| Mínimo | 0.5472 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.0649 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 226.4 |
| Palavras únicas (média) | 149.2 |
| Diversidade vocabular | 65.90% |
| Frases (média) | 10.6 |
| Palavras por frase | 21.5 |

