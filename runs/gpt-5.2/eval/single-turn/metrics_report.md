# Relatório de Avaliação - Capitu

**Modelo:** gpt-5.2

**Dataset:** data/input_questions.jsonl

**Modo:** Single-turn

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| Acurácia Estrita (prompt) | 91.50% (183/200) |
| Acurácia Flexível (prompt) | 91.00% |
| Acurácia por Instrução | 95.06% (385/405) |
| Pontuação Final | 0.9706 |

### Distribuição de Resultados

| Resultado | Quantidade | Porcentagem |
|-----------|------------|-------------|
| 100% corretos | 183 | 91.5% |
| Parcialmente corretos | 17 | 8.5% |
| 0% corretos | 0 | 0.0% |

## Resultados por Dificuldade

| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |
|-------------|-------------------|----------------------|-------|
| Easy | 100.0% | 100.0% | 70 |
| Medium | 91.4% | 95.7% | 70 |
| Hard | 81.7% | 92.8% | 60 |

## Resultados por Categoria de Instrução

| Categoria | Acurácia | Tipos | Total |
|-----------|----------|-------|-------|
| punctuation | 80.0% | 3 | 10 |
| count | 91.5% | 12 | 118 |
| words | 92.9% | 7 | 56 |
| format | 93.5% | 5 | 31 |
| structure | 96.9% | 5 | 32 |
| pattern | 98.6% | 7 | 70 |
| forbidden | 100.0% | 6 | 88 |

## Resultados por Obra Literária

| Obra | Acurácia | Coerência | Total |
|------|----------|-----------|-------|
| A Hora da Estrela | 81.8% | 0.99 | 33 |
| Dom Casmurro | 88.2% | 1.00 | 17 |
| Vidas Secas | 88.5% | 0.96 | 26 |
| Capitães da Areia | 90.9% | 0.97 | 22 |
| Iracema | 91.7% | 0.98 | 24 |
| Grande Sertão: Veredas | 92.3% | 0.99 | 26 |
| Macunaíma | 100.0% | 0.98 | 32 |
| O Cortiço | 100.0% | 1.00 | 20 |

## Instruções Mais Difíceis

| # | Instrução | Acurácia |
|---|-----------|----------|
| 1 | `count:exact_word_count` | 0.0% |
| 2 | `punctuation:include_quote` | 0.0% |
| 3 | `words:max_word_repeat` | 20.0% |
| 4 | `count:word_count_range` | 77.8% |
| 5 | `structure:acrostic` | 80.0% |
| 6 | `count:unique_word_count` | 83.3% |
| 7 | `pattern:terminacao_inho_inha_min` | 87.5% |
| 8 | `format:bullet_list` | 88.9% |
| 9 | `count:min_paragraph_count` | 100.0% |
| 10 | `pattern:terminacao_ando_endo_indo_min` | 100.0% |

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
| Média | 0.9836 |
| Mínimo | 0.5986 |
| Máximo | 1.0000 |
| Desvio Padrão | 0.0586 |

## Qualidade das Respostas

| Métrica | Valor |
|---------|-------|
| Palavras (média) | 293.0 |
| Palavras únicas (média) | 185.5 |
| Diversidade vocabular | 63.31% |
| Frases (média) | 11.8 |
| Palavras por frase | 24.8 |

