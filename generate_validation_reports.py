#!/usr/bin/env python3
"""Generate multiple validation reports with different samples."""
import json
import random
from pathlib import Path
from collections import defaultdict

# Models to include
MODELS = [
    "claude-haiku-4.5", "claude-sonnet-4.5", "gemini-3-flash", "gemini-3-pro",
    "gpt-5.2", "gpt-5-mini", "qwen3-14b", "qwen3-235b", "qwen3-32b", "qwen3-8b",
    "sabia-3", "sabia-3.1", "sabia-4", "sabiazinho-3", "sabiazinho-4", "think-gpt-5"
]

def load_all_results():
    """Load all evaluation results."""
    all_results = []
    
    for model in MODELS:
        eval_path = Path(f"runs/{model}/eval/single-turn/eval_results_scored.jsonl")
        if not eval_path.exists():
            continue
        
        with open(eval_path) as f:
            for line in f:
                data = json.loads(line)
                data["_model"] = model
                all_results.append(data)
    
    return all_results

def generate_report(all_results, seed, output_path, samples_per_instruction=2):
    """Generate a validation report with specific seed."""
    random.seed(seed)
    
    # Group by instruction
    by_instruction = defaultdict(lambda: {"pass": [], "fail": []})
    
    for result in all_results:
        instr_ids = result.get("instruction_id_list", [])
        follow_list = result.get("follow_instruction_list", [])
        
        for instr_id, followed in zip(instr_ids, follow_list):
            key = "pass" if followed else "fail"
            by_instruction[instr_id][key].append({
                "model": result["_model"],
                "prompt": result["prompt"],
                "response": result["response"],
                "all_instructions": instr_ids,
                "all_results": follow_list,
                "this_instruction": instr_id,
                "this_result": followed
            })
    
    # Sample from each instruction
    samples = []
    for instr_id in sorted(by_instruction.keys()):
        data = by_instruction[instr_id]
        
        # Sample passes
        if data["pass"]:
            random.shuffle(data["pass"])
            for item in data["pass"][:samples_per_instruction]:
                samples.append(item)
        
        # Sample fails
        if data["fail"]:
            random.shuffle(data["fail"])
            for item in data["fail"][:samples_per_instruction]:
                samples.append(item)
    
    # Write markdown report
    with open(output_path, "w") as f:
        f.write(f"# Manual Validation Dataset (Seed {seed})\n\n")
        f.write(f"Total samples: {len(samples)}\n")
        f.write(f"Instruction types: {len(by_instruction)}\n\n")
        f.write("---\n\n")
        
        current_instr = None
        sample_num = 0
        
        for item in sorted(samples, key=lambda x: (x["this_instruction"], not x["this_result"])):
            if item["this_instruction"] != current_instr:
                current_instr = item["this_instruction"]
                sample_num = 0
                f.write(f"## {current_instr}\n\n")
            
            sample_num += 1
            status = "PASS" if item["this_result"] else "FAIL"
            
            f.write(f"### Sample {sample_num} [{status}] - {item['model']}\n\n")
            f.write("**Prompt:**\n```\n")
            f.write(item["prompt"])
            f.write("\n```\n\n")
            f.write("**Response:**\n```\n")
            f.write(item["response"])
            f.write("\n```\n\n")
            f.write(f"**All instructions:** {item['all_instructions']}\n")
            f.write(f"**All results:** {item['all_results']}\n\n")
            f.write("**Manual verification:** [ ] Agree  [ ] Disagree\n\n")
            f.write("**Notes:**\n\n")
            f.write("---\n\n")
    
    print(f"Generated: {output_path} ({len(samples)} samples)")

def main():
    print("Loading results...")
    all_results = load_all_results()
    print(f"Loaded {len(all_results)} results")
    
    # Generate 3 reports with different seeds
    for i, seed in enumerate([100, 200, 300], 1):
        output_path = f"validation/validation_review_{i}.md"
        generate_report(all_results, seed, output_path)

if __name__ == "__main__":
    main()
