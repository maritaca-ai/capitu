#!/usr/bin/env python3
"""
Módulo de métricas para o Capitu.

Fornece cálculos detalhados de métricas para avaliação de seguimento de instruções.
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import math


@dataclass
class InstructionMetrics:
    """Métricas por instrução."""
    instruction_id: str
    category: str
    total: int = 0
    correct: int = 0
    accuracy: float = 0.0

    def compute_accuracy(self):
        self.accuracy = self.correct / self.total if self.total > 0 else 0.0


@dataclass
class CategoryMetrics:
    """Métricas por categoria de instrução."""
    category: str
    total_instructions: int = 0
    total_correct: int = 0
    accuracy: float = 0.0
    instruction_count: int = 0  # Número de tipos de instrução na categoria


@dataclass
class DifficultyMetrics:
    """Métricas por nível de dificuldade."""
    difficulty: str
    total: int = 0
    correct: int = 0
    accuracy: float = 0.0
    avg_instructions: float = 0.0
    instruction_level_accuracy: float = 0.0  # Acurácia no nível de instrução


@dataclass
class BookMetrics:
    """Métricas por obra literária."""
    book: str
    total: int = 0
    correct: int = 0
    accuracy: float = 0.0
    avg_coherence: float = 0.0


@dataclass
class TurnMetrics:
    """Métricas por turno (multi-turn)."""
    turn: int
    total: int = 0
    correct: int = 0
    accuracy: float = 0.0
    avg_instructions: float = 0.0


@dataclass
class ResponseQualityMetrics:
    """Métricas de qualidade das respostas."""
    avg_word_count: float = 0.0
    avg_char_count: float = 0.0
    avg_unique_words: float = 0.0
    avg_vocabulary_diversity: float = 0.0  # unique_words / total_words
    avg_sentence_count: float = 0.0
    avg_words_per_sentence: float = 0.0


@dataclass
class CoherenceMetrics:
    """Métricas de coerência."""
    avg_coherence: float = 0.0
    min_coherence: float = 0.0
    max_coherence: float = 0.0
    std_coherence: float = 0.0
    coherence_by_difficulty: Dict[str, float] = field(default_factory=dict)
    coherence_by_book: Dict[str, float] = field(default_factory=dict)


@dataclass
class OverallMetrics:
    """Métricas gerais consolidadas."""
    # Acurácias principais
    strict_accuracy: float = 0.0  # % de prompts com TODAS instruções corretas
    loose_accuracy: float = 0.0   # % de prompts com TODAS instruções corretas (modo flexível)
    instruction_level_accuracy: float = 0.0  # % de instruções individuais corretas

    # Pontuações compostas
    final_score: float = 0.0  # Média ponderada de instruções + coerência

    # Totais
    total_prompts: int = 0
    total_instructions: int = 0
    total_instructions_correct: int = 0

    # Contagens por resultado
    prompts_all_correct: int = 0
    prompts_partial_correct: int = 0
    prompts_all_wrong: int = 0


@dataclass
class EvaluationReport:
    """Relatório completo de avaliação."""
    model_name: str = ""
    dataset_name: str = ""
    is_multi_turn: bool = False

    # Métricas principais
    overall: OverallMetrics = field(default_factory=OverallMetrics)
    coherence: CoherenceMetrics = field(default_factory=CoherenceMetrics)
    response_quality: ResponseQualityMetrics = field(default_factory=ResponseQualityMetrics)

    # Métricas detalhadas
    by_instruction: Dict[str, InstructionMetrics] = field(default_factory=dict)
    by_category: Dict[str, CategoryMetrics] = field(default_factory=dict)
    by_difficulty: Dict[str, DifficultyMetrics] = field(default_factory=dict)
    by_book: Dict[str, BookMetrics] = field(default_factory=dict)
    by_turn: Dict[int, TurnMetrics] = field(default_factory=dict)

    # Rankings
    hardest_instructions: List[Tuple[str, float]] = field(default_factory=list)
    easiest_instructions: List[Tuple[str, float]] = field(default_factory=list)
    hardest_books: List[Tuple[str, float]] = field(default_factory=list)


def get_instruction_category(instruction_id: str) -> str:
    """Extrai a categoria do ID da instrução."""
    if ":" in instruction_id:
        return instruction_id.split(":")[0]
    return "unknown"


def compute_std(values: List[float], mean: float) -> float:
    """Calcula desvio padrão."""
    if len(values) < 2:
        return 0.0
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def count_sentences(text: str) -> int:
    """Conta sentenças no texto."""
    if not text:
        return 0
    # Conta terminadores de sentença
    count = text.count('.') + text.count('!') + text.count('?')
    return max(1, count)


def count_unique_words(text: str) -> int:
    """Conta palavras únicas no texto."""
    if not text:
        return 0
    words = text.lower().split()
    return len(set(words))


class MetricsCalculator:
    """Calculadora de métricas para avaliação."""

    def __init__(self):
        self.instruction_stats = defaultdict(lambda: {"correct": 0, "total": 0})
        self.category_stats = defaultdict(lambda: {"correct": 0, "total": 0, "instructions": set()})
        self.difficulty_stats = defaultdict(lambda: {"correct": 0, "total": 0, "instructions_total": 0, "instructions_correct": 0})
        self.book_stats = defaultdict(lambda: {"correct": 0, "total": 0, "coherence_sum": 0.0})
        self.turn_stats = defaultdict(lambda: {"correct": 0, "total": 0, "instructions_sum": 0})

        self.coherence_values = []
        self.coherence_by_difficulty = defaultdict(list)
        self.coherence_by_book = defaultdict(list)

        self.response_word_counts = []
        self.response_char_counts = []
        self.response_unique_words = []
        self.response_sentence_counts = []

        self.total_prompts = 0
        self.total_instructions = 0
        self.total_instructions_correct = 0
        self.prompts_all_correct = 0
        self.prompts_partial_correct = 0
        self.prompts_all_wrong = 0

        self.strict_correct = 0
        self.loose_correct = 0
        self.final_scores = []

    def add_single_turn_result(
        self,
        instruction_ids: List[str],
        follow_list: List[bool],
        follow_all: bool,
        difficulty: str = "unknown",
        book: str = "unknown",
        coherence_score: float = 0.0,
        final_score: float = 0.0,
        response_text: str = "",
        loose_follow_all: bool = False,
    ):
        """Adiciona resultado de uma questão single-turn."""
        self.total_prompts += 1

        # Acurácia estrita/flexível
        if follow_all:
            self.strict_correct += 1
        if loose_follow_all:
            self.loose_correct += 1

        # Contagem por resultado
        correct_count = sum(follow_list)
        if correct_count == len(follow_list):
            self.prompts_all_correct += 1
        elif correct_count == 0:
            self.prompts_all_wrong += 1
        else:
            self.prompts_partial_correct += 1

        # Instruções individuais
        for instr_id, followed in zip(instruction_ids, follow_list):
            self.total_instructions += 1
            if followed:
                self.total_instructions_correct += 1

            self.instruction_stats[instr_id]["total"] += 1
            if followed:
                self.instruction_stats[instr_id]["correct"] += 1

            category = get_instruction_category(instr_id)
            self.category_stats[category]["total"] += 1
            self.category_stats[category]["instructions"].add(instr_id)
            if followed:
                self.category_stats[category]["correct"] += 1

        # Por dificuldade
        self.difficulty_stats[difficulty]["total"] += 1
        self.difficulty_stats[difficulty]["instructions_total"] += len(follow_list)
        self.difficulty_stats[difficulty]["instructions_correct"] += correct_count
        if follow_all:
            self.difficulty_stats[difficulty]["correct"] += 1

        # Por livro
        self.book_stats[book]["total"] += 1
        self.book_stats[book]["coherence_sum"] += coherence_score
        if follow_all:
            self.book_stats[book]["correct"] += 1

        # Coerência
        if coherence_score > 0:
            self.coherence_values.append(coherence_score)
            self.coherence_by_difficulty[difficulty].append(coherence_score)
            self.coherence_by_book[book].append(coherence_score)

        # Qualidade da resposta
        if response_text:
            words = response_text.split()
            self.response_word_counts.append(len(words))
            self.response_char_counts.append(len(response_text))
            self.response_unique_words.append(count_unique_words(response_text))
            self.response_sentence_counts.append(count_sentences(response_text))

        # Pontuação final
        if final_score > 0:
            self.final_scores.append(final_score)

    def add_multi_turn_result(
        self,
        turns: List[dict],
        all_correct: bool,
    ):
        """Adiciona resultado de uma conversa multi-turn."""
        self.total_prompts += 1

        if all_correct:
            self.strict_correct += 1
            self.prompts_all_correct += 1
        else:
            # Verifica se algum turno passou
            any_correct = any(t.get("all_followed", False) for t in turns)
            if any_correct:
                self.prompts_partial_correct += 1
            else:
                self.prompts_all_wrong += 1

        for turn_data in turns:
            turn_num = turn_data.get("turn", 0)
            instruction_ids = turn_data.get("instructions", [])
            follow_list = turn_data.get("followed", [])
            all_followed = turn_data.get("all_followed", False)

            self.turn_stats[turn_num]["total"] += 1
            self.turn_stats[turn_num]["instructions_sum"] += len(instruction_ids)
            if all_followed:
                self.turn_stats[turn_num]["correct"] += 1

            # Instruções individuais
            for instr_id, followed in zip(instruction_ids, follow_list):
                self.total_instructions += 1
                if followed:
                    self.total_instructions_correct += 1

                self.instruction_stats[instr_id]["total"] += 1
                if followed:
                    self.instruction_stats[instr_id]["correct"] += 1

                category = get_instruction_category(instr_id)
                self.category_stats[category]["total"] += 1
                self.category_stats[category]["instructions"].add(instr_id)
                if followed:
                    self.category_stats[category]["correct"] += 1

    def compute_report(self, model_name: str = "", dataset_name: str = "", is_multi_turn: bool = False) -> EvaluationReport:
        """Computa e retorna o relatório completo."""
        report = EvaluationReport(
            model_name=model_name,
            dataset_name=dataset_name,
            is_multi_turn=is_multi_turn,
        )

        # Overall metrics
        report.overall.total_prompts = self.total_prompts
        report.overall.total_instructions = self.total_instructions
        report.overall.total_instructions_correct = self.total_instructions_correct
        report.overall.prompts_all_correct = self.prompts_all_correct
        report.overall.prompts_partial_correct = self.prompts_partial_correct
        report.overall.prompts_all_wrong = self.prompts_all_wrong

        report.overall.strict_accuracy = self.strict_correct / self.total_prompts if self.total_prompts else 0.0
        report.overall.loose_accuracy = self.loose_correct / self.total_prompts if self.total_prompts else 0.0
        report.overall.instruction_level_accuracy = self.total_instructions_correct / self.total_instructions if self.total_instructions else 0.0
        report.overall.final_score = sum(self.final_scores) / len(self.final_scores) if self.final_scores else 0.0

        # Instruction metrics
        for instr_id, stats in self.instruction_stats.items():
            metrics = InstructionMetrics(
                instruction_id=instr_id,
                category=get_instruction_category(instr_id),
                total=stats["total"],
                correct=stats["correct"],
            )
            metrics.compute_accuracy()
            report.by_instruction[instr_id] = metrics

        # Category metrics
        for category, stats in self.category_stats.items():
            report.by_category[category] = CategoryMetrics(
                category=category,
                total_instructions=stats["total"],
                total_correct=stats["correct"],
                accuracy=stats["correct"] / stats["total"] if stats["total"] else 0.0,
                instruction_count=len(stats["instructions"]),
            )

        # Difficulty metrics
        for difficulty, stats in self.difficulty_stats.items():
            if stats["total"] > 0:
                report.by_difficulty[difficulty] = DifficultyMetrics(
                    difficulty=difficulty,
                    total=stats["total"],
                    correct=stats["correct"],
                    accuracy=stats["correct"] / stats["total"],
                    avg_instructions=stats["instructions_total"] / stats["total"],
                    instruction_level_accuracy=stats["instructions_correct"] / stats["instructions_total"] if stats["instructions_total"] else 0.0,
                )

        # Book metrics
        for book, stats in self.book_stats.items():
            if stats["total"] > 0:
                report.by_book[book] = BookMetrics(
                    book=book,
                    total=stats["total"],
                    correct=stats["correct"],
                    accuracy=stats["correct"] / stats["total"],
                    avg_coherence=stats["coherence_sum"] / stats["total"],
                )

        # Turn metrics (multi-turn)
        for turn_num, stats in self.turn_stats.items():
            if stats["total"] > 0:
                report.by_turn[turn_num] = TurnMetrics(
                    turn=turn_num,
                    total=stats["total"],
                    correct=stats["correct"],
                    accuracy=stats["correct"] / stats["total"],
                    avg_instructions=stats["instructions_sum"] / stats["total"],
                )

        # Coherence metrics
        if self.coherence_values:
            avg_coh = sum(self.coherence_values) / len(self.coherence_values)
            report.coherence = CoherenceMetrics(
                avg_coherence=avg_coh,
                min_coherence=min(self.coherence_values),
                max_coherence=max(self.coherence_values),
                std_coherence=compute_std(self.coherence_values, avg_coh),
                coherence_by_difficulty={k: sum(v)/len(v) for k, v in self.coherence_by_difficulty.items() if v},
                coherence_by_book={k: sum(v)/len(v) for k, v in self.coherence_by_book.items() if v},
            )

        # Response quality metrics
        if self.response_word_counts:
            n = len(self.response_word_counts)
            avg_words = sum(self.response_word_counts) / n
            avg_unique = sum(self.response_unique_words) / n
            avg_sentences = sum(self.response_sentence_counts) / n

            report.response_quality = ResponseQualityMetrics(
                avg_word_count=avg_words,
                avg_char_count=sum(self.response_char_counts) / n,
                avg_unique_words=avg_unique,
                avg_vocabulary_diversity=avg_unique / avg_words if avg_words else 0.0,
                avg_sentence_count=avg_sentences,
                avg_words_per_sentence=avg_words / avg_sentences if avg_sentences else 0.0,
            )

        # Rankings
        sorted_by_acc = sorted(report.by_instruction.items(), key=lambda x: x[1].accuracy)
        report.hardest_instructions = [(k, v.accuracy) for k, v in sorted_by_acc[:10]]
        report.easiest_instructions = [(k, v.accuracy) for k, v in reversed(sorted_by_acc[-10:])]

        sorted_books = sorted(report.by_book.items(), key=lambda x: x[1].accuracy)
        report.hardest_books = [(k, v.accuracy) for k, v in sorted_books[:5]]

        return report


def print_report(report: EvaluationReport, verbose: bool = True):
    """Imprime o relatório no terminal."""
    print("\n" + "=" * 80)
    print(f"RELATÓRIO DE AVALIAÇÃO - Capitu")
    if report.model_name:
        print(f"Modelo: {report.model_name}")
    if report.dataset_name:
        print(f"Dataset: {report.dataset_name}")
    print(f"Modo: {'Multi-turn' if report.is_multi_turn else 'Single-turn'}")
    print("=" * 80)

    # Métricas principais
    print("\n MÉTRICAS PRINCIPAIS")
    print("-" * 60)
    o = report.overall
    print(f"  Acurácia Estrita (prompt):     {o.strict_accuracy:6.2%}  ({o.prompts_all_correct}/{o.total_prompts})")
    if o.loose_accuracy > 0:
        print(f"  Acurácia Flexível (prompt):    {o.loose_accuracy:6.2%}")
    print(f"  Acurácia por Instrução:        {o.instruction_level_accuracy:6.2%}  ({o.total_instructions_correct}/{o.total_instructions})")
    if o.final_score > 0:
        print(f"  Pontuação Final (ponderada):   {o.final_score:6.4f}")

    print(f"\n  Prompts 100% corretos:         {o.prompts_all_correct:4d}  ({o.prompts_all_correct/o.total_prompts:.1%})")
    print(f"  Prompts parcialmente corretos: {o.prompts_partial_correct:4d}  ({o.prompts_partial_correct/o.total_prompts:.1%})")
    print(f"  Prompts 0% corretos:           {o.prompts_all_wrong:4d}  ({o.prompts_all_wrong/o.total_prompts:.1%})")

    # Coerência
    if report.coherence.avg_coherence > 0:
        print("\n COERÊNCIA")
        print("-" * 60)
        c = report.coherence
        print(f"  Média:          {c.avg_coherence:.4f}")
        print(f"  Mínimo:         {c.min_coherence:.4f}")
        print(f"  Máximo:         {c.max_coherence:.4f}")
        print(f"  Desvio padrão:  {c.std_coherence:.4f}")

    # Qualidade das respostas
    if report.response_quality.avg_word_count > 0:
        print("\n QUALIDADE DAS RESPOSTAS")
        print("-" * 60)
        q = report.response_quality
        print(f"  Palavras (média):              {q.avg_word_count:.1f}")
        print(f"  Palavras únicas (média):       {q.avg_unique_words:.1f}")
        print(f"  Diversidade vocabular:         {q.avg_vocabulary_diversity:.2%}")
        print(f"  Frases (média):                {q.avg_sentence_count:.1f}")
        print(f"  Palavras por frase:            {q.avg_words_per_sentence:.1f}")

    # Por dificuldade
    if report.by_difficulty:
        print("\n POR DIFICULDADE")
        print("-" * 60)
        print(f"  {'Nível':<10} {'Acurácia':>10} {'Instr.':>10} {'N':>6}")
        print(f"  {'-'*10} {'-'*10} {'-'*10} {'-'*6}")
        for diff in ["easy", "medium", "hard"]:
            if diff in report.by_difficulty:
                d = report.by_difficulty[diff]
                print(f"  {diff.capitalize():<10} {d.accuracy:>9.1%} {d.instruction_level_accuracy:>9.1%} {d.total:>6}")

    # Por categoria
    if verbose and report.by_category:
        print("\n POR CATEGORIA DE INSTRUÇÃO")
        print("-" * 60)
        print(f"  {'Categoria':<15} {'Acurácia':>10} {'Tipos':>8} {'Total':>8}")
        print(f"  {'-'*15} {'-'*10} {'-'*8} {'-'*8}")
        sorted_cats = sorted(report.by_category.items(), key=lambda x: x[1].accuracy)
        for cat, m in sorted_cats:
            print(f"  {cat:<15} {m.accuracy:>9.1%} {m.instruction_count:>8} {m.total_instructions:>8}")

    # Por livro
    if verbose and report.by_book:
        print("\n POR OBRA LITERÁRIA")
        print("-" * 60)
        print(f"  {'Obra':<30} {'Acurácia':>10} {'Coerência':>10} {'N':>6}")
        print(f"  {'-'*30} {'-'*10} {'-'*10} {'-'*6}")
        sorted_books = sorted(report.by_book.items(), key=lambda x: x[1].accuracy)
        for book, m in sorted_books:
            coh_str = f"{m.avg_coherence:.2f}" if m.avg_coherence > 0 else "N/A"
            print(f"  {book:<30} {m.accuracy:>9.1%} {coh_str:>10} {m.total:>6}")

    # Por turno (multi-turn)
    if report.by_turn:
        print("\n POR TURNO")
        print("-" * 60)
        print(f"  {'Turno':<10} {'Acurácia':>10} {'Instruções':>12} {'N':>6}")
        print(f"  {'-'*10} {'-'*10} {'-'*12} {'-'*6}")
        for turn_num in sorted(report.by_turn.keys()):
            t = report.by_turn[turn_num]
            print(f"  Turno {turn_num:<3} {t.accuracy:>9.1%} {t.avg_instructions:>11.1f} {t.total:>6}")

    # Instruções mais difíceis
    if verbose and report.hardest_instructions:
        print("\n INSTRUÇÕES MAIS DIFÍCEIS")
        print("-" * 60)
        for i, (instr_id, acc) in enumerate(report.hardest_instructions[:10], 1):
            bar = "█" * int(acc * 20) + "░" * (20 - int(acc * 20))
            print(f"  {i:2d}. {instr_id:<35} {bar} {acc:5.1%}")

    # Instruções mais fáceis
    if verbose and report.easiest_instructions:
        print("\n INSTRUÇÕES MAIS FÁCEIS")
        print("-" * 60)
        for i, (instr_id, acc) in enumerate(report.easiest_instructions[:10], 1):
            bar = "█" * int(acc * 20) + "░" * (20 - int(acc * 20))
            print(f"  {i:2d}. {instr_id:<35} {bar} {acc:5.1%}")

    print("\n" + "=" * 80)


def save_report_json(report: EvaluationReport, path: Path):
    """Salva o relatório em JSON."""
    data = {
        "model_name": report.model_name,
        "dataset_name": report.dataset_name,
        "is_multi_turn": report.is_multi_turn,
        "overall": asdict(report.overall),
        "coherence": asdict(report.coherence),
        "response_quality": asdict(report.response_quality),
        "by_instruction": {k: asdict(v) for k, v in report.by_instruction.items()},
        "by_category": {k: asdict(v) for k, v in report.by_category.items()},
        "by_difficulty": {k: asdict(v) for k, v in report.by_difficulty.items()},
        "by_book": {k: asdict(v) for k, v in report.by_book.items()},
        "by_turn": {str(k): asdict(v) for k, v in report.by_turn.items()},
        "hardest_instructions": report.hardest_instructions,
        "easiest_instructions": report.easiest_instructions,
        "hardest_books": report.hardest_books,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_markdown_report(report: EvaluationReport, path: Path):
    """Gera relatório em Markdown."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Relatório de Avaliação - Capitu\n\n")

        if report.model_name:
            f.write(f"**Modelo:** {report.model_name}\n\n")
        if report.dataset_name:
            f.write(f"**Dataset:** {report.dataset_name}\n\n")
        f.write(f"**Modo:** {'Multi-turn' if report.is_multi_turn else 'Single-turn'}\n\n")

        # Métricas principais
        f.write("## Métricas Principais\n\n")
        o = report.overall
        f.write("| Métrica | Valor |\n")
        f.write("|---------|-------|\n")
        f.write(f"| Acurácia Estrita (prompt) | {o.strict_accuracy:.2%} ({o.prompts_all_correct}/{o.total_prompts}) |\n")
        if o.loose_accuracy > 0:
            f.write(f"| Acurácia Flexível (prompt) | {o.loose_accuracy:.2%} |\n")
        f.write(f"| Acurácia por Instrução | {o.instruction_level_accuracy:.2%} ({o.total_instructions_correct}/{o.total_instructions}) |\n")
        if o.final_score > 0:
            f.write(f"| Pontuação Final | {o.final_score:.4f} |\n")
        f.write("\n")

        # Distribuição de resultados
        f.write("### Distribuição de Resultados\n\n")
        f.write("| Resultado | Quantidade | Porcentagem |\n")
        f.write("|-----------|------------|-------------|\n")
        f.write(f"| 100% corretos | {o.prompts_all_correct} | {o.prompts_all_correct/o.total_prompts:.1%} |\n")
        f.write(f"| Parcialmente corretos | {o.prompts_partial_correct} | {o.prompts_partial_correct/o.total_prompts:.1%} |\n")
        f.write(f"| 0% corretos | {o.prompts_all_wrong} | {o.prompts_all_wrong/o.total_prompts:.1%} |\n")
        f.write("\n")

        # Por dificuldade
        if report.by_difficulty:
            f.write("## Resultados por Dificuldade\n\n")
            f.write("| Dificuldade | Acurácia (prompt) | Acurácia (instrução) | Total |\n")
            f.write("|-------------|-------------------|----------------------|-------|\n")
            for diff in ["easy", "medium", "hard"]:
                if diff in report.by_difficulty:
                    d = report.by_difficulty[diff]
                    f.write(f"| {diff.capitalize()} | {d.accuracy:.1%} | {d.instruction_level_accuracy:.1%} | {d.total} |\n")
            f.write("\n")

        # Por categoria
        if report.by_category:
            f.write("## Resultados por Categoria de Instrução\n\n")
            f.write("| Categoria | Acurácia | Tipos | Total |\n")
            f.write("|-----------|----------|-------|-------|\n")
            sorted_cats = sorted(report.by_category.items(), key=lambda x: x[1].accuracy)
            for cat, m in sorted_cats:
                f.write(f"| {cat} | {m.accuracy:.1%} | {m.instruction_count} | {m.total_instructions} |\n")
            f.write("\n")

        # Por livro
        if report.by_book:
            f.write("## Resultados por Obra Literária\n\n")
            f.write("| Obra | Acurácia | Coerência | Total |\n")
            f.write("|------|----------|-----------|-------|\n")
            sorted_books = sorted(report.by_book.items(), key=lambda x: x[1].accuracy)
            for book, m in sorted_books:
                coh_str = f"{m.avg_coherence:.2f}" if m.avg_coherence > 0 else "N/A"
                f.write(f"| {book} | {m.accuracy:.1%} | {coh_str} | {m.total} |\n")
            f.write("\n")

        # Instruções mais difíceis
        if report.hardest_instructions:
            f.write("## Instruções Mais Difíceis\n\n")
            f.write("| # | Instrução | Acurácia |\n")
            f.write("|---|-----------|----------|\n")
            for i, (instr_id, acc) in enumerate(report.hardest_instructions, 1):
                f.write(f"| {i} | `{instr_id}` | {acc:.1%} |\n")
            f.write("\n")

        # Instruções mais fáceis
        if report.easiest_instructions:
            f.write("## Instruções Mais Fáceis\n\n")
            f.write("| # | Instrução | Acurácia |\n")
            f.write("|---|-----------|----------|\n")
            for i, (instr_id, acc) in enumerate(report.easiest_instructions, 1):
                f.write(f"| {i} | `{instr_id}` | {acc:.1%} |\n")
            f.write("\n")

        # Coerência
        if report.coherence.avg_coherence > 0:
            f.write("## Métricas de Coerência\n\n")
            c = report.coherence
            f.write("| Métrica | Valor |\n")
            f.write("|---------|-------|\n")
            f.write(f"| Média | {c.avg_coherence:.4f} |\n")
            f.write(f"| Mínimo | {c.min_coherence:.4f} |\n")
            f.write(f"| Máximo | {c.max_coherence:.4f} |\n")
            f.write(f"| Desvio Padrão | {c.std_coherence:.4f} |\n")
            f.write("\n")

        # Qualidade das respostas
        if report.response_quality.avg_word_count > 0:
            f.write("## Qualidade das Respostas\n\n")
            q = report.response_quality
            f.write("| Métrica | Valor |\n")
            f.write("|---------|-------|\n")
            f.write(f"| Palavras (média) | {q.avg_word_count:.1f} |\n")
            f.write(f"| Palavras únicas (média) | {q.avg_unique_words:.1f} |\n")
            f.write(f"| Diversidade vocabular | {q.avg_vocabulary_diversity:.2%} |\n")
            f.write(f"| Frases (média) | {q.avg_sentence_count:.1f} |\n")
            f.write(f"| Palavras por frase | {q.avg_words_per_sentence:.1f} |\n")
            f.write("\n")
