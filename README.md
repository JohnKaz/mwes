## mwes

A small set of tools for modifying and evaluating conllu files containing Multi-word Expression (MWE) annotations.

### move_mwes.py

Copies MWE type information from the MISC (10th) collumn to either the XPOS (5th) or DEPREL (8th) collumn.

Examples of usage:

(move info to XPOS collumn)
with open("input.conllu") as file:
    move_mwes(file, "output.conllu", "xpos")

(move info to DEPREL collumn)
with open("input.conllu") as file:
    move_mwes(file, "output.conllu", "deprel")

### evaluate_mwes.py

Calculates three metrics for a given conllu file containing predicted mwe annotations: Per-token recall, Per-token precision and Per-VMWE recall.

Example of usage (for file containing predictions in the XPOS collumn:

with open("predictions.conllu", "r", encoding="utf-8") as file:
    evaluate_mwes(file, "xpos")
