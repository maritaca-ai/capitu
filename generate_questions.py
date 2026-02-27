#!/usr/bin/env python3
"""
Gerador de questões para o Capitu com níveis de dificuldade e suporte multi-turn.

Níveis:
- easy: 1 instrução
- medium: 2 instruções combinadas
- hard: 3-4 instruções combinadas

Modos:
- single-turn: Uma pergunta por vez (padrão)
- multi-turn: Conversa com 2-3 turnos progressivos

Uso:
    python generate_questions.py --output data/input_questions.jsonl --easy 70 --medium 70 --hard 60
    python generate_questions.py --output data/input_questions_multiturn.jsonl --multi_turn --turns 100
"""

import argparse
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass
class InstructionTemplate:
    """Template de uma instrução com descrição e kwargs."""
    id: str
    description_template: str
    kwargs_generator: Callable
    category: str

def gen_word_count_range():
    min_w = random.choice([80, 100, 120, 150, 180])
    max_w = min_w + random.randint(20, 50)
    return {"min_words": min_w, "max_words": max_w}

def gen_exact_word_count():
    return {"target_words": random.choice([100, 120, 150, 180, 200])}

def gen_min_word_count():
    return {"min_words": random.choice([80, 100, 120, 150])}

def gen_max_word_count():
    return {"max_words": random.choice([150, 200, 250, 300])}

def gen_unique_word_count():
    return {"N": random.choice([40, 50, 60, 75])}

def gen_character_count_range():
    min_c = random.choice([400, 500, 600, 800])
    max_c = min_c + random.randint(200, 400)
    return {"min_chars": min_c, "max_chars": max_c}

def gen_exact_sentence_count():
    return {"N": random.choice([5, 6, 7, 8, 10])}

def gen_min_sentence_count():
    return {"N": random.choice([4, 5, 6, 8])}

def gen_sentence_count_range():
    min_s = random.choice([4, 5, 6])
    max_s = min_s + random.randint(2, 4)
    return {"min_sentences": min_s, "max_sentences": max_s}

def gen_exact_paragraph_count():
    return {"num_paragraphs": random.choice([2, 3, 4])}

def gen_min_paragraph_count():
    return {"min_paragraphs": random.choice([2, 3, 4])}

def gen_max_sentence_length():
    return {"max_words_per_sentence": random.choice([15, 20, 25, 30])}

def gen_min_sentence_length():
    return {"min_words_per_sentence": random.choice([8, 10, 12])}

def gen_exact_line_count():
    return {"N": random.choice([5, 6, 7, 8, 10])}

def gen_exact_number_count():
    return {"N": random.choice([2, 3, 4, 5])}

def gen_min_number_count():
    return {"N": random.choice([2, 3, 4])}

def gen_include_specific_number():
    return {"number": random.choice([7, 10, 15, 20, 42, 100, 1000, 2024])}

def gen_include_word():
    words = ["literatura", "narrativa", "personagem", "enredo", "autor",
             "sociedade", "conflito", "transformação", "identidade", "memória",
             "história", "cultura", "tradição", "Brasil", "brasileiro"]
    return {"word": random.choice(words)}

def gen_include_words():
    all_words = ["literatura", "narrativa", "personagem", "enredo", "autor",
                 "sociedade", "conflito", "transformação", "identidade", "memória"]
    return {"words": random.sample(all_words, k=random.randint(2, 3))}

def gen_word_frequency():
    words = ["assim", "então", "portanto", "contudo", "porém", "porque", "pois"]
    return {"word": random.choice(words), "min_count": random.choice([2, 3, 4])}

def gen_min_word_frequency():
    words = ["assim", "então", "portanto", "contudo", "porém"]
    return {"word": random.choice(words), "min_count": random.choice([2, 3])}

def gen_forbidden_word():
    words = ["muito", "sempre", "nunca", "realmente", "basicamente",
             "obviamente", "interessante", "importante", "fundamental",
             "incrível", "maravilhoso", "fantástico", "coisa", "fazer"]
    return {"forbidden_word": random.choice(words)}

def gen_forbidden_words_list():
    words = ["muito", "sempre", "nunca", "realmente", "basicamente",
             "obviamente", "interessante", "importante", "fundamental"]
    return {"forbidden_words": random.sample(words, k=3)}

def gen_empty():
    return {}

def gen_start_word():
    words = ["Primeiramente", "Inicialmente", "Considerando", "Analisando",
             "Observando", "Refletindo", "Certamente", "Naturalmente"]
    return {"start_word": random.choice(words)}

def gen_end_word():
    words = ["sociedade", "literatura", "reflexão", "análise", "conclusão",
             "perspectiva", "contexto", "narrativa"]
    return {"end_word": random.choice(words)}

def gen_start_end_same():
    words = ["literatura", "narrativa", "análise", "reflexão", "obra"]
    return {"word": random.choice(words)}

def gen_line_prefix():
    prefixes = ["•", "-", "*", ">", "→"]
    return {"prefix": random.choice(prefixes)}

def gen_acrostic():
    words = ["AMOR", "VIDA", "ARTE", "OBRA", "LER", "SOL", "MAR", "CÉU"]
    return {"word": random.choice(words)}

def gen_terminacao_ando_endo_indo_limit():
    return {"max_count": random.choice([3, 4, 5, 7])}

def gen_terminacao_ando_endo_indo_min():
    return {"min_count": random.choice([2, 3, 4])}

def gen_terminacao_inho_inha_min():
    return {"min_count": random.choice([2, 3, 4])}

def gen_terminacao_ao_oes_min():
    return {"min_count": random.choice([2, 3, 4])}

def gen_terminacao_mente_limit():
    return {"max_count": random.choice([2, 3, 4, 5])}

def gen_terminacao_mente_min():
    return {"min_count": random.choice([2, 3, 4])}

def gen_conjunction_count():
    return {"N": random.choice([3, 4, 5, 7])}

def gen_connective_min():
    return {"min_connectives": random.choice([2, 3, 4])}

def gen_temporal_marker():
    return {"min_markers": random.choice([2, 3])}

def gen_contrast_marker():
    return {}  # apenas exige pelo menos um

def gen_max_word_repeat():
    return {"N": random.choice([3, 4, 5])}

INSTRUCTIONS = {
    "count:word_count_range": InstructionTemplate(
        id="count:word_count_range",
        description_template="a resposta deve conter entre {min_words} e {max_words} palavras",
        kwargs_generator=gen_word_count_range,
        category="count"
    ),
    "count:exact_word_count": InstructionTemplate(
        id="count:exact_word_count",
        description_template="a resposta deve ter exatamente {target_words} palavras",
        kwargs_generator=gen_exact_word_count,
        category="count"
    ),
    "count:min_word_count": InstructionTemplate(
        id="count:min_word_count",
        description_template="a resposta deve ter pelo menos {min_words} palavras",
        kwargs_generator=gen_min_word_count,
        category="count"
    ),
    "count:max_word_count": InstructionTemplate(
        id="count:max_word_count",
        description_template="a resposta deve ter no máximo {max_words} palavras",
        kwargs_generator=gen_max_word_count,
        category="count"
    ),
    "count:unique_word_count": InstructionTemplate(
        id="count:unique_word_count",
        description_template="use pelo menos {N} palavras únicas (diferentes) na resposta",
        kwargs_generator=gen_unique_word_count,
        category="count"
    ),
    "count:character_count_range": InstructionTemplate(
        id="count:character_count_range",
        description_template="a resposta deve ter entre {min_chars} e {max_chars} caracteres",
        kwargs_generator=gen_character_count_range,
        category="count"
    ),

    "count:exact_sentence_count": InstructionTemplate(
        id="count:exact_sentence_count",
        description_template="a resposta deve ter exatamente {N} frases",
        kwargs_generator=gen_exact_sentence_count,
        category="count"
    ),
    "count:min_sentence_count": InstructionTemplate(
        id="count:min_sentence_count",
        description_template="a resposta deve ter pelo menos {N} frases",
        kwargs_generator=gen_min_sentence_count,
        category="count"
    ),
    "count:sentence_count_range": InstructionTemplate(
        id="count:sentence_count_range",
        description_template="a resposta deve ter entre {min_sentences} e {max_sentences} frases",
        kwargs_generator=gen_sentence_count_range,
        category="count"
    ),
    "count:exact_paragraph_count": InstructionTemplate(
        id="count:exact_paragraph_count",
        description_template="a resposta deve ter exatamente {num_paragraphs} parágrafos",
        kwargs_generator=gen_exact_paragraph_count,
        category="count"
    ),
    "count:min_paragraph_count": InstructionTemplate(
        id="count:min_paragraph_count",
        description_template="a resposta deve ter pelo menos {min_paragraphs} parágrafos",
        kwargs_generator=gen_min_paragraph_count,
        category="count"
    ),
    "count:max_sentence_length": InstructionTemplate(
        id="count:max_sentence_length",
        description_template="cada frase deve ter no máximo {max_words_per_sentence} palavras",
        kwargs_generator=gen_max_sentence_length,
        category="count"
    ),
    "count:min_sentence_length": InstructionTemplate(
        id="count:min_sentence_length",
        description_template="cada frase deve ter pelo menos {min_words_per_sentence} palavras",
        kwargs_generator=gen_min_sentence_length,
        category="count"
    ),
    "count:exact_line_count": InstructionTemplate(
        id="count:exact_line_count",
        description_template="a resposta deve ter exatamente {N} linhas",
        kwargs_generator=gen_exact_line_count,
        category="count"
    ),

    "count:exact_number_count": InstructionTemplate(
        id="count:exact_number_count",
        description_template="use exatamente {N} números (algarismos) diferentes",
        kwargs_generator=gen_exact_number_count,
        category="count"
    ),
    "count:min_number_count": InstructionTemplate(
        id="count:min_number_count",
        description_template="use pelo menos {N} números (algarismos)",
        kwargs_generator=gen_min_number_count,
        category="count"
    ),
    "count:include_specific_number": InstructionTemplate(
        id="count:include_specific_number",
        description_template="inclua o número {number} na resposta",
        kwargs_generator=gen_include_specific_number,
        category="count"
    ),

    "words:include_word": InstructionTemplate(
        id="words:include_word",
        description_template="inclua a palavra '{word}' na resposta",
        kwargs_generator=gen_include_word,
        category="words"
    ),
    "words:include_words": InstructionTemplate(
        id="words:include_words",
        description_template="inclua as palavras: {words_str}",
        kwargs_generator=gen_include_words,
        category="words"
    ),
    "words:word_frequency": InstructionTemplate(
        id="words:word_frequency",
        description_template="use a palavra '{word}' pelo menos {min_count} vezes",
        kwargs_generator=gen_word_frequency,
        category="words"
    ),
    "words:min_word_frequency": InstructionTemplate(
        id="words:min_word_frequency",
        description_template="use a palavra '{word}' pelo menos {min_count} vezes",
        kwargs_generator=gen_min_word_frequency,
        category="words"
    ),

    "forbidden:word": InstructionTemplate(
        id="forbidden:word",
        description_template='NÃO use a palavra "{forbidden_word}"',
        kwargs_generator=gen_forbidden_word,
        category="forbidden"
    ),
    "forbidden:words_list": InstructionTemplate(
        id="forbidden:words_list",
        description_template="NÃO use nenhuma das palavras: {forbidden_words_str}",
        kwargs_generator=gen_forbidden_words_list,
        category="forbidden"
    ),
    "forbidden:no_numbers": InstructionTemplate(
        id="forbidden:no_numbers",
        description_template="NÃO use números (algarismos)",
        kwargs_generator=gen_empty,
        category="forbidden"
    ),

    "forbidden:no_first_person": InstructionTemplate(
        id="forbidden:no_first_person",
        description_template="NÃO use pronomes de primeira pessoa (eu, me, mim, nós, meu, nosso, etc.)",
        kwargs_generator=gen_empty,
        category="forbidden"
    ),
    "forbidden:no_second_person": InstructionTemplate(
        id="forbidden:no_second_person",
        description_template="NÃO use pronomes de segunda pessoa (tu, te, ti, vós, teu, você, etc.)",
        kwargs_generator=gen_empty,
        category="forbidden"
    ),
    "words:use_first_person": InstructionTemplate(
        id="words:use_first_person",
        description_template="escreva em primeira pessoa (use eu, meu, nosso, etc.)",
        kwargs_generator=gen_empty,
        category="words"
    ),
    "words:use_third_person": InstructionTemplate(
        id="words:use_third_person",
        description_template="escreva em terceira pessoa (use ele, ela, eles, dele, etc.)",
        kwargs_generator=gen_empty,
        category="words"
    ),

    "forbidden:no_questions": InstructionTemplate(
        id="forbidden:no_questions",
        description_template="NÃO faça perguntas (não use '?')",
        kwargs_generator=gen_empty,
        category="forbidden"
    ),
    "forbidden:no_exclamations": InstructionTemplate(
        id="forbidden:no_exclamations",
        description_template="NÃO use pontos de exclamação",
        kwargs_generator=gen_empty,
        category="forbidden"
    ),
    "punctuation:only_declarative": InstructionTemplate(
        id="punctuation:only_declarative",
        description_template="use apenas frases declarativas (sem perguntas ou exclamações)",
        kwargs_generator=gen_empty,
        category="punctuation"
    ),
    "punctuation:include_question": InstructionTemplate(
        id="punctuation:include_question",
        description_template="inclua pelo menos uma pergunta na resposta",
        kwargs_generator=gen_empty,
        category="punctuation"
    ),
    "punctuation:include_quote": InstructionTemplate(
        id="punctuation:include_quote",
        description_template='inclua pelo menos uma citação entre aspas ("...")',
        kwargs_generator=gen_empty,
        category="punctuation"
    ),
    "punctuation:use_semicolon": InstructionTemplate(
        id="punctuation:use_semicolon",
        description_template="use pelo menos um ponto e vírgula (;)",
        kwargs_generator=gen_empty,
        category="punctuation"
    ),
    "punctuation:use_colon": InstructionTemplate(
        id="punctuation:use_colon",
        description_template="use pelo menos dois pontos (:) para introduzir uma explicação ou lista",
        kwargs_generator=gen_empty,
        category="punctuation"
    ),

    "structure:start_with_word": InstructionTemplate(
        id="structure:start_with_word",
        description_template="comece a resposta com a palavra '{start_word}'",
        kwargs_generator=gen_start_word,
        category="structure"
    ),
    "structure:end_with_word": InstructionTemplate(
        id="structure:end_with_word",
        description_template="termine a resposta com a palavra '{end_word}'",
        kwargs_generator=gen_end_word,
        category="structure"
    ),
    "structure:start_end_same_word": InstructionTemplate(
        id="structure:start_end_same_word",
        description_template="comece e termine a resposta com a palavra '{word}'",
        kwargs_generator=gen_start_end_same,
        category="structure"
    ),
    "format:bullet_list": InstructionTemplate(
        id="format:bullet_list",
        description_template="formate a resposta como lista com marcadores (use • ou - no início de cada item)",
        kwargs_generator=gen_empty,
        category="format"
    ),
    "format:numbered_list": InstructionTemplate(
        id="format:numbered_list",
        description_template="formate a resposta como lista numerada (1., 2., 3., etc.)",
        kwargs_generator=gen_empty,
        category="format"
    ),
    "format:all_caps": InstructionTemplate(
        id="format:all_caps",
        description_template="escreva toda a resposta em LETRAS MAIÚSCULAS",
        kwargs_generator=gen_empty,
        category="format"
    ),
    "format:all_lowercase": InstructionTemplate(
        id="format:all_lowercase",
        description_template="escreva toda a resposta em letras minúsculas",
        kwargs_generator=gen_empty,
        category="format"
    ),
    "format:title_case_start": InstructionTemplate(
        id="format:title_case_start",
        description_template="capitalize a primeira letra de cada frase",
        kwargs_generator=gen_empty,
        category="format"
    ),
    "structure:no_repeat_sentence_start": InstructionTemplate(
        id="structure:no_repeat_sentence_start",
        description_template="não comece duas frases com a mesma palavra",
        kwargs_generator=gen_empty,
        category="structure"
    ),
    "structure:each_line_starts_with": InstructionTemplate(
        id="structure:each_line_starts_with",
        description_template="cada linha deve começar com '{prefix}'",
        kwargs_generator=gen_line_prefix,
        category="structure"
    ),
    "structure:acrostic": InstructionTemplate(
        id="structure:acrostic",
        description_template="escreva um acróstico onde a primeira letra de cada linha forma a palavra '{word}'",
        kwargs_generator=gen_acrostic,
        category="structure"
    ),

    "pattern:terminacao_ando_endo_indo_limit": InstructionTemplate(
        id="pattern:terminacao_ando_endo_indo_limit",
        description_template="use no máximo {max_count} palavras terminadas em -ando, -endo ou -indo",
        kwargs_generator=gen_terminacao_ando_endo_indo_limit,
        category="pattern"
    ),
    "pattern:terminacao_ando_endo_indo_min": InstructionTemplate(
        id="pattern:terminacao_ando_endo_indo_min",
        description_template="use pelo menos {min_count} palavras terminadas em -ando, -endo ou -indo",
        kwargs_generator=gen_terminacao_ando_endo_indo_min,
        category="pattern"
    ),
    "pattern:terminacao_inho_inha_min": InstructionTemplate(
        id="pattern:terminacao_inho_inha_min",
        description_template="use pelo menos {min_count} palavras terminadas em -inho ou -inha",
        kwargs_generator=gen_terminacao_inho_inha_min,
        category="pattern"
    ),
    "pattern:terminacao_inho_inha_proibido": InstructionTemplate(
        id="pattern:terminacao_inho_inha_proibido",
        description_template="NÃO use palavras terminadas em -inho ou -inha",
        kwargs_generator=gen_empty,
        category="pattern"
    ),
    "pattern:terminacao_ao_oes_min": InstructionTemplate(
        id="pattern:terminacao_ao_oes_min",
        description_template="use pelo menos {min_count} palavras terminadas em -ão ou -ões",
        kwargs_generator=gen_terminacao_ao_oes_min,
        category="pattern"
    ),
    "pattern:terminacao_mente_limit": InstructionTemplate(
        id="pattern:terminacao_mente_limit",
        description_template="use no máximo {max_count} palavras terminadas em -mente",
        kwargs_generator=gen_terminacao_mente_limit,
        category="pattern"
    ),
    "pattern:terminacao_mente_min": InstructionTemplate(
        id="pattern:terminacao_mente_min",
        description_template="use pelo menos {min_count} palavras terminadas em -mente",
        kwargs_generator=gen_terminacao_mente_min,
        category="pattern"
    ),
    "pattern:terminacao_mente_proibido": InstructionTemplate(
        id="pattern:terminacao_mente_proibido",
        description_template="NÃO use palavras terminadas em -mente",
        kwargs_generator=gen_empty,
        category="pattern"
    ),

    "words:conjunction_count": InstructionTemplate(
        id="words:conjunction_count",
        description_template="use pelo menos {N} conjunções (e, mas, ou, porém, contudo, etc.)",
        kwargs_generator=gen_conjunction_count,
        category="words"
    ),
    "words:connective": InstructionTemplate(
        id="words:connective",
        description_template="use pelo menos {min_connectives} conectivos (portanto, assim, além disso, etc.)",
        kwargs_generator=gen_connective_min,
        category="words"
    ),
    "words:temporal_marker": InstructionTemplate(
        id="words:temporal_marker",
        description_template="use pelo menos {min_markers} marcadores temporais (primeiro, depois, então, finalmente, etc.)",
        kwargs_generator=gen_temporal_marker,
        category="words"
    ),
    "words:contrast_marker": InstructionTemplate(
        id="words:contrast_marker",
        description_template="inclua pelo menos um marcador de contraste (porém, contudo, no entanto, por outro lado, etc.)",
        kwargs_generator=gen_contrast_marker,
        category="words"
    ),
    "words:max_word_repeat": InstructionTemplate(
        id="words:max_word_repeat",
        description_template="nenhuma palavra pode se repetir mais de {N} vezes",
        kwargs_generator=gen_max_word_repeat,
        category="words"
    ),
}

EASY_INSTRUCTIONS = [
    # Contagens simples
    "count:min_word_count",
    "count:max_word_count",
    "count:min_sentence_count",
    "count:min_paragraph_count",
    # Proibições simples
    "forbidden:no_questions",
    "forbidden:no_exclamations",
    "forbidden:no_numbers",
    # Formato simples
    "format:title_case_start",
    "format:bullet_list",
    # Estrutura simples
    "structure:start_with_word",
    # Palavras
    "words:include_word",
    "words:connective",
    # Padrões
    "pattern:terminacao_ando_endo_indo_limit",
    "pattern:terminacao_mente_limit",
]

MEDIUM_COMBINATIONS = [
    # Contagem + Proibição
    ["count:word_count_range", "forbidden:no_questions"],
    ["count:word_count_range", "forbidden:no_exclamations"],
    ["count:min_word_count", "forbidden:word"],
    ["count:min_sentence_count", "forbidden:no_first_person"],

    # Contagem + Formato
    ["count:word_count_range", "format:bullet_list"],
    ["count:sentence_count_range", "format:numbered_list"],
    ["count:min_paragraph_count", "punctuation:use_semicolon"],

    # Contagem + Padrão
    ["count:word_count_range", "pattern:terminacao_ando_endo_indo_limit"],
    ["count:min_word_count", "pattern:terminacao_mente_limit"],
    ["count:unique_word_count", "pattern:terminacao_inho_inha_min"],

    # Formato + Proibição
    ["format:bullet_list", "forbidden:no_numbers"],
    ["format:numbered_list", "forbidden:no_questions"],
    ["structure:start_with_word", "forbidden:no_exclamations"],

    # Palavras + Proibição
    ["words:include_word", "forbidden:word"],
    ["words:connective", "forbidden:no_first_person"],
    ["words:temporal_marker", "forbidden:no_questions"],

    # Pontuação + Contagem
    ["punctuation:include_quote", "count:min_sentence_count"],
    ["punctuation:use_semicolon", "count:min_paragraph_count"],
    ["punctuation:include_question", "count:word_count_range"],

    # Padrões + Outros
    ["pattern:terminacao_ando_endo_indo_min", "words:connective"],
    ["pattern:terminacao_mente_min", "words:include_word"],
    ["pattern:terminacao_ao_oes_min", "count:min_word_count"],

    # Estrutura + Contagem
    ["structure:start_with_word", "count:word_count_range"],
    ["structure:end_with_word", "count:min_sentence_count"],
    ["structure:no_repeat_sentence_start", "count:min_paragraph_count"],
]

HARD_COMBINATIONS = [
    # Triplas com contagem exata
    ["count:exact_word_count", "forbidden:no_questions", "forbidden:no_exclamations"],
    ["count:exact_sentence_count", "pattern:terminacao_mente_limit", "words:connective"],
    ["count:exact_paragraph_count", "structure:start_with_word", "forbidden:word"],

    # Triplas com múltiplas proibições
    ["forbidden:no_first_person", "forbidden:no_questions", "count:word_count_range"],
    ["forbidden:word", "forbidden:no_numbers", "pattern:terminacao_ando_endo_indo_limit"],
    ["forbidden:words_list", "forbidden:no_exclamations", "count:min_sentence_count"],

    # Triplas com padrões complexos
    ["pattern:terminacao_inho_inha_min", "pattern:terminacao_mente_limit", "count:word_count_range"],
    ["pattern:terminacao_ao_oes_min", "words:temporal_marker", "forbidden:no_first_person"],
    ["pattern:terminacao_ando_endo_indo_min", "words:contrast_marker", "punctuation:include_quote"],

    # Triplas com estrutura
    ["structure:start_end_same_word", "count:min_paragraph_count", "forbidden:no_questions"],
    ["structure:no_repeat_sentence_start", "count:sentence_count_range", "words:connective"],
    ["structure:each_line_starts_with", "count:exact_line_count", "forbidden:no_numbers"],

    # Triplas com formato
    ["format:all_caps", "count:word_count_range", "forbidden:no_questions"],
    ["format:all_lowercase", "count:min_sentence_count", "words:include_word"],
    ["format:bullet_list", "count:min_paragraph_count", "pattern:terminacao_mente_limit"],

    # Triplas com palavras obrigatórias
    ["words:include_words", "count:word_count_range", "forbidden:no_first_person"],
    ["words:word_frequency", "pattern:terminacao_ando_endo_indo_limit", "forbidden:no_exclamations"],
    ["words:max_word_repeat", "count:unique_word_count", "forbidden:word"],

    # Quádruplas - máxima dificuldade
    ["count:word_count_range", "forbidden:no_questions", "forbidden:no_first_person", "pattern:terminacao_mente_limit"],
    ["count:exact_paragraph_count", "structure:start_with_word", "words:connective", "forbidden:word"],
    ["pattern:terminacao_inho_inha_min", "words:temporal_marker", "count:min_sentence_count", "forbidden:no_exclamations"],
    ["count:character_count_range", "words:include_word", "forbidden:no_numbers", "punctuation:use_semicolon"],
    ["structure:acrostic", "count:exact_line_count", "forbidden:no_questions", "pattern:terminacao_mente_proibido"],
    ["count:exact_word_count", "words:max_word_repeat", "forbidden:no_first_person", "words:contrast_marker"],
]

TASK_TEMPLATES = [
    "Escreva uma análise crítica de '{title}' de {author}, explorando como a obra aborda {theme}.",
    "Produza uma análise mostrando como '{title}' dialoga com questões de {theme}.",
    "Elabore um texto analítico sobre '{title}', explorando como {author} aborda {theme}.",
    "Escreva uma carta para um clube de leitura convidando o grupo a debater '{title}', destacando {theme}.",
    "Redija uma apresentação de '{title}' para um grupo de leitura, explicando como {author} trata {theme}.",
    "Escreva um comentário sobre '{title}' para um grupo de leitura, destacando {theme}.",
    "Apresente '{title}' de {author} como mediador de um clube de leitura, focando em {theme}.",
    "Escreva uma resenha de '{title}' que explore como a obra de {author} aborda {theme}.",
    "Produza uma breve resenha crítica de '{title}', analisando o tratamento de {theme}.",
    "Reflita sobre como '{title}' de {author} contribui para discussões sobre {theme}.",
    "Discuta a importância de '{title}' para a literatura brasileira, considerando {theme}.",
    "Analise como '{title}' representa {theme} na literatura brasileira do período.",
    "Compare a abordagem de {theme} em '{title}' com outras obras de {author}.",
]

THEMES = [
    "identidade e pertencimento",
    "desigualdade social",
    "relações humanas e conflitos",
    "memória e narrativa",
    "sobrevivência e resistência",
    "tradição e modernidade",
    "amor e ciúme",
    "poder e opressão",
    "natureza e civilização",
    "busca por sentido",
    "marginalização e exclusão",
    "ambiguidade moral",
    "transformação social",
    "a condição humana",
    "o papel da mulher na sociedade",
    "a religiosidade popular",
    "o sertão e a cidade",
]


MULTI_TURN_TEMPLATES = {
    "expansion": [
        {
            "turn_1": "Apresente brevemente a obra '{title}' de {author}.",
            "turn_2": "Agora aprofunde a análise, focando em {theme}.",
            "turn_3": "Para concluir, compare esta obra com outra do mesmo período literário.",
        },
        {
            "turn_1": "Descreva o contexto histórico em que '{title}' foi escrita.",
            "turn_2": "Relacione esse contexto com a temática de {theme} presente na obra.",
            "turn_3": "Explique como essa temática ainda é relevante na atualidade.",
        },
    ],
    "deepening": [
        {
            "turn_1": "Quem é o protagonista de '{title}'? Descreva suas características.",
            "turn_2": "Como esse personagem se relaciona com o tema de {theme}?",
            "turn_3": "Analise a evolução desse personagem ao longo da narrativa.",
        },
        {
            "turn_1": "Qual é o estilo narrativo utilizado em '{title}'?",
            "turn_2": "Como essa escolha narrativa influencia a percepção de {theme}?",
            "turn_3": "Compare com outra obra que use um estilo diferente.",
        },
    ],
    "critical": [
        {
            "turn_1": "Identifique o principal recurso literário usado em '{title}'.",
            "turn_2": "Explique como esse recurso contribui para a representação de {theme}.",
            "turn_3": "Apresente uma análise crítica sobre a eficácia desse recurso.",
        },
        {
            "turn_1": "A qual movimento literário pertence '{title}'?",
            "turn_2": "Quais características desse movimento estão presentes na abordagem de {theme}?",
            "turn_3": "Critique ou defenda a classificação da obra nesse movimento.",
        },
    ],
}

MULTI_TURN_INSTRUCTIONS = {
    "turn_1": [
        ["count:word_count_range"],
        ["count:min_word_count"],
        ["forbidden:no_questions"],
        ["structure:start_with_word"],
        ["words:include_word"],
    ],
    "turn_2": [
        ["words:connective"],
        ["pattern:terminacao_mente_limit"],
        ["forbidden:word"],
        ["punctuation:include_quote"],
        ["words:contrast_marker"],
    ],
    "turn_3": [
        ["forbidden:no_first_person"],
        ["count:min_paragraph_count"],
        ["words:temporal_marker"],
        ["pattern:terminacao_ando_endo_indo_limit"],
        ["structure:no_repeat_sentence_start"],
    ],
}


class QuestionGenerator:
    def __init__(self, book_context_path: str):
        with open(book_context_path, "r", encoding="utf-8") as f:
            self.books = json.load(f)
        self.key_counter = 0

    def _get_random_book(self) -> dict:
        return random.choice(self.books)

    def _build_instruction_description(self, instruction_ids: list[str], kwargs_list: list[dict]) -> str:
        """Constrói a descrição das instruções para o prompt."""
        descriptions = []
        for inst_id, kwargs in zip(instruction_ids, kwargs_list):
            template = INSTRUCTIONS[inst_id]

            format_kwargs = kwargs.copy()

            if "words" in format_kwargs and isinstance(format_kwargs["words"], list):
                format_kwargs["words_str"] = ", ".join(f'"{w}"' for w in format_kwargs["words"])
            if "forbidden_words" in format_kwargs and isinstance(format_kwargs["forbidden_words"], list):
                format_kwargs["forbidden_words_str"] = ", ".join(f'"{w}"' for w in format_kwargs["forbidden_words"])

            desc = template.description_template.format(**format_kwargs)
            descriptions.append(desc)

        if len(descriptions) == 1:
            return f"Siga estritamente: {descriptions[0]}."
        else:
            joined = "; ".join(descriptions[:-1]) + f"; e {descriptions[-1]}"
            return f"Siga estritamente: {joined}."

    def _generate_kwargs(self, instruction_ids: list[str]) -> list[dict]:
        """Gera kwargs para cada instrução."""
        kwargs_list = []
        for inst_id in instruction_ids:
            template = INSTRUCTIONS[inst_id]
            kwargs = template.kwargs_generator()
            kwargs_list.append(kwargs)
        return kwargs_list

    def generate_question(self, difficulty: str) -> dict:
        """Gera uma questão com o nível de dificuldade especificado."""
        book = self._get_random_book()
        theme = random.choice(THEMES)
        task_template = random.choice(TASK_TEMPLATES)

        if difficulty == "easy":
            instruction_ids = [random.choice(EASY_INSTRUCTIONS)]
        elif difficulty == "medium":
            instruction_ids = list(random.choice(MEDIUM_COMBINATIONS))
        else:  # hard
            instruction_ids = list(random.choice(HARD_COMBINATIONS))

        kwargs_list = self._generate_kwargs(instruction_ids)

        task = task_template.format(
            title=book["title"],
            author=book["author"],
            theme=theme
        )
        instruction_desc = self._build_instruction_description(instruction_ids, kwargs_list)
        prompt = f"{task} {instruction_desc}"

        question = {
            "key": self.key_counter,
            "prompt": prompt,
            "instruction_id_list": instruction_ids,
            "kwargs": kwargs_list,
            "difficulty": difficulty,
            "book": book["title"],
            "num_instructions": len(instruction_ids),
        }

        self.key_counter += 1
        return question

    def generate_multi_turn_question(self) -> dict:
        """Gera uma questão multi-turn com 3 turnos progressivos."""
        book = self._get_random_book()
        theme = random.choice(THEMES)

        conversation_type = random.choice(list(MULTI_TURN_TEMPLATES.keys()))
        template = random.choice(MULTI_TURN_TEMPLATES[conversation_type])

        turns = []
        accumulated_instructions = []
        accumulated_kwargs = []

        for turn_num in range(1, 4):
            turn_key = f"turn_{turn_num}"

            turn_prompt = template[turn_key].format(
                title=book["title"],
                author=book["author"],
                theme=theme
            )

            new_instructions = random.choice(MULTI_TURN_INSTRUCTIONS[turn_key])
            new_kwargs = self._generate_kwargs(new_instructions)

            accumulated_instructions.extend(new_instructions)
            accumulated_kwargs.extend(new_kwargs)

            instruction_desc = self._build_instruction_description(
                accumulated_instructions, accumulated_kwargs
            )

            full_prompt = f"{turn_prompt} {instruction_desc}"

            turns.append({
                "turn": turn_num,
                "prompt": full_prompt,
                "instruction_id_list": list(accumulated_instructions),
                "kwargs": list(accumulated_kwargs),
                "new_instructions": new_instructions,
            })

        question = {
            "key": self.key_counter,
            "conversation_type": conversation_type,
            "book": book["title"],
            "theme": theme,
            "turns": turns,
            "total_instructions": len(accumulated_instructions),
            "is_multi_turn": True,
        }

        self.key_counter += 1
        return question

    def generate_dataset(
        self,
        easy_count: int = 100,
        medium_count: int = 100,
        hard_count: int = 100,
        shuffle: bool = True
    ) -> list[dict]:
        """Gera um dataset completo com questões de todos os níveis."""
        questions = []

        for _ in range(easy_count):
            questions.append(self.generate_question("easy"))

        for _ in range(medium_count):
            questions.append(self.generate_question("medium"))

        for _ in range(hard_count):
            questions.append(self.generate_question("hard"))

        if shuffle:
            random.shuffle(questions)
            for i, q in enumerate(questions):
                q["key"] = i

        return questions

    def generate_multi_turn_dataset(self, count: int = 100, shuffle: bool = True) -> list[dict]:
        """Gera um dataset de questões multi-turn."""
        questions = []

        for _ in range(count):
            questions.append(self.generate_multi_turn_question())

        if shuffle:
            random.shuffle(questions)
            for i, q in enumerate(questions):
                q["key"] = i

        return questions


def main():
    parser = argparse.ArgumentParser(description="Gera questões do Capitu com níveis de dificuldade.")
    parser.add_argument("--book_context", default="data/book_context.json", help="Caminho para book_context.json")
    parser.add_argument("--output", default="data/input_questions.jsonl", help="Arquivo de saída JSONL")
    parser.add_argument("--easy", type=int, default=70, help="Número de questões fáceis")
    parser.add_argument("--medium", type=int, default=70, help="Número de questões médias")
    parser.add_argument("--hard", type=int, default=60, help="Número de questões difíceis")
    parser.add_argument("--seed", type=int, default=42, help="Seed para reprodutibilidade")
    parser.add_argument("--no_shuffle", action="store_true", help="Não embaralhar questões")

    parser.add_argument("--multi_turn", action="store_true", help="Gerar dataset multi-turn")
    parser.add_argument("--turns", type=int, default=100, help="Número de conversas multi-turn")

    args = parser.parse_args()

    random.seed(args.seed)

    generator = QuestionGenerator(args.book_context)

    if args.multi_turn:
        questions = generator.generate_multi_turn_dataset(
            count=args.turns,
            shuffle=not args.no_shuffle
        )
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + "\n")

        print(f"Dataset multi-turn gerado: {output_path}")
        print(f"  Total: {len(questions)} conversas")
        print(f"  Turnos por conversa: 3")

        type_counts = {}
        for q in questions:
            t = q["conversation_type"]
            type_counts[t] = type_counts.get(t, 0) + 1
        print("\nDistribuição por tipo de conversa:")
        for t, count in sorted(type_counts.items()):
            print(f"  {t}: {count}")
    else:
        questions = generator.generate_dataset(
            easy_count=args.easy,
            medium_count=args.medium,
            hard_count=args.hard,
            shuffle=not args.no_shuffle
        )

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + "\n")

        easy_count = sum(1 for q in questions if q["difficulty"] == "easy")
        medium_count = sum(1 for q in questions if q["difficulty"] == "medium")
        hard_count = sum(1 for q in questions if q["difficulty"] == "hard")

        print(f"Dataset gerado: {output_path}")
        print(f"  Total: {len(questions)} questões")
        print(f"  Fácil: {easy_count} (1 instrução)")
        print(f"  Médio: {medium_count} (2 instruções)")
        print(f"  Difícil: {hard_count} (3-4 instruções)")

        book_counts = {}
        for q in questions:
            book_counts[q["book"]] = book_counts.get(q["book"], 0) + 1
        print("\nDistribuição por obra:")
        for book, count in sorted(book_counts.items()):
            print(f"  {book}: {count}")

        instruction_counts = {}
        for q in questions:
            for inst in q["instruction_id_list"]:
                instruction_counts[inst] = instruction_counts.get(inst, 0) + 1
        print(f"\nInstruções únicas usadas: {len(instruction_counts)}")
        print("\nTop 10 instruções mais usadas:")
        sorted_instructions = sorted(instruction_counts.items(), key=lambda x: -x[1])[:10]
        for inst, count in sorted_instructions:
            print(f"  {inst}: {count}")


if __name__ == "__main__":
    main()
