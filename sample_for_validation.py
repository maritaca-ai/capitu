#!/usr/bin/env python3
"""
Generate a manual verification document with 100 sampled cases.

Sampling strategy:
- 6 diverse models across tiers
- Stratified by: pass/fail, instruction category, difficulty
- Prioritize boundary cases (failed from good models, hardest instructions)
- Exactly 100 cases for human annotation

Outputs:
  - validation/manual_verification_100.jsonl (structured data)
  - validation/manual_verification_100.md (human-readable review doc)
"""

import json
import random
from pathlib import Path
from collections import defaultdict

random.seed(42)

RUNS_DIR = Path("runs")
DATA_DIR = Path("data")
OUTPUT_DIR = Path("validation")

# 6 representative models across performance tiers
MODELS = [
    "think-gpt-5.2",     # Best (98.5% strict)
    "claude-sonnet-4.5",  # Mid-high, different family
    "gemini-3-flash",     # Mid, different family
    "qwen3-235b",         # Open-weight
    "sabiazinho-4",       # Portuguese-specialized
    "sabia-3.1",          # Weaker Portuguese model
]


def load_input_questions():
    """Load input questions to get kwargs for each question."""
    questions = {}
    with open(DATA_DIR / "input_questions.jsonl") as f:
        for i, line in enumerate(f):
            d = json.loads(line)
            questions[i] = d
    return questions


def load_model_data(model_name):
    """Load eval results matched with response metadata."""
    eval_path = RUNS_DIR / model_name / "eval" / "single-turn" / "eval_results_strict.jsonl"
    resp_path = RUNS_DIR / model_name / "single-turn" / "responses.jsonl"

    if not eval_path.exists() or not resp_path.exists():
        print(f"  Skipping {model_name}: missing files")
        return []

    # Responses indexed by prompt prefix
    resp_by_prompt = {}
    with open(resp_path) as f:
        for line in f:
            r = json.loads(line)
            resp_by_prompt[r["prompt"][:200]] = r

    # Eval results
    results = []
    with open(eval_path) as f:
        for i, line in enumerate(f):
            e = json.loads(line)
            r = resp_by_prompt.get(e["prompt"][:200])
            if r:
                results.append({
                    "model": model_name,
                    "question_idx": i,
                    "key": r.get("key", i),
                    "prompt": e["prompt"],
                    "response": e["response"],
                    "difficulty": r.get("difficulty", "unknown"),
                    "book": r.get("book", "unknown"),
                    "instruction_ids": e["instruction_id_list"],
                    "follow_all": e["follow_all_instructions"],
                    "follow_list": e["follow_instruction_list"],
                })

    return results


def get_category(instruction_id):
    return instruction_id.split(":")[0]


def sample_100_cases(all_cases, input_questions):
    """
    Sample exactly 100 cases with stratified coverage:
    - ~45 FAIL cases (verify auto-eval correctly detects failures)
    - ~45 PASS cases (verify auto-eval doesn't give false positives)
    - ~10 from hardest instructions (boundary cases)
    """
    # Separate by auto verdict at instruction level
    fail_items = []  # (case, instruction_index) where instruction failed
    pass_items = []  # (case, instruction_index) where instruction passed

    for case in all_cases:
        for i, (iid, passed) in enumerate(zip(case["instruction_ids"], case["follow_list"])):
            item = (case, i, iid, get_category(iid))
            if passed:
                pass_items.append(item)
            else:
                fail_items.append(item)

    random.shuffle(fail_items)
    random.shuffle(pass_items)

    selected = []
    seen = set()  # (model, question_idx, instruction_idx) to avoid duplicates

    def add_item(case, instr_idx, verdict_label):
        key = (case["model"], case["question_idx"], instr_idx)
        if key in seen:
            return False
        seen.add(key)
        selected.append({
            "case": case,
            "focus_idx": instr_idx,
            "focus_id": case["instruction_ids"][instr_idx],
            "focus_verdict": verdict_label,
        })
        return True

    # --- 1. FAIL cases: stratify by category ---
    fail_by_cat = defaultdict(list)
    for case, idx, iid, cat in fail_items:
        fail_by_cat[cat].append((case, idx))

    target_fail = 45
    cats = sorted(fail_by_cat.keys())
    per_cat = max(3, target_fail // max(len(cats), 1))

    for cat in cats:
        count = 0
        for case, idx in fail_by_cat[cat]:
            if count >= per_cat:
                break
            if add_item(case, idx, "FAIL"):
                count += 1
        if len(selected) >= target_fail:
            break

    # Fill remaining fail slots
    for case, idx, iid, cat in fail_items:
        if len(selected) >= target_fail:
            break
        add_item(case, idx, "FAIL")

    n_fail = len(selected)

    # --- 2. PASS cases: stratify by difficulty and category ---
    pass_by_diff_cat = defaultdict(list)
    for case, idx, iid, cat in pass_items:
        pass_by_diff_cat[(case["difficulty"], cat)].append((case, idx))

    target_pass = 45
    for (diff, cat), items in sorted(pass_by_diff_cat.items()):
        if len(selected) >= n_fail + target_pass:
            break
        count = 0
        for case, idx in items:
            if count >= 3:
                break
            if add_item(case, idx, "PASS"):
                count += 1

    # Fill remaining pass slots
    for case, idx, iid, cat in pass_items:
        if len(selected) >= n_fail + target_pass:
            break
        add_item(case, idx, "PASS")

    n_pass = len(selected) - n_fail

    # --- 3. Hardest instructions (boundary cases) ---
    hardest = [
        "count:exact_word_count", "words:max_word_repeat",
        "count:character_count_range", "structure:acrostic",
        "pattern:terminacao_inho_inha_min", "punctuation:include_quote",
    ]
    remaining = 100 - len(selected)
    boundary_pool = []
    for case, idx, iid, cat in fail_items + pass_items:
        if iid in hardest:
            boundary_pool.append((case, idx, "PASS" if case["follow_list"][idx] else "FAIL"))

    random.shuffle(boundary_pool)
    for case, idx, verdict in boundary_pool:
        if remaining <= 0:
            break
        if add_item(case, idx, verdict):
            remaining -= 1

    print(f"Selected: {n_fail} FAIL + {n_pass} PASS + {len(selected) - n_fail - n_pass} boundary = {len(selected)} total")

    random.shuffle(selected)
    return selected[:100]


def build_entry(item, input_questions, case_id):
    """Build a structured verification entry."""
    case = item["case"]
    q = input_questions.get(case["question_idx"], {})
    kwargs_list = q.get("kwargs", [{}] * len(case["instruction_ids"]))

    instructions = []
    for i, (iid, passed) in enumerate(zip(case["instruction_ids"], case["follow_list"])):
        kw = kwargs_list[i] if i < len(kwargs_list) else {}
        instructions.append({
            "instruction_id": iid,
            "category": get_category(iid),
            "parameters": kw,
            "auto_verdict": "PASS" if passed else "FAIL",
        })

    return {
        "case_id": case_id,
        "model": case["model"],
        "difficulty": case["difficulty"],
        "book": case["book"],
        "focus_instruction": item["focus_id"],
        "focus_auto_verdict": item["focus_verdict"],
        "prompt": case["prompt"],
        "response": case["response"],
        "instructions": instructions,
        "all_auto_verdict": "PASS" if case["follow_all"] else "FAIL",
        # Human annotation fields:
        "human_verdict": "",           # PASS / FAIL / UNCERTAIN
        "human_agrees_with_auto": "",  # YES / NO
        "human_notes": "",
    }


def write_markdown(entries, output_path):
    """Write human-readable review document."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# CAPITU - Verificação Manual de 100 Casos\n\n")
        f.write("**Instruções para o revisor:**\n")
        f.write("- Para cada caso, a **instrução em foco** está destacada\n")
        f.write("- Verifique se o veredito automático (PASS/FAIL) está correto\n")
        f.write("- Preencha: `[CONCORDO]` ou `[DISCORDO]` e adicione notas se necessário\n\n")
        f.write("---\n\n")

        for e in entries:
            verdict_emoji = "✅" if e["focus_auto_verdict"] == "PASS" else "❌"
            f.write(f"## Caso {e['case_id']} — {verdict_emoji} {e['focus_auto_verdict']}\n\n")
            f.write(f"- **Modelo:** {e['model']}\n")
            f.write(f"- **Dificuldade:** {e['difficulty']}\n")
            f.write(f"- **Obra:** {e['book']}\n")
            f.write(f"- **Instrução em foco:** `{e['focus_instruction']}` → Auto: **{e['focus_auto_verdict']}**\n\n")

            f.write("**Todas as instruções:**\n\n")
            for instr in e["instructions"]:
                marker = "→" if instr["instruction_id"] == e["focus_instruction"] else " "
                params = ""
                if instr["parameters"]:
                    params = " " + str(instr["parameters"])
                f.write(f"  {marker} `{instr['instruction_id']}`{params} — {instr['auto_verdict']}\n")

            f.write(f"\n**Prompt:**\n\n> {e['prompt']}\n\n")

            # Truncate very long responses for readability
            response = e["response"]
            if len(response) > 2000:
                response = response[:2000] + "\n[... truncado, ver JSONL para resposta completa ...]"
            f.write(f"**Resposta do modelo:**\n\n```\n{response}\n```\n\n")

            f.write("**Verificação humana:**\n\n")
            f.write("- [ ] CONCORDO com veredito automático\n")
            f.write("- [ ] DISCORDO — veredito correto seria: ___\n")
            f.write("- Notas: \n\n")
            f.write("---\n\n")

    print(f"Wrote markdown to {output_path}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading input questions...")
    input_questions = load_input_questions()
    print(f"  {len(input_questions)} questions loaded\n")

    all_cases = []
    for model in MODELS:
        print(f"Loading {model}...")
        cases = load_model_data(model)
        print(f"  {len(cases)} cases")
        all_cases.extend(cases)

    print(f"\nTotal: {len(all_cases)} cases across {len(MODELS)} models\n")

    selected = sample_100_cases(all_cases, input_questions)

    # Build entries
    entries = []
    for i, item in enumerate(selected):
        entries.append(build_entry(item, input_questions, i + 1))

    # Write JSONL
    jsonl_path = OUTPUT_DIR / "manual_verification_100.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"Wrote JSONL to {jsonl_path}")

    # Write Markdown
    md_path = OUTPUT_DIR / "manual_verification_100.md"
    write_markdown(entries, md_path)

    # Summary stats
    models = defaultdict(int)
    diffs = defaultdict(int)
    verdicts = defaultdict(int)
    cats = defaultdict(int)

    for e in entries:
        models[e["model"]] += 1
        diffs[e["difficulty"]] += 1
        verdicts[e["focus_auto_verdict"]] += 1
        cats[get_category(e["focus_instruction"])] += 1

    print("\n=== Distribuição da Amostra ===")
    print("\nPor modelo:")
    for m, c in sorted(models.items(), key=lambda x: -x[1]):
        print(f"  {m}: {c}")
    print("\nPor dificuldade:")
    for d in ["easy", "medium", "hard"]:
        print(f"  {d}: {diffs.get(d, 0)}")
    print("\nPor veredito automático:")
    for v, c in sorted(verdicts.items()):
        print(f"  {v}: {c}")
    print("\nPor categoria de instrução:")
    for cat, c in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {c}")


if __name__ == "__main__":
    main()
