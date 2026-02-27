# Relatório de Avaliação - Capitu

**Modelo:** gpt-5

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 98.00% (196/200) |
| Acurácia Flexível (prompt) | 99.00% |
| Acurácia por Instrução | 99.01% (401/405) |
| Pontuação Final | 0.9912 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 196 | 98.0% |
| Parcialmente corretos | 4 | 2.0% |
| 0% corretos | 0 | 0.0% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 100.0% | 100.0% | 70 |
| Medium | 97.1% | 98.6% | 70 |
| Hard | 96.7% | 99.0% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| punctuation | 80.0% | 3 | 10 |
| words | 98.2% | 7 | 56 |
| count | 99.2% | 12 | 118 |
| pattern | 100.0% | 7 | 70 |
| forbidden | 100.0% | 6 | 88 |
| format | 100.0% | 5 | 31 |
| structure | 100.0% | 5 | 32 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| A Hora da Estrela | 93.9% | 0.99 | 33 |
| Capitães da Areia | 95.5% | 0.99 | 22 |
| Grande Sertão: Veredas | 96.2% | 1.00 | 26 |
| Iracema | 100.0% | 0.98 | 24 |
| Macunaíma | 100.0% | 0.99 | 32 |
| Dom Casmurro | 100.0% | 1.00 | 17 |
| O Cortiço | 100.0% | 0.99 | 20 |
| Vidas Secas | 100.0% | 0.98 | 26 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `punctuation:include_quote` | 0.0% |
| 2 | `words:word_frequency` | 50.0% |
| 3 | `count:word_count_range` | 96.3% |
| 4 | `count:min_paragraph_count` | 100.0% |
| 5 | `pattern:terminacao_ando_endo_indo_min` | 100.0% |
| 6 | `words:connective` | 100.0% |
| 7 | `count:exact_word_count` | 100.0% |
| 8 | `words:max_word_repeat` | 100.0% |
| 9 | `forbidden:no_first_person` | 100.0% |
| 10 | `words:contrast_marker` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `format:all_lowercase` | 100.0% |
| 2 | `structure:no_repeat_sentence_start` | 100.0% |
| 3 | `structure:start_end_same_word` | 100.0% |
| 4 | `count:character_count_range` | 100.0% |
| 5 | `words:include_words` | 100.0% |
| 6 | `pattern:terminacao_mente_min` | 100.0% |
| 7 | `forbidden:words_list` | 100.0% |
| 8 | `format:all_caps` | 100.0% |
| 9 | `forbidden:no_numbers` | 100.0% |
| 10 | `structure:end_with_word` | 100.0% |

## Métricas de Coerência

| Métrica | Valor |
|---------|-------|
| Média | 0.9903 |
| Mínimo | 0.7000 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.0395 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 310.6 |
| Palavras únicas (média) | 199.3 |
| Diversidade vocabular | 64.18% |
| Frases (média) | 14.5 |
| Palavras por frase | 21.4 |

