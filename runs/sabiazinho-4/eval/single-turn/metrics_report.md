# Relatório de Avaliação - Capitu

**Modelo:** sabiazinho-4

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 87.00% (174/200) |
| Acurácia Flexível (prompt) | 87.00% |
| Acurácia por Instrução | 93.09% (377/405) |
| Pontuação Final | 0.9463 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 174 | 87.0% |
| Parcialmente corretos | 26 | 13.0% |
| 0% corretos | 0 | 0.0% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 100.0% | 100.0% | 70 |
| Medium | 85.7% | 92.9% | 70 |
| Hard | 73.3% | 90.8% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 88.6% | 7 | 70 |
| words | 89.3% | 7 | 56 |
| count | 90.7% | 12 | 118 |
| format | 96.8% | 5 | 31 |
| structure | 96.9% | 5 | 32 |
| forbidden | 98.9% | 6 | 88 |
| punctuation | 100.0% | 3 | 10 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| Grande Sertão: Veredas | 73.1% | 0.97 | 26 |
| A Hora da Estrela | 78.8% | 0.98 | 33 |
| Dom Casmurro | 82.4% | 0.92 | 17 |
| Iracema | 87.5% | 0.95 | 24 |
| Vidas Secas | 88.5% | 0.93 | 26 |
| Capitães da Areia | 90.9% | 0.97 | 22 |
| O Cortiço | 95.0% | 0.89 | 20 |
| Macunaíma | 100.0% | 0.90 | 32 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `count:character_count_range` | 0.0% |
| 3 | `words:max_word_repeat` | 20.0% |
| 4 | `pattern:terminacao_inho_inha_min` | 25.0% |
| 5 | `words:word_frequency` | 50.0% |
| 6 | `structure:start_end_same_word` | 66.7% |
| 7 | `pattern:terminacao_ando_endo_indo_min` | 80.0% |
| 8 | `count:word_count_range` | 81.5% |
| 9 | `pattern:terminacao_ando_endo_indo_limit` | 92.9% |
| 10 | `forbidden:no_first_person` | 93.8% |

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
| Média | 0.9413 |
| Mínimo | 0.1833 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.1623 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 194.0 |
| Palavras únicas (média) | 130.3 |
| Diversidade vocabular | 67.15% |
| Frases (média) | 8.5 |
| Palavras por frase | 22.9 |

