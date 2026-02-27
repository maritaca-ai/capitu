import functools
import random
import re

import immutabledict
import nltk


WORD_LIST = [
    # Personagens e obras
    "sertao", "veredas", "capitu", "bentinho", "riobaldo", "diadorim",
    "macunaima", "iracema", "martim", "fabiano", "sinhavitoria", "baleia",
    "macabea", "cortico", "casmurro",

    # Termos literários
    "narrador", "protagonista", "antagonista", "metafora", "simbolo",
    "alegoria", "critica", "ensaio", "memoria", "testemunho", "romance",
    "cronica", "conto", "poesia", "verso", "prefacio", "posfacio",
    "capitulo", "epilogo", "paragrafo", "epigrafe",

    # Movimentos literários
    "realismo", "naturalismo", "modernismo", "romantismo", "regionalismo",
    "simbolismo", "parnasianismo", "barroco", "arcadismo",

    # Cultura brasileira
    "cangaco", "lampiao", "capoeira", "cordel", "senzala", "quilombo",
    "folclore", "curupira", "saci", "boitata", "yara", "bumba", "reisado",
    "maracatu", "frevo", "ciranda", "samba", "pagode", "choro", "bossa",
    "forro", "xote", "xaxado", "repente", "embolada", "cantoria",

    # Religião e espiritualidade
    "orixa", "terreiro", "umbanda", "candomble", "sincretismo",
    "benzedeira", "pajelanca", "romaria", "procissao",

    # Geografia e natureza
    "nordeste", "sudeste", "amazonia", "cerrado", "caatinga", "pantanal",
    "litoral", "sertao", "mangue", "restinga", "chapada", "serra", "varzea",
    "igarape", "cachoeira",

    # Povos e identidades
    "caboclo", "ribeirinho", "sertanejo", "vaqueiro", "jangadeiro",
    "quilombola", "tropeiro", "cangaceiro", "garimpo", "garimpeiro",
    "tupi", "guarani", "xavante", "cacique",

    # Gentílicos
    "baiano", "pernambucano", "cearense", "mineiro", "carioca",
    "paulistano", "gaucho", "paraense", "amazonense", "nordestino",

    # Lugares e construções
    "fazenda", "engenho", "casarao", "sobrado", "cortico", "favela",
    "pelourinho", "praca", "mercado", "feira", "boteco",

    # Flora e fauna
    "mandacaru", "umbuzeiro", "juazeiro", "jatoba", "buriti", "carnauba",
    "pequi", "jabuticaba", "arara", "tucano", "tamandua", "jaburu",

    # Alimentos
    "mandioca", "feijao", "farofa", "rapadura", "cachaca", "quitute",

    # Instrumentos e arte
    "berimbau", "atabaque", "viola", "sanfona", "zabumba",
    "xilogravura", "ceramica", "renda", "bordado",
]


def download_nltk_resources():
    """Baixa recursos do NLTK necessários para processamento de português."""
    resources = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
    ]
    for path, name in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            try:
                nltk.download(name, quiet=True)
            except Exception:
                pass


download_nltk_resources()


# Letras do alfabeto português (incluindo acentuadas)
_ALPHABETS = r"([A-Za-zÀ-ÿ])"

# Abreviações comuns em português
_PREFIXES = r"(Sr|Sra|Srta|Dr|Dra|Prof|Profa|Cap|Pe|Dom|Frei|Ir|Mons|Rev)[.]"

# Sufixos comuns
_SUFFIXES = r"(Ltda|S\.?A|Filho|Neto|Jr|Sr|etc)"

# Palavras que iniciam frases frequentemente
_STARTERS = (
    r"(Sr\s|Sra\s|Srta\s|Dr\s|Dra\s|Prof\s|Profa\s|"
    r"Ele\s|Ela\s|Eles\s|Elas\s|Isso\s|Isto\s|Aquilo\s|"
    r"Mas\s|Porém\s|Entretanto\s|Contudo\s|Assim\s|"
    r"Então\s|Onde\s|Quando\s|Enquanto\s|Porque\s|Portanto\s|"
    r"Logo\s|Além\s|Todavia\s|Ademais\s|Outrossim\s)"
)

# Siglas e acrônimos
_ACRONYMS = r"([A-ZÀ-Ý][.][A-ZÀ-Ý][.](?:[A-ZÀ-Ý][.])?)"

# Websites e domínios
_WEBSITES = r"[.](com|net|org|io|gov|edu|me|br)"

# Dígitos
_DIGITS = r"([0-9])"

# Múltiplos pontos (reticências)
_MULTIPLE_DOTS = r"\.{2,}"


STOPWORDS_PT = {
    # Artigos
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    # Preposições
    "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas",
    "por", "pelo", "pela", "pelos", "pelas", "para", "pra", "pro",
    "com", "sem", "sobre", "entre", "sob", "até", "após", "desde",
    "contra", "perante", "ante", "mediante",
    # Conjunções
    "e", "ou", "mas", "porém", "contudo", "todavia", "entretanto",
    "porque", "pois", "que", "como", "quando", "onde", "se", "embora",
    "enquanto", "caso", "logo", "portanto", "assim", "então",
    # Pronomes pessoais
    "eu", "tu", "ele", "ela", "nós", "vós", "eles", "elas",
    "me", "te", "se", "lhe", "nos", "vos", "lhes",
    "mim", "ti", "si", "conosco", "convosco", "consigo",
    # Pronomes possessivos
    "meu", "minha", "meus", "minhas", "teu", "tua", "teus", "tuas",
    "seu", "sua", "seus", "suas", "nosso", "nossa", "nossos", "nossas",
    "vosso", "vossa", "vossos", "vossas",
    # Pronomes demonstrativos
    "este", "esta", "estes", "estas", "isto",
    "esse", "essa", "esses", "essas", "isso",
    "aquele", "aquela", "aqueles", "aquelas", "aquilo",
    # Pronomes indefinidos
    "algum", "alguma", "alguns", "algumas", "algo",
    "nenhum", "nenhuma", "nada", "ninguém",
    "todo", "toda", "todos", "todas", "tudo",
    "outro", "outra", "outros", "outras", "outrem",
    "muito", "muita", "muitos", "muitas",
    "pouco", "pouca", "poucos", "poucas",
    "tanto", "tanta", "tantos", "tantas",
    "qual", "quais", "quanto", "quanta", "quantos", "quantas",
    # Pronomes relativos
    "quem", "cujo", "cuja", "cujos", "cujas", "onde",
    # Advérbios comuns
    "não", "sim", "já", "ainda", "sempre", "nunca", "jamais",
    "também", "apenas", "só", "somente", "muito", "pouco",
    "mais", "menos", "bem", "mal", "assim", "aqui", "ali", "lá",
    "aí", "cá", "além", "aquém", "dentro", "fora", "perto", "longe",
    "acima", "abaixo", "atrás", "diante", "hoje", "ontem", "amanhã",
    "agora", "antes", "depois", "cedo", "tarde", "logo", "sempre",
    # Verbos auxiliares comuns
    "ser", "estar", "ter", "haver", "ir", "vir",
    "é", "são", "foi", "foram", "era", "eram", "será", "serão",
    "está", "estão", "esteve", "estiveram", "estava", "estavam",
    "tem", "têm", "teve", "tiveram", "tinha", "tinham",
    "há", "houve", "havia",
    "vai", "vão", "foi", "foram", "ia", "iam",
    "vem", "vêm", "veio", "vieram", "vinha", "vinham",
    # Outros
    "ao", "aos", "à", "às", "pelo", "pela", "pelos", "pelas",
    "num", "numa", "nuns", "numas", "dum", "duma", "duns", "dumas",
    "você", "vocês", "voce", "voces", "gente",
}



def split_into_sentences(text):
    """Divide o texto em frases.

    Args:
        text: String com uma ou mais frases.

    Returns:
        Lista de strings, cada uma sendo uma frase.
    """
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(_PREFIXES, "\\1<prd>", text)
    text = re.sub(_WEBSITES, "<prd>\\1", text)
    text = re.sub(_DIGITS + "[.]" + _DIGITS, "\\1<prd>\\2", text)
    text = re.sub(
        _MULTIPLE_DOTS,
        lambda match: "<prd>" * len(match.group(0)) + "<stop>",
        text,
    )
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub(r"\s" + _ALPHABETS + "[.] ", " \\1<prd> ", text)
    text = re.sub(_ACRONYMS + " " + _STARTERS, "\\1<stop> \\2", text)
    text = re.sub(
        _ALPHABETS + "[.]" + _ALPHABETS + "[.]" + _ALPHABETS + "[.]",
        "\\1<prd>\\2<prd>\\3<prd>",
        text,
    )
    text = re.sub(_ALPHABETS + "[.]" + _ALPHABETS + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + _SUFFIXES + "[.] " + _STARTERS, " \\1<stop> \\2", text)
    text = re.sub(" " + _SUFFIXES + "[.]", " \\1<prd>", text)
    text = re.sub(" " + _ALPHABETS + "[.]", " \\1<prd>", text)

    # Aspas tipográficas (curly quotes)
    left_curly = "\u201c"   # "
    right_curly = "\u201d"  # "
    if left_curly in text:
        text = text.replace("." + right_curly, right_curly + ".")
    if '"' in text:
        text = text.replace('."', '".')
    if "!" in text:
        text = text.replace('!"', '"!')
    if "?" in text:
        text = text.replace('?"', '"?')

    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]:
        sentences = sentences[:-1]
    return sentences


def count_words(text):
    """Conta o número de palavras no texto."""
    tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text)
    return len(tokens)


def count_unique_words(text):
    """Conta palavras distintas, ignorando maiúsculas e pontuação."""
    tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text.lower())
    return len(set(tokens))


def count_stopwords(text):
    """Conta o número de stop words no texto."""
    try:
        stopwords = set(nltk.corpus.stopwords.words('portuguese'))
    except LookupError:
        stopwords = STOPWORDS_PT

    tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text)
    num_stopwords = len([t for t in tokens if t.lower() in stopwords])
    return num_stopwords


def generate_keywords(num_keywords):
    """Gera palavras-chave aleatórias da lista brasileira."""
    return random.sample(WORD_LIST, k=min(num_keywords, len(WORD_LIST)))


@functools.lru_cache(maxsize=None)
def _get_sentence_tokenizer():
    """Carrega o tokenizador de frases para português."""
    try:
        return nltk.data.load("nltk:tokenizers/punkt/portuguese.pickle")
    except LookupError:
        return nltk.data.load("nltk:tokenizers/punkt/english.pickle")


def count_paragraphs(text):
    """Conta o número de parágrafos no texto."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    if len(paragraphs) <= 1:
        # Tenta dividir por quebra de linha simples
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    return len(paragraphs)


def count_sentences(text):
    """Conta o número de frases no texto."""
    sentences = split_into_sentences(text)
    return len(sentences)


def get_first_word(text):
    """Retorna a primeira palavra do texto."""
    tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text)
    return tokens[0] if tokens else ""


def get_last_word(text):
    """Retorna a última palavra do texto."""
    tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text)
    return tokens[-1] if tokens else ""


def normalize_text(text):
    """Normaliza texto removendo acentos e convertendo para minúsculas."""
    import unicodedata
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text


def extract_quoted_text(text):
    """Extrai textos entre aspas do texto."""
    patterns = [
        r'"([^"]+)"',  # Aspas duplas normais
        r'"([^"]+)"',  # Aspas tipográficas
        r'«([^»]+)»',  # Aspas francesas
        r"'([^']+)'",  # Aspas simples
    ]
    quotes = []
    for pattern in patterns:
        quotes.extend(re.findall(pattern, text))
    return quotes


def has_question_mark(text):
    """Verifica se o texto contém ponto de interrogação."""
    return '?' in text


def has_exclamation_mark(text):
    """Verifica se o texto contém ponto de exclamação."""
    return '!' in text


def count_numbers(text):
    """Conta números (algarismos) no texto."""
    numbers = re.findall(r'\b\d+\b', text)
    return len(set(numbers))



FIRST_PERSON_PRONOUNS = {
    # Pronome pessoal de primeira pessoa caso reto
    "eu", "nós",
    # Pronomes pessoais de primeira pessoa caso oblíquo
    "me", "mim", "migo", "comigo",
    "nos", "conosco",
    # Pronomes possessivos de primeira pessoa
    "meu", "minha", "meus", "minhas",
    "nosso", "nossa", "nossos", "nossas",
}

PERSONAL_PRONOUNS = {
    # Primeira pessoa
    "eu", "me", "mim", "comigo", "nós", "nos", "conosco",
    # Segunda pessoa
    "tu", "te", "ti", "contigo", "vós", "vos", "convosco",
    "você", "vocês",
    # Terceira pessoa
    "ele", "ela", "eles", "elas", "se", "si", "consigo",
    "o", "a", "os", "as", "lhe", "lhes",
}



def count_first_person_pronouns(text):
    """Conta pronomes de primeira pessoa no texto."""
    tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text.lower())
    return len([t for t in tokens if t in FIRST_PERSON_PRONOUNS])


def count_personal_pronouns(text):
    """Conta pronomes pessoais no texto."""
    tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text.lower())
    return len([t for t in tokens if t in PERSONAL_PRONOUNS])


COORDINATING_CONJUNCTIONS = {
    # Aditivas
    "e", "nem", "também",
    # Adversativas
    "mas", "porém", "contudo", "todavia", "entretanto", "no entanto",
    # Alternativas
    "ou", "ora", "já", "quer", "seja",
    # Conclusivas
    "logo", "portanto", "assim", "então", "pois",
    # Explicativas
    "que", "porque", "pois", "porquanto",
}


def count_conjunctions(text):
    """Conta conjunções coordenativas no texto."""
    text_lower = text.lower()
    count = 0
    for conj in COORDINATING_CONJUNCTIONS:
        if ' ' in conj:
            # Expressões com múltiplas palavras
            count += text_lower.count(conj)
        else:
            # Palavras simples
            pattern = r'\b' + re.escape(conj) + r'\b'
            count += len(re.findall(pattern, text_lower))
    return count


SUPERLATIVES = {
    # Superlativos absolutos sintéticos comuns
    "melhor", "pior", "maior", "menor", "ótimo", "ótima", "péssimo", "péssima",
    "máximo", "máxima", "mínimo", "mínima", "superior", "inferior",
    "excelente", "terrível", "horrível", "maravilhoso", "maravilhosa",
    "incrível", "fantástico", "fantástica", "espetacular", "extraordinário",
    "excepcional", "magnífico", "magnífica", "sublime", "supremo", "suprema",
    # Advérbios intensificadores
    "extremamente", "absolutamente", "completamente", "totalmente",
    "incrivelmente", "terrivelmente", "horrivelmente",
}

# Padrão para superlativos em -íssimo
SUPERLATIVE_PATTERN = r'\b\w+[íi]ssim[oa]s?\b'


def has_superlatives(text):
    """Verifica se o texto contém superlativos."""
    text_lower = text.lower()

    # Verifica superlativos da lista
    for sup in SUPERLATIVES:
        if re.search(r'\b' + re.escape(sup) + r'\b', text_lower):
            return True

    # Verifica padrão -íssimo
    if re.search(SUPERLATIVE_PATTERN, text_lower):
        return True

    return False
