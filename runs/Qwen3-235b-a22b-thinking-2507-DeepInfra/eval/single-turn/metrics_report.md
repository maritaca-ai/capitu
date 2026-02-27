# Relatório de Avaliação - Capitu

**Modelo:** qwen/qwen3-235b-a22b-thinking-2507

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 84.00% (168/200) |
| Acurácia Flexível (prompt) | 83.50% |
| Acurácia por Instrução | 87.65% (355/405) |
| Pontuação Final | 0.9263 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 168 | 84.0% |
| Parcialmente corretos | 24 | 12.0% |
| 0% corretos | 8 | 4.0% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 98.6% | 98.6% | 70 |
| Medium | 85.7% | 92.1% | 70 |
| Hard | 65.0% | 80.5% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| format | 77.4% | 5 | 31 |
| count | 82.2% | 12 | 118 |
| pattern | 84.3% | 7 | 70 |
| punctuation | 90.0% | 3 | 10 |
| words | 91.1% | 7 | 56 |
| forbidden | 95.5% | 6 | 88 |
| structure | 96.9% | 5 | 32 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| Vidas Secas | 73.1% | 0.96 | 26 |
| A Hora da Estrela | 78.8% | 0.97 | 33 |
| Iracema | 83.3% | 0.95 | 24 |
| Grande Sertão: Veredas | 84.6% | 0.97 | 26 |
| O Cortiço | 85.0% | 0.94 | 20 |
| Capitães da Areia | 86.4% | 0.98 | 22 |
| Dom Casmurro | 88.2% | 0.96 | 17 |
| Macunaíma | 93.8% | 0.96 | 32 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `format:all_caps` | 0.0% |
| 3 | `count:character_count_range` | 0.0% |
| 4 | `format:all_lowercase` | 0.0% |
| 5 | `words:max_word_repeat` | 20.0% |
| 6 | `punctuation:include_quote` | 50.0% |
| 7 | `count:unique_word_count` | 66.7% |
| 8 | `pattern:terminacao_mente_limit` | 68.0% |
| 9 | `count:min_paragraph_count` | 72.2% |
| 10 | `format:bullet_list` | 72.2% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `structure:no_repeat_sentence_start` | 100.0% |
| 2 | `structure:start_end_same_word` | 100.0% |
| 3 | `words:include_words` | 100.0% |
| 4 | `pattern:terminacao_mente_min` | 100.0% |
| 5 | `forbidden:words_list` | 100.0% |
| 6 | `forbidden:no_numbers` | 100.0% |
| 7 | `structure:end_with_word` | 100.0% |
| 8 | `format:title_case_start` | 100.0% |
| 9 | `words:word_frequency` | 100.0% |
| 10 | `count:exact_sentence_count` | 100.0% |

## Métricas de Coerência

| Métrica | Valor |
|---------|-------|
| Média | 0.9615 |
| Mínimo | 0.6000 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.0698 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 211.0 |
| Palavras únicas (média) | 145.3 |
| Diversidade vocabular | 68.89% |
| Frases (média) | 8.7 |
| Palavras por frase | 24.3 |

