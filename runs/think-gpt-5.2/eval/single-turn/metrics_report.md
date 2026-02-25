# Relatório de Avaliação - Capitu

**Modelo:** gpt-5.2

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 98.50% (197/200) |
| Acurácia Flexível (prompt) | 98.50% |
| Acurácia por Instrução | 99.26% (402/405) |
| Pontuação Final | 0.9881 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 197 | 98.5% |
| Parcialmente corretos | 3 | 1.5% |
| 0% corretos | 0 | 0.0% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 100.0% | 100.0% | 70 |
| Medium | 98.6% | 99.3% | 70 |
| Hard | 96.7% | 99.0% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| punctuation | 80.0% | 3 | 10 |
| format | 96.8% | 5 | 31 |
| count | 100.0% | 12 | 118 |
| pattern | 100.0% | 7 | 70 |
| words | 100.0% | 7 | 56 |
| forbidden | 100.0% | 6 | 88 |
| structure | 100.0% | 5 | 32 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| Capitães da Areia | 95.5% | 0.98 | 22 |
| Grande Sertão: Veredas | 96.2% | 1.00 | 26 |
| A Hora da Estrela | 97.0% | 0.98 | 33 |
| Iracema | 100.0% | 0.95 | 24 |
| Macunaíma | 100.0% | 0.97 | 32 |
| Dom Casmurro | 100.0% | 0.98 | 17 |
| O Cortiço | 100.0% | 0.97 | 20 |
| Vidas Secas | 100.0% | 0.98 | 26 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `punctuation:include_quote` | 0.0% |
| 2 | `format:bullet_list` | 94.4% |
| 3 | `count:min_paragraph_count` | 100.0% |
| 4 | `pattern:terminacao_ando_endo_indo_min` | 100.0% |
| 5 | `words:connective` | 100.0% |
| 6 | `count:exact_word_count` | 100.0% |
| 7 | `words:max_word_repeat` | 100.0% |
| 8 | `forbidden:no_first_person` | 100.0% |
| 9 | `words:contrast_marker` | 100.0% |
| 10 | `count:word_count_range` | 100.0% |

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
| Média | 0.9760 |
| Mínimo | 0.8000 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.0439 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 303.8 |
| Palavras únicas (média) | 191.4 |
| Diversidade vocabular | 62.99% |
| Frases (média) | 11.9 |
| Palavras por frase | 25.5 |

