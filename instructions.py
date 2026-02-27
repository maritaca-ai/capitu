"""
Biblioteca de instruções para o Capitu.

Instruções verificáveis automaticamente para português brasileiro.
Foco em verificação determinística sem ambiguidade.
"""

import logging
import random
import re
import string
from typing import Dict, Optional, Sequence, Union
from collections import Counter

logger = logging.getLogger(__name__)

_InstructionArgsDtype = Optional[Dict[str, Union[int, str, Sequence[str]]]]

# Pronomes de primeira pessoa
_PRONOMES_PRIMEIRA_PESSOA = [
    "eu", "me", "mim", "comigo", "meu", "minha", "meus", "minhas",
    "nós", "nos", "conosco", "nosso", "nossa", "nossos", "nossas",
]

# Pronomes de segunda pessoa
_PRONOMES_SEGUNDA_PESSOA = [
    "tu", "te", "ti", "contigo", "teu", "tua", "teus", "tuas",
    "você", "vocês", "vós", "convosco", "vosso", "vossa", "vossos", "vossas",
]

# Pronomes de terceira pessoa
_PRONOMES_TERCEIRA_PESSOA = [
    "ele", "ela", "eles", "elas", "lhe", "lhes", "o", "a", "os", "as",
    "si", "consigo", "seu", "sua", "seus", "suas", "dele", "dela", "deles", "delas",
]

# Conjunções coordenativas em português
_CONJUNCOES_COORDENATIVAS = [
    "e", "nem", "mas", "porém", "contudo", "todavia", "entretanto", "no entanto",
    "ou", "ora", "quer", "seja", "pois", "logo", "portanto", "por isso",
    "assim", "então", "por conseguinte", "porque",
]

# Conjunções subordinativas em português
_CONJUNCOES_SUBORDINATIVAS = [
    "que", "se", "porque", "como", "quando", "enquanto", "embora", "embora",
    "caso", "conforme", "consoante", "segundo", "conquanto", "posto que",
    "visto que", "já que", "uma vez que", "dado que", "desde que",
    "a fim de que", "para que", "a menos que", "salvo se", "exceto se",
]

_CONECTIVOS = [
    # Causa / consequência
    "portanto", "por isso", "logo", "então", "assim",
    "dessa forma", "desse modo", "deste modo",
    "por conseguinte", "consequentemente",
    "sendo assim", "em consequência", "em decorrência",
    "diante disso", "por essa razão", "com isso",
    # Adição
    "além disso", "ademais", "outrossim",
    "da mesma forma", "do mesmo modo",
    # Oposição / concessão
    "contudo", "todavia", "entretanto", "porém",
    "no entanto", "em contrapartida", "por outro lado",
    "apesar disso", "não obstante", "ainda assim", "mesmo assim",
    "ao contrário",
    # Conclusão / resumo
    "em suma", "em síntese", "em resumo", "enfim", "por fim",
    "em conclusão", "finalmente", "afinal", "em última análise",
    # Sequência / ordem
    "primeiramente", "em primeiro lugar", "em segundo lugar",
    "em seguida", "posteriormente",
    # Direção / acordo
    "nesse sentido", "neste sentido",
    # Reformulação / explicação
    "ou seja", "isto é", "em outras palavras",
    # Confirmação / ênfase
    "de fato", "com efeito", "sobretudo",
    # Transição
    "por sua vez", "de qualquer forma",
]

# Preposições em português
_PREPOSICOES = [
    "a", "ante", "após", "até", "com", "contra", "de", "desde",
    "em", "entre", "para", "perante", "por", "sem", "sob", "sobre", "trás",
]

# Stop words em português (palavras muito frequentes)
_STOP_WORDS_PT = [
    "o", "a", "os", "as", "um", "uma", "uns", "umas",
    "de", "da", "do", "das", "dos", "em", "na", "no", "nas", "nos",
    "por", "para", "com", "sem", "sob", "sobre",
    "e", "ou", "mas", "que", "se", "como", "quando",
    "é", "são", "foi", "eram", "ser", "estar", "ter", "haver",
    "este", "esta", "esse", "essa", "aquele", "aquela",
    "isto", "isso", "aquilo", "mesmo", "próprio",
    "muito", "pouco", "mais", "menos", "bem", "mal",
    "já", "ainda", "sempre", "nunca", "também", "só", "apenas",
]

# Palavras comuns proibíveis
_PALAVRAS_PROIBIBEIS = [
    "muito", "sempre", "nunca", "talvez", "realmente",
    "basicamente", "obviamente", "certamente", "definitivamente",
    "interessante", "importante", "fundamental", "essencial",
    "bom", "ruim", "ótimo", "péssimo", "incrível", "maravilhoso",
    "coisa", "algo", "tudo", "nada", "gente", "pessoa",
]

# Marcadores temporais
_MARCADORES_TEMPORAIS = [
    "primeiro", "primeiramente", "depois", "em seguida", "a seguir",
    "por fim", "finalmente", "inicialmente", "posteriormente",
    "antes", "após", "enquanto", "durante", "simultaneamente",
    "ao mesmo tempo", "mais tarde", "anteriormente", "em breve",
]

# Marcadores de contraste
_MARCADORES_CONTRASTE = [
    "por outro lado", "em contrapartida", "no entanto", "porém",
    "contudo", "todavia", "entretanto", "apesar de", "embora",
    "enquanto", "ao contrário", "diferentemente", "ao passo que",
]

def _contar_palavras(texto: str) -> int:
    """Conta o número de palavras no texto."""
    palavras = texto.split()
    return len(palavras)


def _contar_palavras_unicas(texto: str) -> int:
    """Conta o número de palavras únicas no texto."""
    palavras = texto.lower().split()
    palavras_limpas = set()
    for p in palavras:
        limpa = p.strip(string.punctuation)
        if limpa:
            palavras_limpas.add(limpa)
    return len(palavras_limpas)


def _contar_frases(texto: str) -> int:
    """Conta o número de frases no texto (terminadas em . ! ?).

    Ignora:
    - Prefixos de lista numerada (1., 2., etc.)
    - Abreviações comuns (S.M., Dr., Sr., Sra., etc.)
    """
    texto_limpo = re.sub(r'^\s*\d+\.\s*', '', texto, flags=re.MULTILINE)
    texto_limpo = re.sub(r'^\s*[•\-\*]\s*', '', texto_limpo, flags=re.MULTILINE)

    abreviacoes = [
        r'Dr\.', r'Dra\.', r'Sr\.', r'Sra\.', r'Prof\.', r'Profa\.',
        r'S\.M\.', r'S\.A\.', r'Ltda\.', r'etc\.', r'vol\.', r'n\.º',
        r'p\.', r'pp\.', r'ed\.', r'org\.', r'coord\.'
    ]
    for i, abrev in enumerate(abreviacoes):
        texto_limpo = re.sub(abrev, f'ABREV{i}PLACEHOLDER', texto_limpo, flags=re.IGNORECASE)

    frases = re.split(r'[.!?]+', texto_limpo.strip())
    frases = [f.strip() for f in frases if f.strip() and len(f.strip()) > 2]
    return len(frases)


def _dividir_em_frases(texto: str) -> list:
    """Divide o texto em frases."""
    frases = re.split(r'(?<=[.!?])\s+', texto.strip())
    return [f.strip() for f in frases if f.strip()]


def _contar_paragrafos(texto: str) -> int:
    """Conta o número de parágrafos (separados por linha em branco)."""
    paragrafos = re.split(r'\n\s*\n', texto.strip())
    paragrafos = [p.strip() for p in paragrafos if p.strip()]
    return len(paragrafos)


def _contar_caracteres(texto: str, incluir_espacos: bool = True) -> int:
    """Conta o número de caracteres no texto."""
    if incluir_espacos:
        return len(texto)
    return len(texto.replace(" ", "").replace("\n", "").replace("\t", ""))

class Instruction:
    """Classe base para instruções."""

    def __init__(self, instruction_id):
        self.id = instruction_id

    def build_description(self, **kwargs):
        raise NotImplementedError("`build_description` não implementado.")

    def get_instruction_args(self):
        raise NotImplementedError("`get_instruction_args` não implementado.")

    def get_instruction_args_keys(self):
        raise NotImplementedError("`get_instruction_args_keys` não implementado.")

    def check_following(self, value):
        raise NotImplementedError("`check_following` não implementado.")

class WordCountRangeChecker(Instruction):
    """A resposta deve ter entre X e Y palavras."""

    def build_description(self, *, min_words=None, max_words=None):
        self._min_words = min_words if min_words is not None else random.randint(50, 100)
        self._max_words = max_words if max_words is not None else self._min_words + random.randint(20, 50)

        self._description_pattern = (
            "A resposta deve ter entre {min_words} e {max_words} palavras."
        )
        return self._description_pattern.format(
            min_words=self._min_words, max_words=self._max_words
        )

    def get_instruction_args(self):
        return {"min_words": self._min_words, "max_words": self._max_words}

    def get_instruction_args_keys(self):
        return ["min_words", "max_words"]

    def check_following(self, value):
        num_palavras = _contar_palavras(value)
        return self._min_words <= num_palavras <= self._max_words


class ExactWordCountChecker(Instruction):
    """A resposta deve ter exatamente N palavras."""

    def build_description(self, *, num_words=None, target_words=None):
        effective_words = num_words if num_words is not None else target_words
        self._num_words = effective_words if effective_words is not None else random.choice([50, 75, 100, 150])

        self._description_pattern = (
            "A resposta deve ter EXATAMENTE {num_words} palavras."
        )
        return self._description_pattern.format(num_words=self._num_words)

    def get_instruction_args(self):
        return {"num_words": self._num_words}

    def get_instruction_args_keys(self):
        return ["num_words"]

    def check_following(self, value):
        num_palavras = _contar_palavras(value)
        return num_palavras == self._num_words


class MinWordCountChecker(Instruction):
    """A resposta deve ter pelo menos N palavras."""

    def build_description(self, *, min_words=None):
        self._min_words = min_words if min_words is not None else random.choice([50, 75, 100, 150])

        self._description_pattern = (
            "A resposta deve ter pelo menos {min_words} palavras."
        )
        return self._description_pattern.format(min_words=self._min_words)

    def get_instruction_args(self):
        return {"min_words": self._min_words}

    def get_instruction_args_keys(self):
        return ["min_words"]

    def check_following(self, value):
        num_palavras = _contar_palavras(value)
        return num_palavras >= self._min_words


class MaxWordCountChecker(Instruction):
    """A resposta deve ter no máximo N palavras."""

    def build_description(self, *, max_words=None):
        self._max_words = max_words if max_words is not None else random.choice([100, 150, 200, 250])

        self._description_pattern = (
            "A resposta deve ter no máximo {max_words} palavras."
        )
        return self._description_pattern.format(max_words=self._max_words)

    def get_instruction_args(self):
        return {"max_words": self._max_words}

    def get_instruction_args_keys(self):
        return ["max_words"]

    def check_following(self, value):
        num_palavras = _contar_palavras(value)
        return num_palavras <= self._max_words


class UniqueWordCountChecker(Instruction):
    """A resposta deve usar pelo menos N palavras únicas."""

    def build_description(self, *, N=None, min_unique=None):
        self._min_unique = N if N is not None else (min_unique if min_unique is not None else random.choice([30, 40, 50, 60]))

        self._description_pattern = (
            "Use pelo menos {min_unique} palavras únicas (diferentes) na resposta."
        )
        return self._description_pattern.format(min_unique=self._min_unique)

    def get_instruction_args(self):
        return {"N": self._min_unique, "min_unique": self._min_unique}

    def get_instruction_args_keys(self):
        return ["N", "min_unique"]

    def check_following(self, value):
        num_unicas = _contar_palavras_unicas(value)
        return num_unicas >= self._min_unique


class CharacterCountRangeChecker(Instruction):
    """A resposta deve ter entre X e Y caracteres."""

    def build_description(self, *, min_chars=None, max_chars=None):
        self._min_chars = min_chars if min_chars is not None else random.randint(200, 400)
        self._max_chars = max_chars if max_chars is not None else self._min_chars + random.randint(100, 300)

        self._description_pattern = (
            "A resposta deve ter entre {min_chars} e {max_chars} caracteres."
        )
        return self._description_pattern.format(
            min_chars=self._min_chars, max_chars=self._max_chars
        )

    def get_instruction_args(self):
        return {"min_chars": self._min_chars, "max_chars": self._max_chars}

    def get_instruction_args_keys(self):
        return ["min_chars", "max_chars"]

    def check_following(self, value):
        num_chars = _contar_caracteres(value, incluir_espacos=True)
        return self._min_chars <= num_chars <= self._max_chars

class ExactSentenceCountChecker(Instruction):
    """A resposta deve ter exatamente N frases."""

    def build_description(self, *, num_sentences=None, N=None):
        effective = num_sentences if num_sentences is not None else N
        self._num_sentences = effective if effective is not None else random.choice([3, 4, 5, 6, 7, 8])

        self._description_pattern = (
            "A resposta deve ter EXATAMENTE {num_sentences} frases."
        )
        return self._description_pattern.format(num_sentences=self._num_sentences)

    def get_instruction_args(self):
        return {"num_sentences": self._num_sentences}

    def get_instruction_args_keys(self):
        return ["num_sentences"]

    def check_following(self, value):
        num_frases = _contar_frases(value)
        return num_frases == self._num_sentences


class MinSentenceCountChecker(Instruction):
    """A resposta deve ter pelo menos N frases."""

    def build_description(self, *, min_sentences=None, N=None):
        effective = min_sentences if min_sentences is not None else N
        self._min_sentences = effective if effective is not None else random.choice([3, 4, 5, 6])

        self._description_pattern = (
            "A resposta deve ter pelo menos {min_sentences} frases."
        )
        return self._description_pattern.format(min_sentences=self._min_sentences)

    def get_instruction_args(self):
        return {"min_sentences": self._min_sentences}

    def get_instruction_args_keys(self):
        return ["min_sentences"]

    def check_following(self, value):
        num_frases = _contar_frases(value)
        return num_frases >= self._min_sentences


class SentenceCountRangeChecker(Instruction):
    """A resposta deve ter entre X e Y frases."""

    def build_description(self, *, min_sentences=None, max_sentences=None):
        self._min_sentences = min_sentences if min_sentences is not None else random.randint(3, 5)
        self._max_sentences = max_sentences if max_sentences is not None else self._min_sentences + random.randint(2, 4)

        self._description_pattern = (
            "A resposta deve ter entre {min_sentences} e {max_sentences} frases."
        )
        return self._description_pattern.format(
            min_sentences=self._min_sentences, max_sentences=self._max_sentences
        )

    def get_instruction_args(self):
        return {"min_sentences": self._min_sentences, "max_sentences": self._max_sentences}

    def get_instruction_args_keys(self):
        return ["min_sentences", "max_sentences"]

    def check_following(self, value):
        num_frases = _contar_frases(value)
        return self._min_sentences <= num_frases <= self._max_sentences


class ExactParagraphCountChecker(Instruction):
    """A resposta deve ter exatamente N parágrafos."""

    def build_description(self, *, num_paragraphs=None):
        self._num_paragraphs = num_paragraphs if num_paragraphs is not None else random.choice([2, 3, 4])

        self._description_pattern = (
            "A resposta deve ter EXATAMENTE {num_paragraphs} parágrafos (separados por linha em branco)."
        )
        return self._description_pattern.format(num_paragraphs=self._num_paragraphs)

    def get_instruction_args(self):
        return {"num_paragraphs": self._num_paragraphs}

    def get_instruction_args_keys(self):
        return ["num_paragraphs"]

    def check_following(self, value):
        num_paragrafos = _contar_paragrafos(value)
        return num_paragrafos == self._num_paragraphs


class MinParagraphCountChecker(Instruction):
    """A resposta deve ter pelo menos N parágrafos."""

    def build_description(self, *, min_paragraphs=None):
        self._min_paragraphs = min_paragraphs if min_paragraphs is not None else random.choice([2, 3, 4])

        self._description_pattern = (
            "A resposta deve ter pelo menos {min_paragraphs} parágrafos (separados por linha em branco)."
        )
        return self._description_pattern.format(min_paragraphs=self._min_paragraphs)

    def get_instruction_args(self):
        return {"min_paragraphs": self._min_paragraphs}

    def get_instruction_args_keys(self):
        return ["min_paragraphs"]

    def check_following(self, value):
        num_paragrafos = _contar_paragrafos(value)
        return num_paragrafos >= self._min_paragraphs


class MaxSentenceLengthChecker(Instruction):
    """Cada frase deve ter no máximo N palavras."""

    def build_description(self, *, max_words_per_sentence=None):
        self._max_words = max_words_per_sentence if max_words_per_sentence is not None else random.choice([15, 20, 25, 30])

        self._description_pattern = (
            "Cada frase deve ter no máximo {max_words} palavras."
        )
        return self._description_pattern.format(max_words=self._max_words)

    def get_instruction_args(self):
        return {"max_words_per_sentence": self._max_words}

    def get_instruction_args_keys(self):
        return ["max_words_per_sentence"]

    def check_following(self, value):
        frases = re.split(r'[.!?]+', value)
        for frase in frases:
            frase = frase.strip()
            if frase:
                num_palavras = len(frase.split())
                if num_palavras > self._max_words:
                    return False
        return True


class MinSentenceLengthChecker(Instruction):
    """Cada frase deve ter pelo menos N palavras."""

    def build_description(self, *, min_words_per_sentence=None):
        self._min_words = min_words_per_sentence if min_words_per_sentence is not None else random.choice([5, 8, 10])

        self._description_pattern = (
            "Cada frase deve ter pelo menos {min_words} palavras."
        )
        return self._description_pattern.format(min_words=self._min_words)

    def get_instruction_args(self):
        return {"min_words_per_sentence": self._min_words}

    def get_instruction_args_keys(self):
        return ["min_words_per_sentence"]

    def check_following(self, value):
        frases = re.split(r'[.!?]+', value)
        frases = [f.strip() for f in frases if f.strip()]
        if not frases:
            return False
        for frase in frases:
            num_palavras = len(frase.split())
            if num_palavras < self._min_words:
                return False
        return True

class ExactNumberCountChecker(Instruction):
    """A resposta deve conter exatamente N números."""

    def build_description(self, *, N=None, num_numbers=None):
        self._num_numbers = N if N is not None else (num_numbers if num_numbers is not None else random.choice([1, 2, 3, 4, 5]))

        self._description_pattern = (
            "A resposta deve conter exatamente {num_numbers} números."
        )
        return self._description_pattern.format(num_numbers=self._num_numbers)

    def get_instruction_args(self):
        return {"N": self._num_numbers, "num_numbers": self._num_numbers}

    def get_instruction_args_keys(self):
        return ["N", "num_numbers"]

    def check_following(self, value):
        numeros = re.findall(r'\d+', value)
        return len(numeros) == self._num_numbers


class MinNumberCountChecker(Instruction):
    """A resposta deve conter pelo menos N números."""

    def build_description(self, *, min_numbers=None):
        self._min_numbers = min_numbers if min_numbers is not None else random.choice([1, 2, 3])

        self._description_pattern = (
            "A resposta deve conter pelo menos {min_numbers} números."
        )
        return self._description_pattern.format(min_numbers=self._min_numbers)

    def get_instruction_args(self):
        return {"min_numbers": self._min_numbers}

    def get_instruction_args_keys(self):
        return ["min_numbers"]

    def check_following(self, value):
        numeros = re.findall(r'\d+', value)
        return len(numeros) >= self._min_numbers


class NoNumbersChecker(Instruction):
    """A resposta não deve conter números."""

    def build_description(self):
        self._description_pattern = (
            "NÃO use números (algarismos) na resposta."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        return not bool(re.search(r'\d', value))


class IncludeSpecificNumberChecker(Instruction):
    """A resposta deve mencionar um número específico."""

    def build_description(self, *, number=None):
        self._number = number if number is not None else random.choice([1899, 1956, 1928, 1865, 1890, 1937, 1938, 1977])

        self._description_pattern = (
            "A resposta deve mencionar o número {number}."
        )
        return self._description_pattern.format(number=self._number)

    def get_instruction_args(self):
        return {"number": self._number}

    def get_instruction_args_keys(self):
        return ["number"]

    def check_following(self, value):
        return str(self._number) in value

class IncludeWordChecker(Instruction):
    """A resposta deve incluir uma palavra específica."""

    def build_description(self, *, word=None, keyword=None):
        self._word = word if word is not None else (keyword if keyword is not None else random.choice(["literatura", "narrativa", "autor", "obra", "personagem"]))

        self._description_pattern = (
            'A resposta deve incluir a palavra "{word}".'
        )
        return self._description_pattern.format(word=self._word)

    def get_instruction_args(self):
        return {"word": self._word, "keyword": self._word}

    def get_instruction_args_keys(self):
        return ["word", "keyword"]

    def check_following(self, value):
        pattern = r'\b' + re.escape(self._word.lower()) + r'\b'
        return bool(re.search(pattern, value.lower()))


class IncludeWordsChecker(Instruction):
    """A resposta deve incluir todas as palavras de uma lista."""

    def build_description(self, *, words=None):
        if words is None:
            self._words = random.sample(["literatura", "narrativa", "autor", "obra", "personagem", "história", "texto"], 2)
        else:
            self._words = words if isinstance(words, list) else [words]

        palavras_str = ", ".join(f'"{w}"' for w in self._words)
        self._description_pattern = (
            "A resposta deve incluir TODAS as seguintes palavras: {words}."
        )
        return self._description_pattern.format(words=palavras_str)

    def get_instruction_args(self):
        return {"words": self._words}

    def get_instruction_args_keys(self):
        return ["words"]

    def check_following(self, value):
        texto = value.lower()
        for word in self._words:
            pattern = r'\b' + re.escape(word.lower()) + r'\b'
            if not re.search(pattern, texto):
                return False
        return True


class WordFrequencyChecker(Instruction):
    """A resposta deve usar uma palavra específica exatamente N vezes."""

    def build_description(self, *, word=None, count=None, min_count=None):
        self._word = word if word is not None else random.choice(["texto", "obra", "autor", "livro", "narrativa"])
        effective_count = count if count is not None else min_count
        self._count = effective_count if effective_count is not None else random.choice([2, 3, 4, 5])

        self._description_pattern = (
            'Use a palavra "{word}" EXATAMENTE {count} vezes na resposta.'
        )
        return self._description_pattern.format(word=self._word, count=self._count)

    def get_instruction_args(self):
        return {"word": self._word, "count": self._count}

    def get_instruction_args_keys(self):
        return ["word", "count"]

    def check_following(self, value):
        pattern = r'\b' + re.escape(self._word.lower()) + r'\b'
        matches = re.findall(pattern, value.lower())
        return len(matches) == self._count


class MinWordFrequencyChecker(Instruction):
    """A resposta deve usar uma palavra específica pelo menos N vezes."""

    def build_description(self, *, word=None, min_count=None):
        self._word = word if word is not None else random.choice(["texto", "obra", "autor", "livro", "narrativa"])
        self._min_count = min_count if min_count is not None else random.choice([2, 3, 4])

        self._description_pattern = (
            'Use a palavra "{word}" pelo menos {min_count} vezes na resposta.'
        )
        return self._description_pattern.format(word=self._word, min_count=self._min_count)

    def get_instruction_args(self):
        return {"word": self._word, "min_count": self._min_count}

    def get_instruction_args_keys(self):
        return ["word", "min_count"]

    def check_following(self, value):
        pattern = r'\b' + re.escape(self._word.lower()) + r'\b'
        matches = re.findall(pattern, value.lower())
        return len(matches) >= self._min_count


class ForbiddenWordChecker(Instruction):
    """A resposta não deve conter uma palavra específica."""

    def build_description(self, *, forbidden_word=None):
        self._forbidden_word = forbidden_word if forbidden_word is not None else random.choice(_PALAVRAS_PROIBIBEIS)

        self._description_pattern = (
            'NÃO use a palavra "{forbidden_word}" na resposta.'
        )
        return self._description_pattern.format(forbidden_word=self._forbidden_word)

    def get_instruction_args(self):
        return {"forbidden_word": self._forbidden_word}

    def get_instruction_args_keys(self):
        return ["forbidden_word"]

    def check_following(self, value):
        pattern = r'\b' + re.escape(self._forbidden_word.lower()) + r'\b'
        return not bool(re.search(pattern, value.lower()))


class ForbiddenWordsListChecker(Instruction):
    """A resposta não deve conter nenhuma palavra de uma lista."""

    def build_description(self, *, forbidden_words=None):
        if forbidden_words is None:
            self._forbidden_words = random.sample(_PALAVRAS_PROIBIBEIS, 3)
        else:
            self._forbidden_words = forbidden_words if isinstance(forbidden_words, list) else [forbidden_words]

        palavras_str = ", ".join(f'"{w}"' for w in self._forbidden_words)
        self._description_pattern = (
            "NÃO use nenhuma das seguintes palavras: {words}."
        )
        return self._description_pattern.format(words=palavras_str)

    def get_instruction_args(self):
        return {"forbidden_words": self._forbidden_words}

    def get_instruction_args_keys(self):
        return ["forbidden_words"]

    def check_following(self, value):
        texto = value.lower()
        for word in self._forbidden_words:
            pattern = r'\b' + re.escape(word.lower()) + r'\b'
            if re.search(pattern, texto):
                return False
        return True



def _is_nos_contraction(texto: str, match_start: int, match_end: int) -> bool:
    """Verifica se 'nos' é contração de 'em + os' (não pronome).

    Heurísticas:
    - Se 'nos' é seguido por palavra que parece substantivo/adjetivo plural
      (terminada em -os, -as, -es, -is, -ões, -ães), é provavelmente contração.
    - Se 'nos' está no início de frase seguido de substantivo, é contração.
    """
    resto = texto[match_end:].lstrip()
    if not resto:
        return False

    # Pega a próxima palavra
    proxima = re.match(r'[a-záéíóúâêôãõç]+', resto, re.IGNORECASE)
    if not proxima:
        return False

    palavra = proxima.group().lower()

    # Padrões de substantivos/adjetivos plurais (indicam contração)
    padroes_plural = [
        r'.*os$',   # livros, afetos, momentos
        r'.*as$',   # casas, pessoas, coisas
        r'.*es$',   # meses, papéis, animais
        r'.*is$',   # animais, papéis
        r'.*ões$',  # corações, ações
        r'.*ães$',  # pães, cães
    ]

    # Se a próxima palavra parece plural, 'nos' é provavelmente contração
    for padrao in padroes_plural:
        if re.match(padrao, palavra):
            # Exceções: palavras que são verbos mesmo terminando em plural
            verbos_excecao = ['vamos', 'vemos', 'temos', 'somos', 'estamos',
                             'fazemos', 'dizemos', 'sabemos', 'podemos', 'queremos']
            if palavra not in verbos_excecao:
                return True

    return False


class NoFirstPersonChecker(Instruction):
    """A resposta não deve usar pronomes de primeira pessoa."""

    def build_description(self):
        self._description_pattern = (
            "NÃO use pronomes de primeira pessoa (eu, me, mim, meu, nós, nosso, etc.)."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        texto = value.lower()
        for pronome in _PRONOMES_PRIMEIRA_PESSOA:
            pattern = r'\b' + re.escape(pronome) + r'\b'
            for match in re.finditer(pattern, texto):
                # Tratamento especial para 'nos' que pode ser contração
                if pronome == 'nos':
                    if _is_nos_contraction(texto, match.start(), match.end()):
                        continue  # É contração, não pronome
                return False
        return True


class NoSecondPersonChecker(Instruction):
    """A resposta não deve usar pronomes de segunda pessoa."""

    def build_description(self):
        self._description_pattern = (
            "NÃO use pronomes de segunda pessoa (tu, te, você, vocês, teu, vosso, etc.)."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        texto = value.lower()
        for pronome in _PRONOMES_SEGUNDA_PESSOA:
            pattern = r'\b' + re.escape(pronome) + r'\b'
            if re.search(pattern, texto):
                return False
        return True


class UseFirstPersonChecker(Instruction):
    """A resposta deve usar pelo menos N pronomes de primeira pessoa."""

    def build_description(self, *, min_count=None):
        self._min_count = min_count if min_count is not None else random.choice([2, 3, 4])

        self._description_pattern = (
            "Use pelo menos {min_count} pronomes de primeira pessoa (eu, me, meu, nós, nosso, etc.)."
        )
        return self._description_pattern.format(min_count=self._min_count)

    def get_instruction_args(self):
        return {"min_count": self._min_count}

    def get_instruction_args_keys(self):
        return ["min_count"]

    def check_following(self, value):
        texto = value.lower()
        count = 0
        for pronome in _PRONOMES_PRIMEIRA_PESSOA:
            pattern = r'\b' + re.escape(pronome) + r'\b'
            for match in re.finditer(pattern, texto):
                # Tratamento especial para 'nos' que pode ser contração
                if pronome == 'nos':
                    if _is_nos_contraction(texto, match.start(), match.end()):
                        continue  # É contração, não pronome
                count += 1
        return count >= self._min_count


class UseThirdPersonChecker(Instruction):
    """A resposta deve usar pelo menos N pronomes de terceira pessoa."""

    def build_description(self, *, min_count=None):
        self._min_count = min_count if min_count is not None else random.choice([2, 3, 4])

        self._description_pattern = (
            "Use pelo menos {min_count} pronomes de terceira pessoa (ele, ela, seu, sua, etc.)."
        )
        return self._description_pattern.format(min_count=self._min_count)

    def get_instruction_args(self):
        return {"min_count": self._min_count}

    def get_instruction_args_keys(self):
        return ["min_count"]

    def check_following(self, value):
        texto = value.lower()
        count = 0
        for pronome in _PRONOMES_TERCEIRA_PESSOA:
            pattern = r'\b' + re.escape(pronome) + r'\b'
            matches = re.findall(pattern, texto)
            count += len(matches)
        return count >= self._min_count

class NoQuestionsChecker(Instruction):
    """A resposta não deve conter perguntas."""

    def build_description(self):
        self._description_pattern = (
            "NÃO faça perguntas na resposta (não use '?')."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        return '?' not in value


class NoExclamationsChecker(Instruction):
    """A resposta não deve conter exclamações."""

    def build_description(self):
        self._description_pattern = (
            "NÃO use pontos de exclamação na resposta."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        return '!' not in value


class OnlyDeclarativeSentencesChecker(Instruction):
    """Todas as frases devem ser declarativas (terminar com ponto final)."""

    def build_description(self):
        self._description_pattern = (
            "Todas as frases devem ser declarativas (terminar apenas com ponto final, sem '?' ou '!')."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        return '?' not in value and '!' not in value


class IncludeQuestionChecker(Instruction):
    """A resposta deve incluir pelo menos uma pergunta."""

    def build_description(self, *, min_questions=None):
        self._min_questions = min_questions if min_questions is not None else 1

        self._description_pattern = (
            "Inclua pelo menos {min_questions} pergunta(s) na resposta."
        )
        return self._description_pattern.format(min_questions=self._min_questions)

    def get_instruction_args(self):
        return {"min_questions": self._min_questions}

    def get_instruction_args_keys(self):
        return ["min_questions"]

    def check_following(self, value):
        count = value.count('?')
        return count >= self._min_questions


class IncludeQuoteChecker(Instruction):
    """A resposta deve incluir pelo menos uma citação entre aspas."""

    def build_description(self):
        self._description_pattern = (
            'Inclua pelo menos uma citação entre aspas ("...") na resposta.'
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        # Verifica aspas duplas (normais e tipográficas)
        pattern = r'[""][^""]+[""]|["""][^"""]+["""]'
        matches = re.findall(pattern, value)
        # Verifica se há pelo menos uma citação com mais de 5 caracteres
        return any(len(m) > 7 for m in matches)


class UseSemicolonChecker(Instruction):
    """A resposta deve usar pelo menos N ponto-e-vírgulas."""

    def build_description(self, *, min_count=None):
        # Default to 1 for deterministic evaluation (avoid random during eval)
        self._min_count = min_count if min_count is not None else 1

        self._description_pattern = (
            "Use pelo menos {min_count} ponto-e-vírgula(s) (;) na resposta."
        )
        return self._description_pattern.format(min_count=self._min_count)

    def get_instruction_args(self):
        return {"min_count": self._min_count}

    def get_instruction_args_keys(self):
        return ["min_count"]

    def check_following(self, value):
        count = value.count(';')
        return count >= self._min_count


class UseColonChecker(Instruction):
    """A resposta deve usar pelo menos N dois-pontos."""

    def build_description(self, *, min_count=None):
        # Default to 1 for deterministic evaluation
        self._min_count = min_count if min_count is not None else 1

        self._description_pattern = (
            "Use pelo menos {min_count} dois-pontos (:) na resposta."
        )
        return self._description_pattern.format(min_count=self._min_count)

    def get_instruction_args(self):
        return {"min_count": self._min_count}

    def get_instruction_args_keys(self):
        return ["min_count"]

    def check_following(self, value):
        count = value.count(':')
        return count >= self._min_count

class StartWithWordChecker(Instruction):
    """A resposta deve começar com uma palavra específica."""

    def build_description(self, *, word=None, start_word=None):
        palavras = ["A", "O", "Esta", "Este", "Na", "No", "Em", "Para", "Quando", "Assim"]
        # Accept both 'word' and 'start_word' for backwards compatibility
        effective_word = word if word is not None else start_word
        self._word = effective_word if effective_word is not None else random.choice(palavras)

        self._description_pattern = (
            'A resposta deve COMEÇAR com a palavra "{word}".'
        )
        return self._description_pattern.format(word=self._word)

    def get_instruction_args(self):
        return {"word": self._word}

    def get_instruction_args_keys(self):
        return ["word"]

    def check_following(self, value):
        texto = value.strip()
        palavras = texto.split()
        if not palavras:
            return False
        primeira = palavras[0].strip(string.punctuation)
        return primeira.lower() == self._word.lower()


class EndWithWordChecker(Instruction):
    """A resposta deve terminar com uma palavra específica."""

    def build_description(self, *, word=None, end_word=None):
        palavras = ["leitor", "obra", "narrativa", "história", "literatura", "reflexão", "análise"]
        # Accept both 'word' and 'end_word' for backwards compatibility
        effective_word = word if word is not None else end_word
        self._word = effective_word if effective_word is not None else random.choice(palavras)

        self._description_pattern = (
            'A resposta deve TERMINAR com a palavra "{word}".'
        )
        return self._description_pattern.format(word=self._word)

    def get_instruction_args(self):
        return {"word": self._word}

    def get_instruction_args_keys(self):
        return ["word"]

    def check_following(self, value):
        texto = value.strip().rstrip('.!?')
        palavras = texto.split()
        if not palavras:
            return False
        ultima = palavras[-1].strip(string.punctuation)
        return ultima.lower() == self._word.lower()


class StartEndSameWordChecker(Instruction):
    """A resposta deve começar e terminar com a mesma palavra."""

    def build_description(self, *, word=None):
        # word parameter is ignored but accepted for backwards compatibility
        self._description_pattern = (
            "A resposta deve COMEÇAR e TERMINAR com a mesma palavra."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        texto = value.strip()
        palavras = re.findall(r'\b\w+\b', texto.lower())
        if len(palavras) < 2:
            return False
        return palavras[0] == palavras[-1]


class BulletListChecker(Instruction):
    """A resposta deve usar lista com marcadores."""

    def build_description(self, *, min_items=None):
        self._min_items = min_items if min_items is not None else 1

        self._description_pattern = (
            "Use uma lista com marcadores (•, -, * ou similar) com pelo menos {min_items} itens."
        )
        return self._description_pattern.format(min_items=self._min_items)

    def get_instruction_args(self):
        return {"min_items": self._min_items}

    def get_instruction_args_keys(self):
        return ["min_items"]

    def check_following(self, value):
        marcadores = ['•', '-', '*', '→', '►', '▪', '●', '○']
        linhas = value.split('\n')
        count = 0
        for linha in linhas:
            linha = linha.strip()
            if linha and linha[0] in marcadores:
                count += 1
        return count >= self._min_items


class NumberedListChecker(Instruction):
    """A resposta deve usar lista numerada."""

    def build_description(self, *, min_items=None):
        self._min_items = min_items if min_items is not None else 1

        self._description_pattern = (
            "Use uma lista numerada (1., 2., 3., etc.) com pelo menos {min_items} itens."
        )
        return self._description_pattern.format(min_items=self._min_items)

    def get_instruction_args(self):
        return {"min_items": self._min_items}

    def get_instruction_args_keys(self):
        return ["min_items"]

    def check_following(self, value):
        pattern = r'^\s*\d+[\.\)]\s+'
        linhas = value.split('\n')
        count = sum(1 for linha in linhas if re.match(pattern, linha))
        return count >= self._min_items


class AllCapsChecker(Instruction):
    """A resposta deve estar inteiramente em MAIÚSCULAS."""

    def build_description(self):
        self._description_pattern = (
            "Escreva toda a resposta em MAIÚSCULAS."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        # Remove pontuação e números, verifica se todas as letras são maiúsculas
        letras = re.findall(r'[a-záàâãéèêíìîóòôõúùûç]', value, re.IGNORECASE)
        if not letras:
            return False
        return all(c.isupper() for c in letras if c.isalpha())


class AllLowercaseChecker(Instruction):
    """A resposta deve estar inteiramente em minúsculas."""

    def build_description(self):
        self._description_pattern = (
            "Escreva toda a resposta em minúsculas."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        letras = re.findall(r'[a-záàâãéèêíìîóòôõúùûç]', value, re.IGNORECASE)
        if not letras:
            return False
        return all(c.islower() for c in letras if c.isalpha())


class TitleCaseStartChecker(Instruction):
    """Cada frase deve começar com letra maiúscula."""

    def build_description(self):
        self._description_pattern = (
            "Cada frase deve começar com letra maiúscula."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        frases = _dividir_em_frases(value)
        for frase in frases:
            frase = frase.strip()
            if frase and frase[0].isalpha() and not frase[0].isupper():
                return False
        return True


class NoRepeatSentenceStartChecker(Instruction):
    """Duas frases consecutivas não podem começar com a mesma palavra."""

    def build_description(self):
        self._description_pattern = (
            "Duas frases consecutivas NÃO podem começar com a mesma palavra."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        frases = _dividir_em_frases(value)
        prev_inicio = None
        for frase in frases:
            palavras = frase.strip().split()
            if not palavras:
                continue
            inicio = palavras[0].lower().strip(string.punctuation)
            if prev_inicio and inicio == prev_inicio:
                return False
            prev_inicio = inicio
        return True

class TerminacaoAndoEndoIndoLimitChecker(Instruction):
    """Limita palavras terminadas em -ando, -endo, -indo."""

    def build_description(self, *, max_count=None, max_gerunds=None):
        self._max_count = max_count if max_count is not None else (max_gerunds if max_gerunds is not None else random.choice([3, 5, 7]))

        self._description_pattern = (
            "Use no máximo {max_count} palavras terminadas em '-ando', '-endo' ou '-indo'."
        )
        return self._description_pattern.format(max_count=self._max_count)

    def get_instruction_args(self):
        return {"max_count": self._max_count, "max_gerunds": self._max_count}

    def get_instruction_args_keys(self):
        return ["max_count", "max_gerunds"]

    def check_following(self, value):
        pattern = r'\b\w+(?:ando|endo|indo)\b'
        matches = re.findall(pattern, value.lower())
        return len(matches) <= self._max_count


class TerminacaoAndoEndoIndoMinChecker(Instruction):
    """Exige mínimo de palavras terminadas em -ando, -endo, -indo."""

    def build_description(self, *, min_count=None, min_gerunds=None):
        self._min_count = min_count if min_count is not None else (min_gerunds if min_gerunds is not None else random.choice([2, 3, 4]))

        self._description_pattern = (
            "Use pelo menos {min_count} palavras terminadas em '-ando', '-endo' ou '-indo'."
        )
        return self._description_pattern.format(min_count=self._min_count)

    def get_instruction_args(self):
        return {"min_count": self._min_count, "min_gerunds": self._min_count}

    def get_instruction_args_keys(self):
        return ["min_count", "min_gerunds"]

    def check_following(self, value):
        pattern = r'\b\w+(?:ando|endo|indo)\b'
        matches = re.findall(pattern, value.lower())
        return len(matches) >= self._min_count


class TerminacaoInhoInhaMinChecker(Instruction):
    """Exige mínimo de palavras terminadas em -inho, -inha, -zinho, -zinha."""

    def build_description(self, *, min_count=None, min_diminutives=None):
        self._min_count = min_count if min_count is not None else (min_diminutives if min_diminutives is not None else random.choice([2, 3, 4]))

        self._description_pattern = (
            "Use pelo menos {min_count} palavras terminadas em '-inho', '-inha', '-zinho' ou '-zinha'."
        )
        return self._description_pattern.format(min_count=self._min_count)

    def get_instruction_args(self):
        return {"min_count": self._min_count, "min_diminutives": self._min_count}

    def get_instruction_args_keys(self):
        return ["min_count", "min_diminutives"]

    def check_following(self, value):
        pattern = r'\b\w+(?:inho|inha|inhos|inhas|zinho|zinha|zinhos|zinhas)\b'
        matches = re.findall(pattern, value.lower())
        return len(matches) >= self._min_count


class TerminacaoInhoInhaProibidoChecker(Instruction):
    """Proíbe palavras terminadas em -inho, -inha, -zinho, -zinha."""

    def build_description(self):
        self._description_pattern = (
            "NÃO use palavras terminadas em '-inho', '-inha', '-zinho' ou '-zinha'."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        pattern = r'\b\w+(?:inho|inha|inhos|inhas|zinho|zinha|zinhos|zinhas)\b'
        return not bool(re.search(pattern, value.lower()))


class TerminacaoAoOesMinChecker(Instruction):
    """Exige mínimo de palavras terminadas em -ão, -ões, -ona, -onas."""

    def build_description(self, *, min_count=None, min_augmentatives=None):
        self._min_count = min_count if min_count is not None else (min_augmentatives if min_augmentatives is not None else random.choice([1, 2]))

        self._description_pattern = (
            "Use pelo menos {min_count} palavra(s) terminada(s) em '-ão', '-ões', '-ona' ou '-onas'."
        )
        return self._description_pattern.format(min_count=self._min_count)

    def get_instruction_args(self):
        return {"min_count": self._min_count, "min_augmentatives": self._min_count}

    def get_instruction_args_keys(self):
        return ["min_count", "min_augmentatives"]

    def check_following(self, value):
        pattern = r'\b\w+(?:ão|ões|ona|onas)\b'
        matches = re.findall(pattern, value.lower())
        return len(matches) >= self._min_count


class TerminacaoMenteLimitChecker(Instruction):
    """Limita palavras terminadas em -mente."""

    def build_description(self, *, max_count=None, max_adverbs=None):
        self._max_count = max_count if max_count is not None else (max_adverbs if max_adverbs is not None else random.choice([3, 5, 7]))

        self._description_pattern = (
            "Use no máximo {max_count} palavras terminadas em '-mente'."
        )
        return self._description_pattern.format(max_count=self._max_count)

    def get_instruction_args(self):
        return {"max_count": self._max_count, "max_adverbs": self._max_count}

    def get_instruction_args_keys(self):
        return ["max_count", "max_adverbs"]

    def check_following(self, value):
        pattern = r'\b\w+mente\b'
        matches = re.findall(pattern, value.lower())
        return len(matches) <= self._max_count


class TerminacaoMenteMinChecker(Instruction):
    """Exige mínimo de palavras terminadas em -mente."""

    def build_description(self, *, min_count=None, min_adverbs=None):
        self._min_count = min_count if min_count is not None else (min_adverbs if min_adverbs is not None else random.choice([2, 3, 4]))

        self._description_pattern = (
            "Use pelo menos {min_count} palavras terminadas em '-mente'."
        )
        return self._description_pattern.format(min_count=self._min_count)

    def get_instruction_args(self):
        return {"min_count": self._min_count, "min_adverbs": self._min_count}

    def get_instruction_args_keys(self):
        return ["min_count", "min_adverbs"]

    def check_following(self, value):
        pattern = r'\b\w+mente\b'
        matches = re.findall(pattern, value.lower())
        return len(matches) >= self._min_count


class TerminacaoMenteProibidoChecker(Instruction):
    """Proíbe palavras terminadas em -mente."""

    def build_description(self):
        self._description_pattern = (
            "NÃO use palavras terminadas em '-mente'."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        pattern = r'\b\w+mente\b'
        return not bool(re.search(pattern, value.lower()))


class ConjunctionCountChecker(Instruction):
    """A resposta deve usar pelo menos N conjunções coordenativas."""

    def build_description(self, *, min_count=None, small_n=None):
        self._min_count = min_count if min_count is not None else (small_n if small_n is not None else random.choice([3, 4, 5]))

        self._description_pattern = (
            "Use pelo menos {min_count} conjunções coordenativas (e, mas, ou, porém, contudo, etc.)."
        )
        return self._description_pattern.format(min_count=self._min_count)

    def get_instruction_args(self):
        return {"min_count": self._min_count, "small_n": self._min_count}

    def get_instruction_args_keys(self):
        return ["min_count", "small_n"]

    def check_following(self, value):
        texto = value.lower()
        count = 0
        for conj in _CONJUNCOES_COORDENATIVAS:
            pattern = r'\b' + re.escape(conj) + r'\b'
            matches = re.findall(pattern, texto)
            count += len(matches)
        return count >= self._min_count


class ConnectiveChecker(Instruction):
    """A resposta deve usar pelo menos N conectivos/marcadores discursivos."""

    def build_description(self, *, min_connectives=None):
        self._min_connectives = min_connectives if min_connectives is not None else random.choice([2, 3, 4])

        self._description_pattern = (
            "Use pelo menos {min_connectives} conectivos (portanto, contudo, além disso, etc.)."
        )
        return self._description_pattern.format(min_connectives=self._min_connectives)

    def get_instruction_args(self):
        return {"min_connectives": self._min_connectives}

    def get_instruction_args_keys(self):
        return ["min_connectives"]

    def check_following(self, value):
        texto = value.lower()
        count = 0
        for conn in _CONECTIVOS:
            if conn in texto:
                count += 1
        return count >= self._min_connectives


class TemporalMarkerChecker(Instruction):
    """A resposta deve usar pelo menos N marcadores temporais."""

    def build_description(self, *, min_markers=None):
        self._min_markers = min_markers if min_markers is not None else random.choice([2, 3])

        self._description_pattern = (
            "Use pelo menos {min_markers} marcadores temporais (primeiro, depois, por fim, etc.)."
        )
        return self._description_pattern.format(min_markers=self._min_markers)

    def get_instruction_args(self):
        return {"min_markers": self._min_markers}

    def get_instruction_args_keys(self):
        return ["min_markers"]

    def check_following(self, value):
        texto = value.lower()
        count = 0
        for marker in _MARCADORES_TEMPORAIS:
            if marker in texto:
                count += 1
        return count >= self._min_markers


class ContrastMarkerChecker(Instruction):
    """A resposta deve usar pelo menos um marcador de contraste."""

    def build_description(self):
        self._description_pattern = (
            "Use pelo menos um marcador de contraste (por outro lado, no entanto, porém, contudo, etc.)."
        )
        return self._description_pattern

    def get_instruction_args(self):
        return {}

    def get_instruction_args_keys(self):
        return []

    def check_following(self, value):
        texto = value.lower()
        for marker in _MARCADORES_CONTRASTE:
            if marker in texto:
                return True
        return False

class MaxWordRepeatChecker(Instruction):
    """Nenhuma palavra pode se repetir mais de N vezes."""

    def build_description(self, *, max_repeats=None, small_n=None, N=None):
        # Accept 'max_repeats', 'small_n', or 'N' for backwards compatibility
        effective = max_repeats if max_repeats is not None else (small_n if small_n is not None else N)
        self._max_repeats = effective if effective is not None else random.choice([3, 4, 5])

        self._description_pattern = (
            "Nenhuma palavra pode aparecer mais de {max_repeats} vezes na resposta."
        )
        return self._description_pattern.format(max_repeats=self._max_repeats)

    def get_instruction_args(self):
        return {"max_repeats": self._max_repeats, "small_n": self._max_repeats}

    def get_instruction_args_keys(self):
        return ["max_repeats", "small_n"]

    def check_following(self, value):
        palavras = value.lower().split()
        palavras = [p.strip(string.punctuation) for p in palavras]
        counter = Counter(palavras)
        for word, count in counter.items():
            if word and count > self._max_repeats:
                return False
        return True

class AcrosticChecker(Instruction):
    """As primeiras letras de cada linha devem formar uma palavra."""

    def build_description(self, *, word=None):
        palavras = ["LIVRO", "OBRA", "LER", "ARTE", "VIDA", "AMOR", "PAZ"]
        self._word = word if word is not None else random.choice(palavras)

        self._description_pattern = (
            'Escreva um acróstico onde a primeira letra de cada linha forma a palavra "{word}".'
        )
        return self._description_pattern.format(word=self._word)

    def get_instruction_args(self):
        return {"word": self._word}

    def get_instruction_args_keys(self):
        return ["word"]

    def check_following(self, value):
        # Split by lines, not sentences
        linhas = [l.strip() for l in value.strip().split('\n') if l.strip()]
        if len(linhas) < len(self._word):
            return False
        primeiras = ''.join(l[0].upper() for l in linhas[:len(self._word)] if l)
        return primeiras == self._word.upper()


class EachLineStartsWithChecker(Instruction):
    """Cada linha deve começar com um caractere específico."""

    def build_description(self, *, char=None):
        self._char = char if char is not None else random.choice(['-', '•', '*', '>', '→'])

        self._description_pattern = (
            'Cada linha deve começar com o caractere "{char}".'
        )
        return self._description_pattern.format(char=self._char)

    def get_instruction_args(self):
        return {"char": self._char}

    def get_instruction_args_keys(self):
        return ["char"]

    def check_following(self, value):
        linhas = value.strip().split('\n')
        linhas = [l.strip() for l in linhas if l.strip()]
        for linha in linhas:
            if not linha.startswith(self._char):
                return False
        return True


class ExactLineCountChecker(Instruction):
    """A resposta deve ter exatamente N linhas."""

    def build_description(self, *, num_lines=None, N=None):
        effective = num_lines if num_lines is not None else N
        self._num_lines = effective if effective is not None else random.choice([3, 4, 5, 6, 7])

        self._description_pattern = (
            "A resposta deve ter EXATAMENTE {num_lines} linhas."
        )
        return self._description_pattern.format(num_lines=self._num_lines)

    def get_instruction_args(self):
        return {"num_lines": self._num_lines}

    def get_instruction_args_keys(self):
        return ["num_lines"]

    def check_following(self, value):
        linhas = value.strip().split('\n')
        linhas = [l.strip() for l in linhas if l.strip()]
        return len(linhas) == self._num_lines


ExactParagraphsChecker = ExactParagraphCountChecker
MinParagraphsChecker = MinParagraphCountChecker
NumbersCountChecker = ExactNumberCountChecker
PronounCountChecker = UseThirdPersonChecker
LimitedWordRepeatChecker = MaxWordRepeatChecker
IncludeKeywordChecker = IncludeWordChecker
SpecialBulletPointsChecker = BulletListChecker
TemporalMarkersChecker = TemporalMarkerChecker
ContrastiveStatementChecker = ContrastMarkerChecker
ConnectivesChecker = ConnectiveChecker
DirectQuoteChecker = IncludeQuoteChecker
GerundLimitChecker = TerminacaoAndoEndoIndoLimitChecker
MinGerundChecker = TerminacaoAndoEndoIndoMinChecker
DiminutiveChecker = TerminacaoInhoInhaMinChecker
NoDiminutiveChecker = TerminacaoInhoInhaProibidoChecker
AugmentativeChecker = TerminacaoAoOesMinChecker
AdverbMenteLimitChecker = TerminacaoMenteLimitChecker
MinAdverbMenteChecker = TerminacaoMenteMinChecker
NoAdverbMenteChecker = TerminacaoMenteProibidoChecker
