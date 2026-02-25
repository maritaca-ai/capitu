"""Upload CAPITU benchmark metrics to W&B.

Reads metrics_report.json files produced by run_eval.py
(single-turn and multi-turn) and creates a W&B run so that
consolidate_wandb_metrics.py can discover and aggregate the results.

Usage:
    python3 upload_to_wandb.py \
        --run_id sabiazinho-4 \
        --wandb_project your-wandb-project \
        --wandb_entity your-wandb-entity
"""

import json
import os
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

import wandb


def load_metrics(path):
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return json.load(f)


def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--run_id", required=True, help="Model run ID (e.g. sabiazinho-4)")
    parser.add_argument("--wandb_project", default="your-wandb-project")
    parser.add_argument("--wandb_entity", default="your-wandb-entity")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "runs", args.run_id)
    st_path = os.path.join(output_dir, "eval", "single-turn", "metrics_report.json")
    mt_path = os.path.join(output_dir, "eval", "multi-turn", "metrics_report.json")

    st = load_metrics(st_path)
    mt = load_metrics(mt_path)

    if st is None and mt is None:
        print(f"No metrics found for run_id={args.run_id} in {output_dir}")
        return

    metrics = {}

    if st is not None:
        metrics["strict_accuracy"] = st["overall"]["strict_accuracy"]
        metrics["loose_accuracy"] = st["overall"]["loose_accuracy"]
        metrics["instruction_level_accuracy"] = st["overall"]["instruction_level_accuracy"]
        if st.get("coherence", {}).get("avg_coherence", 0) > 0:
            metrics["coherence"] = st["coherence"]["avg_coherence"]
        if st["overall"].get("final_score", 0) > 0:
            metrics["final_score"] = st["overall"]["final_score"]
        # Per-difficulty
        for diff in ["easy", "medium", "hard"]:
            if diff in st.get("by_difficulty", {}):
                metrics[f"difficulty/{diff}/strict_accuracy"] = st["by_difficulty"][diff]["strict_accuracy"]

    if mt is not None:
        metrics["multi_turn/conversation_accuracy"] = mt["overall"]["strict_accuracy"]
        metrics["multi_turn/instruction_level_accuracy"] = mt["overall"]["instruction_level_accuracy"]
        # Per-turn
        for turn_key, turn_data in mt.get("by_turn", {}).items():
            metrics[f"multi_turn/{turn_key}/strict_accuracy"] = turn_data["strict_accuracy"]

    if not metrics:
        print("No valid metrics extracted.")
        return

    wandb_run_name = f"{args.run_id}_capitu"

    with wandb.init(
        entity=args.wandb_entity,
        project=args.wandb_project,
        name=wandb_run_name,
        config={"model": args.run_id, "benchmark": "capitu"},
    ) as run:
        run.summary.update(metrics)
        print(f"Uploaded {len(metrics)} metrics to W&B run: {wandb_run_name}")
        for k, v in sorted(metrics.items()):
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
