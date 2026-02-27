# Relatório de Avaliação - Capitu

**Modelo:** qwen/qwen3-235b-a22b-2507

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 79.50% (159/200) |
| Acurácia Flexível (prompt) | 84.50% |
| Acurácia por Instrução | 89.38% (362/405) |
| Pontuação Final | 0.9173 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 159 | 79.5% |
| Parcialmente corretos | 32 | 16.0% |
| 0% corretos | 9 | 4.5% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 87.1% | 87.1% | 70 |
| Medium | 84.3% | 92.1% | 70 |
| Hard | 65.0% | 88.2% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 67.1% | 7 | 70 |
| count | 90.7% | 12 | 118 |
| words | 91.1% | 7 | 56 |
| format | 93.5% | 5 | 31 |
| structure | 96.9% | 5 | 32 |
| forbidden | 98.9% | 6 | 88 |
| punctuation | 100.0% | 3 | 10 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| Vidas Secas | 69.2% | 0.97 | 26 |
| O Cortiço | 75.0% | 0.92 | 20 |
| Dom Casmurro | 76.5% | 0.94 | 17 |
| Capitães da Areia | 77.3% | 0.98 | 22 |
| Macunaíma | 81.2% | 0.96 | 32 |
| A Hora da Estrela | 81.8% | 0.99 | 33 |
| Grande Sertão: Veredas | 84.6% | 0.98 | 26 |
| Iracema | 87.5% | 0.97 | 24 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `words:max_word_repeat` | 0.0% |
| 3 | `count:character_count_range` | 0.0% |
| 4 | `pattern:terminacao_ando_endo_indo_limit` | 21.4% |
| 5 | `count:max_word_count` | 33.3% |
| 6 | `pattern:terminacao_mente_limit` | 56.0% |
| 7 | `structure:no_repeat_sentence_start` | 66.7% |
| 8 | `count:word_count_range` | 85.2% |
| 9 | `pattern:terminacao_inho_inha_min` | 87.5% |
| 10 | `format:bullet_list` | 88.9% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `format:all_lowercase` | 100.0% |
| 2 | `structure:start_end_same_word` | 100.0% |
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
| Média | 0.9677 |
| Mínimo | 0.0972 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.1118 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 220.4 |
| Palavras únicas (média) | 147.0 |
| Diversidade vocabular | 66.66% |
| Frases (média) | 9.7 |
| Palavras por frase | 22.7 |

