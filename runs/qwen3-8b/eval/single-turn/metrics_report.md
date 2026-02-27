# Relatório de Avaliação - Capitu

**Modelo:** qwen/qwen3-8b

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 81.50% (163/200) |
| Acurácia Flexível (prompt) | 85.00% |
| Acurácia por Instrução | 90.37% (366/405) |
| Pontuação Final | 0.9270 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 163 | 81.5% |
| Parcialmente corretos | 35 | 17.5% |
| 0% corretos | 2 | 1.0% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 97.1% | 97.1% | 70 |
| Medium | 87.1% | 93.6% | 70 |
| Hard | 56.7% | 85.6% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| format | 83.9% | 5 | 31 |
| pattern | 87.1% | 7 | 70 |
| count | 87.3% | 12 | 118 |
| words | 87.5% | 7 | 56 |
| structure | 90.6% | 5 | 32 |
| forbidden | 100.0% | 6 | 88 |
| punctuation | 100.0% | 3 | 10 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| Vidas Secas | 73.1% | 0.92 | 26 |
| Grande Sertão: Veredas | 76.9% | 0.96 | 26 |
| A Hora da Estrela | 78.8% | 0.98 | 33 |
| Capitães da Areia | 81.8% | 0.97 | 22 |
| Dom Casmurro | 82.4% | 0.93 | 17 |
| Iracema | 83.3% | 0.89 | 24 |
| Macunaíma | 87.5% | 0.87 | 32 |
| O Cortiço | 90.0% | 0.82 | 20 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `words:max_word_repeat` | 0.0% |
| 3 | `words:word_frequency` | 0.0% |
| 4 | `count:character_count_range` | 0.0% |
| 5 | `pattern:terminacao_inho_inha_min` | 50.0% |
| 6 | `count:word_count_range` | 66.7% |
| 7 | `structure:start_end_same_word` | 66.7% |
| 8 | `structure:no_repeat_sentence_start` | 66.7% |
| 9 | `pattern:terminacao_ando_endo_indo_limit` | 71.4% |
| 10 | `format:bullet_list` | 72.2% |

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
| 8 | `structure:end_with_word` | 100.0% |
| 9 | `format:title_case_start` | 100.0% |
| 10 | `count:exact_sentence_count` | 100.0% |

## Métricas de Coerência

| Métrica | Valor |
|---------|-------|
| Média | 0.9218 |
| Mínimo | 0.1306 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.1838 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 190.7 |
| Palavras únicas (média) | 118.3 |
| Diversidade vocabular | 62.03% |
| Frases (média) | 8.0 |
| Palavras por frase | 23.8 |

