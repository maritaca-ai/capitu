# Relatório de Avaliação - Capitu

**Modelo:** gpt-5-mini

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 98.00% (196/200) |
| Acurácia Flexível (prompt) | 98.00% |
| Acurácia por Instrução | 99.01% (401/405) |
| Pontuação Final | 0.9888 |

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
| Medium | 98.6% | 99.3% | 70 |
| Hard | 95.0% | 98.5% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| punctuation | 90.0% | 3 | 10 |
| words | 98.2% | 7 | 56 |
| pattern | 98.6% | 7 | 70 |
| count | 99.2% | 12 | 118 |
| forbidden | 100.0% | 6 | 88 |
| format | 100.0% | 5 | 31 |
| structure | 100.0% | 5 | 32 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| A Hora da Estrela | 90.9% | 0.98 | 33 |
| Vidas Secas | 96.2% | 0.96 | 26 |
| Iracema | 100.0% | 0.98 | 24 |
| Macunaíma | 100.0% | 0.98 | 32 |
| Dom Casmurro | 100.0% | 1.00 | 17 |
| O Cortiço | 100.0% | 0.95 | 20 |
| Grande Sertão: Veredas | 100.0% | 1.00 | 26 |
| Capitães da Areia | 100.0% | 0.98 | 22 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `punctuation:include_quote` | 50.0% |
| 2 | `count:character_count_range` | 50.0% |
| 3 | `words:max_word_repeat` | 80.0% |
| 4 | `pattern:terminacao_ando_endo_indo_limit` | 92.9% |
| 5 | `count:min_paragraph_count` | 100.0% |
| 6 | `pattern:terminacao_ando_endo_indo_min` | 100.0% |
| 7 | `words:connective` | 100.0% |
| 8 | `count:exact_word_count` | 100.0% |
| 9 | `forbidden:no_first_person` | 100.0% |
| 10 | `words:contrast_marker` | 100.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `format:all_lowercase` | 100.0% |
| 2 | `structure:no_repeat_sentence_start` | 100.0% |
| 3 | `structure:start_end_same_word` | 100.0% |
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
| Média | 0.9807 |
| Mínimo | 0.6208 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.0580 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 266.1 |
| Palavras únicas (média) | 172.2 |
| Diversidade vocabular | 64.68% |
| Frases (média) | 11.1 |
| Palavras por frase | 23.9 |

