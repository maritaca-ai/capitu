
import instructions


INSTRUCTION_DICT = {
    "count:word_count_range": instructions.WordCountRangeChecker,
    "count:exact_word_count": instructions.ExactWordCountChecker,
    "count:min_word_count": instructions.MinWordCountChecker,
    "count:max_word_count": instructions.MaxWordCountChecker,
    "count:unique_word_count": instructions.UniqueWordCountChecker,
    "count:character_count_range": instructions.CharacterCountRangeChecker,
    "count:exact_sentence_count": instructions.ExactSentenceCountChecker,
    "count:min_sentence_count": instructions.MinSentenceCountChecker,
    "count:sentence_count_range": instructions.SentenceCountRangeChecker,
    "count:exact_paragraph_count": instructions.ExactParagraphCountChecker,
    "count:min_paragraph_count": instructions.MinParagraphCountChecker,
    "count:max_sentence_length": instructions.MaxSentenceLengthChecker,
    "count:min_sentence_length": instructions.MinSentenceLengthChecker,
    "count:exact_line_count": instructions.ExactLineCountChecker,
    "count:exact_number_count": instructions.ExactNumberCountChecker,
    "count:min_number_count": instructions.MinNumberCountChecker,
    "count:include_specific_number": instructions.IncludeSpecificNumberChecker,
    "words:include_word": instructions.IncludeWordChecker,
    "words:include_words": instructions.IncludeWordsChecker,
    "words:word_frequency": instructions.WordFrequencyChecker,
    "words:min_word_frequency": instructions.MinWordFrequencyChecker,
    "forbidden:word": instructions.ForbiddenWordChecker,
    "forbidden:words_list": instructions.ForbiddenWordsListChecker,
    "forbidden:no_numbers": instructions.NoNumbersChecker,
    "forbidden:no_first_person": instructions.NoFirstPersonChecker,
    "forbidden:no_second_person": instructions.NoSecondPersonChecker,
    "words:use_first_person": instructions.UseFirstPersonChecker,
    "words:use_third_person": instructions.UseThirdPersonChecker,
    "forbidden:no_questions": instructions.NoQuestionsChecker,
    "forbidden:no_exclamations": instructions.NoExclamationsChecker,
    "punctuation:only_declarative": instructions.OnlyDeclarativeSentencesChecker,
    "punctuation:include_question": instructions.IncludeQuestionChecker,
    "punctuation:include_quote": instructions.IncludeQuoteChecker,
    "punctuation:use_semicolon": instructions.UseSemicolonChecker,
    "punctuation:use_colon": instructions.UseColonChecker,
    "structure:start_with_word": instructions.StartWithWordChecker,
    "structure:end_with_word": instructions.EndWithWordChecker,
    "structure:start_end_same_word": instructions.StartEndSameWordChecker,
    "format:bullet_list": instructions.BulletListChecker,
    "format:numbered_list": instructions.NumberedListChecker,
    "format:all_caps": instructions.AllCapsChecker,
    "format:all_lowercase": instructions.AllLowercaseChecker,
    "format:title_case_start": instructions.TitleCaseStartChecker,
    "structure:no_repeat_sentence_start": instructions.NoRepeatSentenceStartChecker,
    "structure:each_line_starts_with": instructions.EachLineStartsWithChecker,
    "structure:acrostic": instructions.AcrosticChecker,
    "pattern:terminacao_ando_endo_indo_limit": instructions.TerminacaoAndoEndoIndoLimitChecker,
    "pattern:terminacao_ando_endo_indo_min": instructions.TerminacaoAndoEndoIndoMinChecker,
    "pattern:terminacao_inho_inha_min": instructions.TerminacaoInhoInhaMinChecker,
    "pattern:terminacao_inho_inha_proibido": instructions.TerminacaoInhoInhaProibidoChecker,
    "pattern:terminacao_ao_oes_min": instructions.TerminacaoAoOesMinChecker,
    "pattern:terminacao_mente_limit": instructions.TerminacaoMenteLimitChecker,
    "pattern:terminacao_mente_min": instructions.TerminacaoMenteMinChecker,
    "pattern:terminacao_mente_proibido": instructions.TerminacaoMenteProibidoChecker,
    "words:conjunction_count": instructions.ConjunctionCountChecker,
    "words:connective": instructions.ConnectiveChecker,
    "words:temporal_marker": instructions.TemporalMarkerChecker,
    "words:contrast_marker": instructions.ContrastMarkerChecker,
    "words:max_word_repeat": instructions.MaxWordRepeatChecker,
    "words:gerund_limit": instructions.TerminacaoAndoEndoIndoLimitChecker,
    "words:min_gerund": instructions.TerminacaoAndoEndoIndoMinChecker,
    "words:diminutive": instructions.TerminacaoInhoInhaMinChecker,
    "words:no_diminutive": instructions.TerminacaoInhoInhaProibidoChecker,
    "words:augmentative": instructions.TerminacaoAoOesMinChecker,
    "words:adverb_mente_limit": instructions.TerminacaoMenteLimitChecker,
    "words:min_adverb_mente": instructions.TerminacaoMenteMinChecker,
    "words:no_adverb_mente": instructions.TerminacaoMenteProibidoChecker,
    "count:numbers": instructions.ExactNumberCountChecker,
    "count:pronouns": instructions.UseThirdPersonChecker,
    "count:conjunctions": instructions.ConjunctionCountChecker,
    "words:repeats": instructions.MaxWordRepeatChecker,
    "sentence:keyword": instructions.IncludeWordChecker,
    "sentence:temporal_markers": instructions.TemporalMarkerChecker,
    "sentence:contrastive": instructions.ContrastMarkerChecker,
    "format:list": instructions.BulletListChecker,
    "words:connectives": instructions.ConnectiveChecker,
    "constraint:max_sentence_length": instructions.MaxSentenceLengthChecker,
    "constraint:exact_paragraphs": instructions.ExactParagraphCountChecker,
    "constraint:min_paragraphs": instructions.MinParagraphCountChecker,
    "forbidden:first_person": instructions.NoFirstPersonChecker,
    "forbidden:questions": instructions.NoQuestionsChecker,
    "forbidden:exclamations": instructions.NoExclamationsChecker,
    "content:direct_quote": instructions.IncludeQuoteChecker,
}


EASY_INSTRUCTIONS = [
    "count:min_word_count",
    "count:max_word_count",
    "count:min_sentence_count",
    "count:min_paragraph_count",
    "forbidden:no_questions",
    "forbidden:no_exclamations",
    "forbidden:no_numbers",
    "format:title_case_start",
]

MEDIUM_INSTRUCTIONS = [
    "count:word_count_range",
    "count:sentence_count_range",
    "count:exact_paragraph_count",
    "count:unique_word_count",
    "words:include_word",
    "forbidden:word",
    "forbidden:no_first_person",
    "punctuation:include_quote",
    "punctuation:use_semicolon",
    "structure:start_with_word",
    "format:bullet_list",
    "format:numbered_list",
    "pattern:terminacao_ando_endo_indo_limit",
    "pattern:terminacao_mente_limit",
    "words:connective",
]

HARD_INSTRUCTIONS = [
    "count:exact_word_count",
    "count:exact_sentence_count",
    "count:character_count_range",
    "count:exact_number_count",
    "words:word_frequency",
    "words:include_words",
    "forbidden:words_list",
    "words:max_word_repeat",
    "structure:start_end_same_word",
    "structure:acrostic",
    "structure:no_repeat_sentence_start",
    "structure:each_line_starts_with",
    "pattern:terminacao_inho_inha_min",
    "pattern:terminacao_ao_oes_min",
    "pattern:terminacao_mente_proibido",
    "pattern:terminacao_inho_inha_proibido",
    "words:temporal_marker",
    "words:contrast_marker",
    "format:all_caps",
    "format:all_lowercase",
]


def get_instruction_by_id(instruction_id: str):
    """Retorna a classe de instrução pelo ID."""
    if instruction_id not in INSTRUCTION_DICT:
        raise ValueError(f"Instrução não encontrada: {instruction_id}")
    return INSTRUCTION_DICT[instruction_id]


def get_all_instruction_ids() -> list:
    """Retorna todos os IDs de instruções disponíveis."""
    return list(INSTRUCTION_DICT.keys())


def get_instructions_by_difficulty(difficulty: str) -> list:
    """Retorna IDs de instruções por nível de dificuldade."""
    if difficulty == "easy":
        return EASY_INSTRUCTIONS
    elif difficulty == "medium":
        return MEDIUM_INSTRUCTIONS
    elif difficulty == "hard":
        return HARD_INSTRUCTIONS
    else:
        raise ValueError(f"Dificuldade inválida: {difficulty}. Use 'easy', 'medium' ou 'hard'.")
