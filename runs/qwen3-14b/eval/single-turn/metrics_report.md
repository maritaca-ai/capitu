# Relatório de Avaliação - Capitu

**Modelo:** qwen/qwen3-14b

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 81.00% (162/200) |
| Acurácia Flexível (prompt) | 83.00% |
| Acurácia por Instrução | 89.38% (362/405) |
| Pontuação Final | 0.9085 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 162 | 81.0% |
| Parcialmente corretos | 31 | 15.5% |
| 0% corretos | 7 | 3.5% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 91.4% | 91.4% | 70 |
| Medium | 80.0% | 90.0% | 70 |
| Hard | 70.0% | 88.2% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 78.6% | 7 | 70 |
| words | 85.7% | 7 | 56 |
| count | 87.3% | 12 | 118 |
| format | 90.3% | 5 | 31 |
| structure | 93.8% | 5 | 32 |
| forbidden | 100.0% | 6 | 88 |
| punctuation | 100.0% | 3 | 10 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| Capitães da Areia | 72.7% | 0.98 | 22 |
| Vidas Secas | 76.9% | 0.94 | 26 |
| Macunaíma | 78.1% | 0.86 | 32 |
| Iracema | 79.2% | 0.91 | 24 |
| Grande Sertão: Veredas | 80.8% | 0.96 | 26 |
| Dom Casmurro | 82.4% | 0.92 | 17 |
| A Hora da Estrela | 87.9% | 0.98 | 33 |
| O Cortiço | 90.0% | 0.87 | 20 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `words:max_word_repeat` | 0.0% |
| 3 | `pattern:terminacao_inho_inha_min` | 37.5% |
| 4 | `count:word_count_range` | 55.6% |
| 5 | `structure:no_repeat_sentence_start` | 66.7% |
| 6 | `pattern:terminacao_ando_endo_indo_limit` | 71.4% |
| 7 | `pattern:terminacao_ando_endo_indo_min` | 80.0% |
| 8 | `pattern:terminacao_mente_limit` | 80.0% |
| 9 | `structure:end_with_word` | 80.0% |
| 10 | `format:bullet_list` | 83.3% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `format:all_lowercase` | 100.0% |
| 2 | `structure:start_end_same_word` | 100.0% |
| 3 | `count:character_count_range` | 100.0% |
| 4 | `punctuation:include_quote` | 100.0% |
| 5 | `words:include_words` | 100.0% |
| 6 | `pattern:terminacao_mente_min` | 100.0% |
| 7 | `forbidden:words_list` | 100.0% |
| 8 | `format:all_caps` | 100.0% |
| 9 | `forbidden:no_numbers` | 100.0% |
| 10 | `format:title_case_start` | 100.0% |

## Métricas de Coerência

| Métrica | Valor |
|---------|-------|
| Média | 0.9272 |
| Mínimo | 0.0292 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.1739 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 186.4 |
| Palavras únicas (média) | 120.3 |
| Diversidade vocabular | 64.56% |
| Frases (média) | 7.5 |
| Palavras por frase | 25.0 |

