"""
Testes para todas as instruções do Capitu.

Execute com: python -m pytest instructions_test.py -v
Ou simplesmente: python instructions_test.py
"""

import unittest
import instructions
import instructions_registry


class TestWordCountInstructions(unittest.TestCase):
    """Testes para instruções de contagem de palavras."""

    def test_word_count_range_pass(self):
        checker = instructions.WordCountRangeChecker("test")
        checker.build_description(min_words=5, max_words=10)
        self.assertTrue(checker.check_following("Uma frase com sete palavras para testar."))

    def test_word_count_range_fail_low(self):
        checker = instructions.WordCountRangeChecker("test")
        checker.build_description(min_words=10, max_words=20)
        self.assertFalse(checker.check_following("Poucas palavras."))

    def test_word_count_range_fail_high(self):
        checker = instructions.WordCountRangeChecker("test")
        checker.build_description(min_words=2, max_words=5)
        self.assertFalse(checker.check_following("Esta frase tem mais de cinco palavras no total."))

    def test_exact_word_count_pass(self):
        checker = instructions.ExactWordCountChecker("test")
        checker.build_description(num_words=5)
        self.assertTrue(checker.check_following("Esta frase tem cinco palavras."))

    def test_exact_word_count_fail(self):
        checker = instructions.ExactWordCountChecker("test")
        checker.build_description(num_words=5)
        self.assertFalse(checker.check_following("Esta frase tem seis palavras agora."))

    def test_min_word_count_pass(self):
        checker = instructions.MinWordCountChecker("test")
        checker.build_description(min_words=5)
        self.assertTrue(checker.check_following("Esta frase tem mais de cinco palavras no total."))

    def test_min_word_count_fail(self):
        checker = instructions.MinWordCountChecker("test")
        checker.build_description(min_words=10)
        self.assertFalse(checker.check_following("Poucas palavras."))

    def test_max_word_count_pass(self):
        checker = instructions.MaxWordCountChecker("test")
        checker.build_description(max_words=10)
        self.assertTrue(checker.check_following("Poucas palavras."))

    def test_max_word_count_fail(self):
        checker = instructions.MaxWordCountChecker("test")
        checker.build_description(max_words=3)
        self.assertFalse(checker.check_following("Esta frase tem muitas palavras."))

    def test_unique_word_count_pass(self):
        checker = instructions.UniqueWordCountChecker("test")
        checker.build_description(N=5)
        self.assertTrue(checker.check_following("O gato dormia enquanto o cachorro brincava feliz."))

    def test_unique_word_count_fail(self):
        checker = instructions.UniqueWordCountChecker("test")
        checker.build_description(N=10)
        self.assertFalse(checker.check_following("O o o o o."))

    def test_character_count_range_pass(self):
        checker = instructions.CharacterCountRangeChecker("test")
        checker.build_description(min_chars=10, max_chars=50)
        self.assertTrue(checker.check_following("Uma frase de tamanho médio."))

    def test_character_count_range_fail(self):
        checker = instructions.CharacterCountRangeChecker("test")
        checker.build_description(min_chars=100, max_chars=200)
        self.assertFalse(checker.check_following("Curto."))


class TestSentenceCountInstructions(unittest.TestCase):
    """Testes para instruções de contagem de frases."""

    def test_exact_sentence_count_pass(self):
        checker = instructions.ExactSentenceCountChecker("test")
        checker.build_description(num_sentences=3)
        self.assertTrue(checker.check_following("Primeira frase. Segunda frase. Terceira frase."))

    def test_exact_sentence_count_fail(self):
        checker = instructions.ExactSentenceCountChecker("test")
        checker.build_description(num_sentences=3)
        self.assertFalse(checker.check_following("Apenas uma frase."))

    def test_min_sentence_count_pass(self):
        checker = instructions.MinSentenceCountChecker("test")
        checker.build_description(min_sentences=2)
        self.assertTrue(checker.check_following("Primeira frase. Segunda frase. Terceira frase."))

    def test_min_sentence_count_fail(self):
        checker = instructions.MinSentenceCountChecker("test")
        checker.build_description(min_sentences=5)
        self.assertFalse(checker.check_following("Apenas uma frase."))

    def test_sentence_count_range_pass(self):
        checker = instructions.SentenceCountRangeChecker("test")
        checker.build_description(min_sentences=2, max_sentences=4)
        self.assertTrue(checker.check_following("Primeira. Segunda. Terceira."))

    def test_sentence_count_range_fail(self):
        checker = instructions.SentenceCountRangeChecker("test")
        checker.build_description(min_sentences=2, max_sentences=3)
        self.assertFalse(checker.check_following("Uma."))

    def test_max_sentence_length_pass(self):
        checker = instructions.MaxSentenceLengthChecker("test")
        checker.build_description(max_words_per_sentence=10)
        self.assertTrue(checker.check_following("Frase curta. Outra frase curta."))

    def test_max_sentence_length_fail(self):
        checker = instructions.MaxSentenceLengthChecker("test")
        checker.build_description(max_words_per_sentence=3)
        self.assertFalse(checker.check_following("Esta frase tem mais de três palavras."))

    def test_min_sentence_length_pass(self):
        checker = instructions.MinSentenceLengthChecker("test")
        checker.build_description(min_words_per_sentence=3)
        self.assertTrue(checker.check_following("Esta frase funciona. Outra frase também."))

    def test_min_sentence_length_fail(self):
        checker = instructions.MinSentenceLengthChecker("test")
        checker.build_description(min_words_per_sentence=5)
        self.assertFalse(checker.check_following("Curta. Muito curta."))


class TestParagraphCountInstructions(unittest.TestCase):
    """Testes para instruções de contagem de parágrafos."""

    def test_exact_paragraph_count_pass(self):
        checker = instructions.ExactParagraphCountChecker("test")
        checker.build_description(num_paragraphs=2)
        texto = "Primeiro parágrafo.\n\nSegundo parágrafo."
        self.assertTrue(checker.check_following(texto))

    def test_exact_paragraph_count_fail(self):
        checker = instructions.ExactParagraphCountChecker("test")
        checker.build_description(num_paragraphs=3)
        texto = "Apenas um parágrafo."
        self.assertFalse(checker.check_following(texto))

    def test_min_paragraph_count_pass(self):
        checker = instructions.MinParagraphCountChecker("test")
        checker.build_description(min_paragraphs=2)
        texto = "Primeiro.\n\nSegundo.\n\nTerceiro."
        self.assertTrue(checker.check_following(texto))

    def test_min_paragraph_count_fail(self):
        checker = instructions.MinParagraphCountChecker("test")
        checker.build_description(min_paragraphs=3)
        texto = "Apenas um parágrafo."
        self.assertFalse(checker.check_following(texto))

    def test_exact_line_count_pass(self):
        checker = instructions.ExactLineCountChecker("test")
        checker.build_description(num_lines=3)
        texto = "Linha 1\nLinha 2\nLinha 3"
        self.assertTrue(checker.check_following(texto))

    def test_exact_line_count_fail(self):
        checker = instructions.ExactLineCountChecker("test")
        checker.build_description(num_lines=3)
        texto = "Apenas uma linha"
        self.assertFalse(checker.check_following(texto))


class TestNumberInstructions(unittest.TestCase):
    """Testes para instruções relacionadas a números."""

    def test_exact_number_count_pass(self):
        checker = instructions.ExactNumberCountChecker("test")
        checker.build_description(N=2)
        self.assertTrue(checker.check_following("Em 1899 e 1956 aconteceram eventos."))

    def test_exact_number_count_fail(self):
        checker = instructions.ExactNumberCountChecker("test")
        checker.build_description(N=2)
        self.assertFalse(checker.check_following("Em 1899 aconteceu algo."))

    def test_min_number_count_pass(self):
        checker = instructions.MinNumberCountChecker("test")
        checker.build_description(min_numbers=2)
        self.assertTrue(checker.check_following("Tinha 10, 20 e 30 itens."))

    def test_min_number_count_fail(self):
        checker = instructions.MinNumberCountChecker("test")
        checker.build_description(min_numbers=3)
        self.assertFalse(checker.check_following("Apenas 1 número."))

    def test_no_numbers_pass(self):
        checker = instructions.NoNumbersChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("Sem números aqui."))

    def test_no_numbers_fail(self):
        checker = instructions.NoNumbersChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Tem o número 42 aqui."))

    def test_include_specific_number_pass(self):
        checker = instructions.IncludeSpecificNumberChecker("test")
        checker.build_description(number=1899)
        self.assertTrue(checker.check_following("Em 1899 foi publicado."))

    def test_include_specific_number_fail(self):
        checker = instructions.IncludeSpecificNumberChecker("test")
        checker.build_description(number=1899)
        self.assertFalse(checker.check_following("Em 1900 foi publicado."))


class TestWordInstructions(unittest.TestCase):
    """Testes para instruções de palavras obrigatórias/proibidas."""

    def test_include_word_pass(self):
        checker = instructions.IncludeWordChecker("test")
        checker.build_description(word="literatura")
        self.assertTrue(checker.check_following("A literatura brasileira é rica."))

    def test_include_word_fail(self):
        checker = instructions.IncludeWordChecker("test")
        checker.build_description(word="literatura")
        self.assertFalse(checker.check_following("O texto brasileiro é rico."))

    def test_include_words_pass(self):
        checker = instructions.IncludeWordsChecker("test")
        checker.build_description(words=["autor", "obra"])
        self.assertTrue(checker.check_following("O autor escreveu uma grande obra."))

    def test_include_words_fail(self):
        checker = instructions.IncludeWordsChecker("test")
        checker.build_description(words=["autor", "obra"])
        self.assertFalse(checker.check_following("O escritor fez um livro."))

    def test_word_frequency_pass(self):
        checker = instructions.WordFrequencyChecker("test")
        checker.build_description(word="texto", count=3)
        self.assertTrue(checker.check_following("O texto é bom. Este texto exemplifica. Outro texto aqui."))

    def test_word_frequency_fail(self):
        checker = instructions.WordFrequencyChecker("test")
        checker.build_description(word="texto", count=3)
        self.assertFalse(checker.check_following("O texto é bom."))

    def test_min_word_frequency_pass(self):
        checker = instructions.MinWordFrequencyChecker("test")
        checker.build_description(word="obra", min_count=2)
        self.assertTrue(checker.check_following("A obra é boa. Outra obra também."))

    def test_min_word_frequency_fail(self):
        checker = instructions.MinWordFrequencyChecker("test")
        checker.build_description(word="obra", min_count=3)
        self.assertFalse(checker.check_following("A obra é boa."))

    def test_forbidden_word_pass(self):
        checker = instructions.ForbiddenWordChecker("test")
        checker.build_description(forbidden_word="muito")
        self.assertTrue(checker.check_following("O texto é bom."))

    def test_forbidden_word_fail(self):
        checker = instructions.ForbiddenWordChecker("test")
        checker.build_description(forbidden_word="muito")
        self.assertFalse(checker.check_following("O texto é muito bom."))

    def test_forbidden_words_list_pass(self):
        checker = instructions.ForbiddenWordsListChecker("test")
        checker.build_description(forbidden_words=["muito", "sempre", "nunca"])
        self.assertTrue(checker.check_following("O texto é bom."))

    def test_forbidden_words_list_fail(self):
        checker = instructions.ForbiddenWordsListChecker("test")
        checker.build_description(forbidden_words=["muito", "sempre", "nunca"])
        self.assertFalse(checker.check_following("O texto é sempre bom."))


class TestPronounInstructions(unittest.TestCase):
    """Testes para instruções de pronomes."""

    def test_no_first_person_pass(self):
        checker = instructions.NoFirstPersonChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("O autor escreve bem."))

    def test_no_first_person_fail_eu(self):
        checker = instructions.NoFirstPersonChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Eu escrevo bem."))

    def test_no_first_person_fail_nos(self):
        checker = instructions.NoFirstPersonChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Nós escrevemos bem."))

    def test_no_first_person_fail_meu(self):
        checker = instructions.NoFirstPersonChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("O meu livro é bom."))

    def test_no_second_person_pass(self):
        checker = instructions.NoSecondPersonChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("O autor escreve bem."))

    def test_no_second_person_fail_voce(self):
        checker = instructions.NoSecondPersonChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Você escreve bem."))

    def test_no_second_person_fail_tu(self):
        checker = instructions.NoSecondPersonChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Tu escreves bem."))

    def test_use_first_person_pass(self):
        checker = instructions.UseFirstPersonChecker("test")
        checker.build_description(min_count=2)
        self.assertTrue(checker.check_following("Eu acredito que meu livro é bom."))

    def test_use_first_person_fail(self):
        checker = instructions.UseFirstPersonChecker("test")
        checker.build_description(min_count=3)
        self.assertFalse(checker.check_following("Eu acredito nisso."))

    def test_use_third_person_pass(self):
        checker = instructions.UseThirdPersonChecker("test")
        checker.build_description(min_count=2)
        self.assertTrue(checker.check_following("Ele disse que ela é inteligente."))

    def test_use_third_person_fail(self):
        checker = instructions.UseThirdPersonChecker("test")
        checker.build_description(min_count=3)
        self.assertFalse(checker.check_following("Ele é bom."))


class TestPunctuationInstructions(unittest.TestCase):
    """Testes para instruções de pontuação."""

    def test_no_questions_pass(self):
        checker = instructions.NoQuestionsChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("Isto é uma afirmação."))

    def test_no_questions_fail(self):
        checker = instructions.NoQuestionsChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Isto é uma pergunta?"))

    def test_no_exclamations_pass(self):
        checker = instructions.NoExclamationsChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("Isto é calmo."))

    def test_no_exclamations_fail(self):
        checker = instructions.NoExclamationsChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Isto é incrível!"))

    def test_only_declarative_pass(self):
        checker = instructions.OnlyDeclarativeSentencesChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("Primeira frase. Segunda frase."))

    def test_only_declarative_fail_question(self):
        checker = instructions.OnlyDeclarativeSentencesChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Primeira frase. Segunda?"))

    def test_only_declarative_fail_exclamation(self):
        checker = instructions.OnlyDeclarativeSentencesChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Primeira frase. Segunda!"))

    def test_include_question_pass(self):
        checker = instructions.IncludeQuestionChecker("test")
        checker.build_description(min_questions=1)
        self.assertTrue(checker.check_following("O que aconteceu?"))

    def test_include_question_fail(self):
        checker = instructions.IncludeQuestionChecker("test")
        checker.build_description(min_questions=2)
        self.assertFalse(checker.check_following("Apenas uma pergunta?"))

    def test_include_quote_pass(self):
        checker = instructions.IncludeQuoteChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following('Ele disse "isso é importante" para todos.'))

    def test_include_quote_fail(self):
        checker = instructions.IncludeQuoteChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Sem citações aqui."))

    def test_use_semicolon_pass(self):
        checker = instructions.UseSemicolonChecker("test")
        checker.build_description(min_count=1)
        self.assertTrue(checker.check_following("Primeira parte; segunda parte."))

    def test_use_semicolon_fail(self):
        checker = instructions.UseSemicolonChecker("test")
        checker.build_description(min_count=2)
        self.assertFalse(checker.check_following("Sem ponto e vírgula."))

    def test_use_colon_pass(self):
        checker = instructions.UseColonChecker("test")
        checker.build_description(min_count=1)
        self.assertTrue(checker.check_following("Exemplo: isto é um teste."))

    def test_use_colon_fail(self):
        checker = instructions.UseColonChecker("test")
        checker.build_description(min_count=2)
        self.assertFalse(checker.check_following("Sem dois pontos."))


class TestStructureInstructions(unittest.TestCase):
    """Testes para instruções de estrutura."""

    def test_start_with_word_pass(self):
        checker = instructions.StartWithWordChecker("test")
        checker.build_description(word="A")
        self.assertTrue(checker.check_following("A literatura é importante."))

    def test_start_with_word_fail(self):
        checker = instructions.StartWithWordChecker("test")
        checker.build_description(word="A")
        self.assertFalse(checker.check_following("O livro é bom."))

    def test_end_with_word_pass(self):
        checker = instructions.EndWithWordChecker("test")
        checker.build_description(word="literatura")
        self.assertTrue(checker.check_following("Isto é sobre literatura."))

    def test_end_with_word_fail(self):
        checker = instructions.EndWithWordChecker("test")
        checker.build_description(word="literatura")
        self.assertFalse(checker.check_following("Isto é sobre livros."))

    def test_start_end_same_word_pass(self):
        checker = instructions.StartEndSameWordChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("Literatura é a arte da literatura."))

    def test_start_end_same_word_fail(self):
        checker = instructions.StartEndSameWordChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Literatura é a arte dos livros."))

    def test_bullet_list_pass(self):
        checker = instructions.BulletListChecker("test")
        checker.build_description(min_items=3)
        texto = "- Item 1\n- Item 2\n- Item 3"
        self.assertTrue(checker.check_following(texto))

    def test_bullet_list_fail(self):
        checker = instructions.BulletListChecker("test")
        checker.build_description(min_items=3)
        texto = "- Item 1\n- Item 2"
        self.assertFalse(checker.check_following(texto))

    def test_numbered_list_pass(self):
        checker = instructions.NumberedListChecker("test")
        checker.build_description(min_items=3)
        texto = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertTrue(checker.check_following(texto))

    def test_numbered_list_fail(self):
        checker = instructions.NumberedListChecker("test")
        checker.build_description(min_items=3)
        texto = "1. Item 1\n2. Item 2"
        self.assertFalse(checker.check_following(texto))

    def test_all_caps_pass(self):
        checker = instructions.AllCapsChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("TUDO EM MAIÚSCULAS."))

    def test_all_caps_fail(self):
        checker = instructions.AllCapsChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Misturado com minúsculas."))

    def test_all_lowercase_pass(self):
        checker = instructions.AllLowercaseChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("tudo em minúsculas."))

    def test_all_lowercase_fail(self):
        checker = instructions.AllLowercaseChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Misturado com Maiúsculas."))

    def test_title_case_start_pass(self):
        checker = instructions.TitleCaseStartChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("Primeira frase. Segunda frase."))

    def test_title_case_start_fail(self):
        checker = instructions.TitleCaseStartChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Primeira frase. segunda frase."))

    def test_no_repeat_sentence_start_pass(self):
        checker = instructions.NoRepeatSentenceStartChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("O gato dormia. A casa era grande."))

    def test_no_repeat_sentence_start_fail(self):
        checker = instructions.NoRepeatSentenceStartChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("O gato dormia. O cachorro brincava."))

    def test_each_line_starts_with_pass(self):
        checker = instructions.EachLineStartsWithChecker("test")
        checker.build_description(char="-")
        texto = "- Linha 1\n- Linha 2\n- Linha 3"
        self.assertTrue(checker.check_following(texto))

    def test_each_line_starts_with_fail(self):
        checker = instructions.EachLineStartsWithChecker("test")
        checker.build_description(char="-")
        texto = "- Linha 1\nLinha 2\n- Linha 3"
        self.assertFalse(checker.check_following(texto))

    def test_acrostic_pass(self):
        checker = instructions.AcrosticChecker("test")
        checker.build_description(word="LER")
        texto = "Literatura é arte. Escrever é criar. Reencontrar a beleza."
        self.assertTrue(checker.check_following(texto))

    def test_acrostic_fail(self):
        checker = instructions.AcrosticChecker("test")
        checker.build_description(word="LER")
        texto = "Arte é bela. Bonito é o mundo. Casa grande."
        self.assertFalse(checker.check_following(texto))


class TestPortugueseLinguisticInstructions(unittest.TestCase):
    """Testes para instruções de características linguísticas do português."""

    # =================================================================
    # TESTES DE TERMINAÇÃO -ANDO, -ENDO, -INDO
    # Verifica QUALQUER palavra com essa terminação (sem exceções)
    # =================================================================
    def test_terminacao_ando_endo_indo_limit_pass(self):
        checker = instructions.TerminacaoAndoEndoIndoLimitChecker("test")
        checker.build_description(max_count=2)
        self.assertTrue(checker.check_following("Estou escrevendo e lendo."))

    def test_terminacao_ando_endo_indo_limit_fail(self):
        checker = instructions.TerminacaoAndoEndoIndoLimitChecker("test")
        checker.build_description(max_count=2)
        self.assertFalse(checker.check_following("Estou escrevendo, lendo e falando."))

    def test_terminacao_ando_endo_indo_conta_todas(self):
        """'quando' e 'lindo' terminam em -ando/-indo, então contam."""
        checker = instructions.TerminacaoAndoEndoIndoLimitChecker("test")
        checker.build_description(max_count=0)
        # "quando" termina em -ando, "lindo" termina em -indo
        self.assertFalse(checker.check_following("Quando cheguei, estava lindo."))

    def test_terminacao_ando_endo_indo_min_pass(self):
        checker = instructions.TerminacaoAndoEndoIndoMinChecker("test")
        checker.build_description(min_count=2)
        self.assertTrue(checker.check_following("Estou escrevendo e lendo muito."))

    def test_terminacao_ando_endo_indo_min_fail(self):
        checker = instructions.TerminacaoAndoEndoIndoMinChecker("test")
        checker.build_description(min_count=3)
        self.assertFalse(checker.check_following("Estou escrevendo."))

    # =================================================================
    # TESTES DE TERMINAÇÃO -INHO, -INHA, -ZINHO, -ZINHA
    # Verifica QUALQUER palavra com essa terminação (sem exceções)
    # =================================================================
    def test_terminacao_inho_inha_min_pass(self):
        checker = instructions.TerminacaoInhoInhaMinChecker("test")
        checker.build_description(min_count=2)
        self.assertTrue(checker.check_following("O livrinho estava na mesinha."))

    def test_terminacao_inho_inha_min_fail(self):
        checker = instructions.TerminacaoInhoInhaMinChecker("test")
        checker.build_description(min_count=2)
        self.assertFalse(checker.check_following("O livro estava na mesa."))

    def test_terminacao_inho_inha_conta_todas(self):
        """'caminho' e 'galinha' terminam em -inho/-inha, então contam."""
        checker = instructions.TerminacaoInhoInhaMinChecker("test")
        checker.build_description(min_count=2)
        # "caminho" termina em -inho, "galinha" termina em -inha
        self.assertTrue(checker.check_following("O caminho para a galinha."))

    def test_terminacao_inho_inha_proibido_pass(self):
        checker = instructions.TerminacaoInhoInhaProibidoChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("O livro estava na mesa."))

    def test_terminacao_inho_inha_proibido_fail(self):
        checker = instructions.TerminacaoInhoInhaProibidoChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("O livrinho estava na mesinha."))

    # =================================================================
    # TESTES DE TERMINAÇÃO -ÃO, -ÕES, -ONA, -ONAS
    # =================================================================
    def test_terminacao_ao_oes_min_pass(self):
        checker = instructions.TerminacaoAoOesMinChecker("test")
        checker.build_description(min_count=1)
        self.assertTrue(checker.check_following("O casarão era enorme."))

    def test_terminacao_ao_oes_min_fail(self):
        checker = instructions.TerminacaoAoOesMinChecker("test")
        checker.build_description(min_count=2)
        self.assertFalse(checker.check_following("O homem chegou."))

    def test_adverb_mente_limit_pass(self):
        checker = instructions.AdverbMenteLimitChecker("test")
        checker.build_description(max_adverbs=2)
        self.assertTrue(checker.check_following("Ele escreveu rapidamente e cuidadosamente."))

    def test_adverb_mente_limit_fail(self):
        checker = instructions.AdverbMenteLimitChecker("test")
        checker.build_description(max_adverbs=1)
        self.assertFalse(checker.check_following("Ele escreveu rapidamente e cuidadosamente."))

    def test_min_adverb_mente_pass(self):
        checker = instructions.MinAdverbMenteChecker("test")
        checker.build_description(min_adverbs=2)
        self.assertTrue(checker.check_following("Ele escreveu rapidamente e cuidadosamente."))

    def test_min_adverb_mente_fail(self):
        checker = instructions.MinAdverbMenteChecker("test")
        checker.build_description(min_adverbs=3)
        self.assertFalse(checker.check_following("Ele escreveu rapidamente."))

    def test_no_adverb_mente_pass(self):
        checker = instructions.NoAdverbMenteChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("Ele escreveu bem."))

    def test_no_adverb_mente_fail(self):
        checker = instructions.NoAdverbMenteChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("Ele escreveu rapidamente."))

    def test_conjunction_count_pass(self):
        checker = instructions.ConjunctionCountChecker("test")
        checker.build_description(min_count=3)
        self.assertTrue(checker.check_following("Ele foi e voltou, mas não quis ou pôde explicar."))

    def test_conjunction_count_fail(self):
        checker = instructions.ConjunctionCountChecker("test")
        checker.build_description(min_count=5)
        self.assertFalse(checker.check_following("Ele foi e voltou."))

    def test_connective_pass(self):
        checker = instructions.ConnectiveChecker("test")
        checker.build_description(min_connectives=2)
        self.assertTrue(checker.check_following("Portanto, além disso, o texto é bom."))

    def test_connective_pass_new(self):
        checker = instructions.ConnectiveChecker("test")
        checker.build_description(min_connectives=4)
        self.assertTrue(checker.check_following(
            "Por isso devemos agir. Em consequência, o resultado foi positivo. "
            "Ou seja, tudo deu certo. Nesse sentido, a análise confirma."
        ))

    def test_connective_fail(self):
        checker = instructions.ConnectiveChecker("test")
        checker.build_description(min_connectives=3)
        self.assertFalse(checker.check_following("Portanto o texto é bom."))

    def test_temporal_marker_pass(self):
        checker = instructions.TemporalMarkerChecker("test")
        checker.build_description(min_markers=2)
        self.assertTrue(checker.check_following("Primeiro ele chegou. Depois ele saiu."))

    def test_temporal_marker_fail(self):
        checker = instructions.TemporalMarkerChecker("test")
        checker.build_description(min_markers=3)
        self.assertFalse(checker.check_following("Primeiro ele chegou."))

    def test_contrast_marker_pass(self):
        checker = instructions.ContrastMarkerChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("O livro é bom, no entanto é longo."))

    def test_contrast_marker_fail(self):
        checker = instructions.ContrastMarkerChecker("test")
        checker.build_description()
        self.assertFalse(checker.check_following("O livro é bom e é longo."))

    # REMOVIDO: test_formal_register_* e test_no_superlatives_*
    # Motivo: Instruções removidas por dependerem de listas abertas incompletas

    def test_max_word_repeat_pass(self):
        checker = instructions.MaxWordRepeatChecker("test")
        checker.build_description(max_repeats=2)
        self.assertTrue(checker.check_following("O gato dormia. O cachorro brincava."))

    def test_max_word_repeat_fail(self):
        checker = instructions.MaxWordRepeatChecker("test")
        checker.build_description(max_repeats=2)
        self.assertFalse(checker.check_following("O o o o gato dormia."))


class TestRegistryIntegration(unittest.TestCase):
    """Testes de integração com o registry."""

    def test_all_instructions_instantiate(self):
        """Verifica se todas as instruções podem ser instanciadas."""
        for instr_id, instr_class in instructions_registry.INSTRUCTION_DICT.items():
            with self.subTest(instruction=instr_id):
                inst = instr_class(instr_id)
                desc = inst.build_description()
                self.assertIsInstance(desc, str)
                self.assertTrue(len(desc) > 0)

    def test_all_instructions_have_check_following(self):
        """Verifica se todas as instruções têm o método check_following."""
        for instr_id, instr_class in instructions_registry.INSTRUCTION_DICT.items():
            with self.subTest(instruction=instr_id):
                inst = instr_class(instr_id)
                inst.build_description()
                self.assertTrue(hasattr(inst, 'check_following'))
                self.assertTrue(callable(inst.check_following))

    def test_get_instruction_by_id(self):
        """Testa a função get_instruction_by_id."""
        cls = instructions_registry.get_instruction_by_id("count:min_word_count")
        self.assertEqual(cls, instructions.MinWordCountChecker)

    def test_get_instruction_by_id_invalid(self):
        """Testa get_instruction_by_id com ID inválido."""
        with self.assertRaises(ValueError):
            instructions_registry.get_instruction_by_id("invalid:instruction")

    def test_get_all_instruction_ids(self):
        """Testa a função get_all_instruction_ids."""
        ids = instructions_registry.get_all_instruction_ids()
        self.assertIsInstance(ids, list)
        self.assertTrue(len(ids) > 0)
        self.assertIn("count:min_word_count", ids)

    def test_get_instructions_by_difficulty(self):
        """Testa a função get_instructions_by_difficulty."""
        easy = instructions_registry.get_instructions_by_difficulty("easy")
        medium = instructions_registry.get_instructions_by_difficulty("medium")
        hard = instructions_registry.get_instructions_by_difficulty("hard")

        self.assertTrue(len(easy) > 0)
        self.assertTrue(len(medium) > 0)
        self.assertTrue(len(hard) > 0)

        # Verificar se todas as instruções por dificuldade existem no INSTRUCTION_DICT
        for instr_id in easy + medium + hard:
            self.assertIn(instr_id, instructions_registry.INSTRUCTION_DICT)


class TestEdgeCases(unittest.TestCase):
    """Testes de casos extremos."""

    def test_empty_string(self):
        """Testa comportamento com string vazia."""
        checker = instructions.MinWordCountChecker("test")
        checker.build_description(min_words=1)
        self.assertFalse(checker.check_following(""))

    def test_whitespace_only(self):
        """Testa comportamento com apenas espaços em branco."""
        checker = instructions.MinWordCountChecker("test")
        checker.build_description(min_words=1)
        self.assertFalse(checker.check_following("   \n\t  "))

    def test_special_characters(self):
        """Testa comportamento com caracteres especiais."""
        checker = instructions.IncludeWordChecker("test")
        checker.build_description(word="café")
        self.assertTrue(checker.check_following("Eu gosto de café."))

    def test_accented_characters(self):
        """Testa comportamento com caracteres acentuados."""
        checker = instructions.ForbiddenWordChecker("test")
        checker.build_description(forbidden_word="então")
        self.assertFalse(checker.check_following("Então vamos lá."))
        self.assertTrue(checker.check_following("Logo vamos lá."))

    def test_case_insensitive_word_check(self):
        """Testa se verificações de palavras são case-insensitive."""
        checker = instructions.IncludeWordChecker("test")
        checker.build_description(word="Literatura")
        self.assertTrue(checker.check_following("A LITERATURA é importante."))
        self.assertTrue(checker.check_following("A literatura é importante."))

    def test_unicode_normalization(self):
        """Testa normalização de unicode."""
        checker = instructions.AllLowercaseChecker("test")
        checker.build_description()
        self.assertTrue(checker.check_following("café é bom."))


if __name__ == "__main__":
    # Executar testes
    print("=" * 70)
    print("Executando testes do Capitu")
    print("=" * 70)

    # Criar suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Adicionar todas as classes de teste
    suite.addTests(loader.loadTestsFromTestCase(TestWordCountInstructions))
    suite.addTests(loader.loadTestsFromTestCase(TestSentenceCountInstructions))
    suite.addTests(loader.loadTestsFromTestCase(TestParagraphCountInstructions))
    suite.addTests(loader.loadTestsFromTestCase(TestNumberInstructions))
    suite.addTests(loader.loadTestsFromTestCase(TestWordInstructions))
    suite.addTests(loader.loadTestsFromTestCase(TestPronounInstructions))
    suite.addTests(loader.loadTestsFromTestCase(TestPunctuationInstructions))
    suite.addTests(loader.loadTestsFromTestCase(TestStructureInstructions))
    suite.addTests(loader.loadTestsFromTestCase(TestPortugueseLinguisticInstructions))
    suite.addTests(loader.loadTestsFromTestCase(TestRegistryIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))

    # Executar com verbosidade
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Resumo final
    print("\n" + "=" * 70)
    print(f"Total de testes: {result.testsRun}")
    print(f"Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Falhas: {len(result.failures)}")
    print(f"Erros: {len(result.errors)}")
    print("=" * 70)
