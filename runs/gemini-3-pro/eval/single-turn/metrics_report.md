# Relatório de Avaliação - Capitu

**Modelo:** google/gemini-3-pro-preview

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 92.50% (185/200) |
| Acurácia Flexível (prompt) | 95.50% |
| Acurácia por Instrução | 95.31% (386/405) |
| Pontuação Final | 0.9709 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 185 | 92.5% |
| Parcialmente corretos | 11 | 5.5% |
| 0% corretos | 4 | 2.0% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 95.7% | 95.7% | 70 |
| Medium | 94.3% | 97.1% | 70 |
| Hard | 86.7% | 93.8% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| structure | 87.5% | 5 | 32 |
| format | 93.5% | 5 | 31 |
| pattern | 94.3% | 7 | 70 |
| count | 94.9% | 12 | 118 |
| forbidden | 97.7% | 6 | 88 |
| words | 98.2% | 7 | 56 |
| punctuation | 100.0% | 3 | 10 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| O Cortiço | 80.0% | 0.90 | 20 |
| Capitães da Areia | 86.4% | 0.99 | 22 |
| Macunaíma | 90.6% | 0.99 | 32 |
| Grande Sertão: Veredas | 92.3% | 1.00 | 26 |
| Iracema | 95.8% | 0.98 | 24 |
| Vidas Secas | 96.2% | 0.99 | 26 |
| A Hora da Estrela | 97.0% | 0.99 | 33 |
| Dom Casmurro | 100.0% | 1.00 | 17 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `structure:acrostic` | 20.0% |
| 2 | `count:exact_word_count` | 66.7% |
| 3 | `words:max_word_repeat` | 80.0% |
| 4 | `count:exact_line_count` | 80.0% |
| 5 | `pattern:terminacao_mente_proibido` | 80.0% |
| 6 | `count:word_count_range` | 85.2% |
| 7 | `format:bullet_list` | 88.9% |
| 8 | `pattern:terminacao_mente_limit` | 92.0% |
| 9 | `pattern:terminacao_ando_endo_indo_limit` | 92.9% |
| 10 | `forbidden:word` | 95.2% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `format:all_lowercase` | 100.0% |
| 2 | `structure:no_repeat_sentence_start` | 100.0% |
| 3 | `structure:start_end_same_word` | 100.0% |
| 4 | `count:character_count_range` | 100.0% |
| 5 | `punctuation:include_quote` | 100.0% |
| 6 | `words:include_words` | 100.0% |
| 7 | `pattern:terminacao_mente_min` | 100.0% |
| 8 | `forbidden:words_list` | 100.0% |
| 9 | `format:all_caps` | 100.0% |
| 10 | `forbidden:no_numbers` | 100.0% |

## Métricas de Coerência

| Métrica | Valor |
|---------|-------|
| Média | 0.9872 |
| Mínimo | 0.4250 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.0642 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 236.1 |
| Palavras únicas (média) | 159.2 |
| Diversidade vocabular | 67.43% |
| Frases (média) | 10.4 |
| Palavras por frase | 22.8 |

