#!/usr/bin/env python3
"""Collect results from runs/ directory and generate summary."""
import json
from pathlib import Path

MODEL_NAMES = {
    "think-gpt-5": "OpenAI GPT-5 (Thinking)",
    "gpt-5-mini": "OpenAI GPT-5-mini (Thinking)",
    "gpt-5.2": "OpenAI GPT-5.2",
    "gemini-3-pro": "Google Gemini 3 Pro (Thinking)",
    "gemini-3-flash": "Google Gemini 3 Flash",
    "claude-sonnet-4.5": "Anthropic Claude Sonnet 4.5",
    "claude-haiku-4.5": "Anthropic Claude Haiku 4.5",
    "qwen3-8b": "Alibaba Qwen 3 8B (Thinking)",
    "qwen3-14b": "Alibaba Qwen 3 14B (Thinking)",
    "qwen3-32b": "Alibaba Qwen 3 32B (Thinking)",
    "qwen3-235b": "Alibaba Qwen 3 235B",
    "sabiazinho-4": "Maritaca Sabiazinho-4",
    "sabia-4": "Maritaca Sabiá-4",
    "sabiazinho-3": "Maritaca Sabiazinho-3",
    "sabia-3": "Maritaca Sabiá-3",
    "sabia-3.1": "Maritaca Sabiá-3.1",
}

MODELS = list(MODEL_NAMES.keys())

runs_dir = Path("runs")

results = []
for model in MODELS:
    model_dir = runs_dir / model
    
    # Single-turn
    single_report = model_dir / "eval" / "single-turn" / "metrics_report.json"
    if single_report.exists():
        with open(single_report) as f:
            data = json.load(f)
        
        # Also check multi-turn
        multi_report = model_dir / "eval" / "multi-turn" / "metrics_report.json"
        multi_data = None
        if multi_report.exists():
            with open(multi_report) as f:
                multi_data = json.load(f)
        
        results.append({
            "model": model,
            "display_name": MODEL_NAMES[model],
            "single": data,
            "multi": multi_data
        })

# Print table
print("# CAPITU Benchmark Results Summary\n")
print("## Single-Turn Results\n")
print("| Model | Strict | Loose | Instr. | Coherence | Final |")
print("|-------|--------|-------|--------|-----------|-------|")
for r in sorted(results, key=lambda x: x["single"]["overall"]["strict_accuracy"], reverse=True):
    s = r["single"]["overall"]
    c = r["single"].get("coherence", {})
    strict = s["strict_accuracy"] * 100
    loose = s["loose_accuracy"] * 100
    instr = s["instruction_level_accuracy"] * 100
    coh = c.get("avg_coherence", 0)
    final = s.get("final_score", 0) * 100
    print(f"| {r['display_name']} | {strict:.1f}% | {loose:.1f}% | {instr:.1f}% | {coh:.3f} | {final:.1f}% |")

print("\n## Multi-Turn Results\n")
print("| Model | Conv. | Turn 1 | Turn 2 | Turn 3 |")
print("|-------|-------|--------|--------|--------|")

multi_results = [r for r in results if r["multi"]]
for r in sorted(multi_results, key=lambda x: x["multi"]["overall"]["strict_accuracy"], reverse=True):
    m = r["multi"]["overall"]
    bt = r["multi"].get("by_turn", {})
    conv = m["strict_accuracy"] * 100
    t1 = bt.get("1", {}).get("accuracy", 0) * 100
    t2 = bt.get("2", {}).get("accuracy", 0) * 100
    t3 = bt.get("3", {}).get("accuracy", 0) * 100
    print(f"| {r['display_name']} | {conv:.1f}% | {t1:.1f}% | {t2:.1f}% | {t3:.1f}% |")
