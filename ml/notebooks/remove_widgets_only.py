import json

nb_path = "FinBERT_MultiTask.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Remove widget metadata (root cause)
nb["metadata"].pop("widgets", None)

# Remove widget output types ONLY
for cell in nb.get("cells", []):
    if cell.get("cell_type") == "code":
        outputs = cell.get("outputs", [])
        cell["outputs"] = [
            out for out in outputs
            if not (
                out.get("output_type") == "display_data"
                and "application/vnd.jupyter.widget-view+json" in out.get("data", {})
            )
        ]

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("✅ Widget metadata removed, normal outputs preserved")