# Relatório de Avaliação - Capitu

**Modelo:** qwen/qwen3-32b

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 82.50% (165/200) |
| Acurácia Flexível (prompt) | 83.50% |
| Acurácia por Instrução | 90.12% (365/405) |
| Pontuação Final | 0.9260 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 165 | 82.5% |
| Parcialmente corretos | 28 | 14.0% |
| 0% corretos | 7 | 3.5% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 91.4% | 91.4% | 70 |
| Medium | 85.7% | 92.9% | 70 |
| Hard | 68.3% | 87.7% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| pattern | 81.4% | 7 | 70 |
| count | 88.1% | 12 | 118 |
| words | 89.3% | 7 | 56 |
| structure | 90.6% | 5 | 32 |
| format | 93.5% | 5 | 31 |
| forbidden | 97.7% | 6 | 88 |
| punctuation | 100.0% | 3 | 10 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| Vidas Secas | 73.1% | 0.97 | 26 |
| Dom Casmurro | 76.5% | 0.94 | 17 |
| Capitães da Areia | 77.3% | 0.99 | 22 |
| Iracema | 83.3% | 0.98 | 24 |
| Macunaíma | 84.4% | 0.94 | 32 |
| A Hora da Estrela | 84.8% | 0.99 | 33 |
| Grande Sertão: Veredas | 88.5% | 0.99 | 26 |
| O Cortiço | 90.0% | 0.88 | 20 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `words:max_word_repeat` | 0.0% |
| 3 | `format:all_caps` | 0.0% |
| 4 | `count:character_count_range` | 0.0% |
| 5 | `structure:end_with_word` | 60.0% |
| 6 | `pattern:terminacao_ando_endo_indo_limit` | 64.3% |
| 7 | `count:word_count_range` | 66.7% |
| 8 | `pattern:terminacao_inho_inha_min` | 75.0% |
| 9 | `pattern:terminacao_ando_endo_indo_min` | 80.0% |
| 10 | `structure:acrostic` | 80.0% |

## Instruções Mais Fáceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `format:all_lowercase` | 100.0% |
| 2 | `structure:no_repeat_sentence_start` | 100.0% |
| 3 | `structure:start_end_same_word` | 100.0% |
| 4 | `punctuation:include_quote` | 100.0% |
| 5 | `words:include_words` | 100.0% |
| 6 | `pattern:terminacao_mente_min` | 100.0% |
| 7 | `forbidden:words_list` | 100.0% |
| 8 | `format:title_case_start` | 100.0% |
| 9 | `words:word_frequency` | 100.0% |
| 10 | `count:exact_sentence_count` | 100.0% |

## Métricas de Coerência

| Métrica | Valor |
|---------|-------|
| Média | 0.9621 |
| Mínimo | 0.2417 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.1163 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 221.1 |
| Palavras únicas (média) | 145.9 |
| Diversidade vocabular | 65.97% |
| Frases (média) | 8.9 |
| Palavras por frase | 24.9 |

