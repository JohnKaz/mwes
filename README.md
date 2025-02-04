# mwes

A small set of tools for modifying and evaluating conllu files containing Multi-word Expression (MWE) annotations.

## move_mwes.py

Copies MWE type information from `field_in` (here: "misc", "xpos" or "deprel") to `field_out` (here: "xpos" or "deprel").
For moves between the "xpos" and "deprel" collumns the parameter `keep` can be set to `True` in order to preserve mwe info in both collumns.

Examples of usage:

(move mwe info from "misc" to "xpos")
```
with open("input.conllu") as file:
    move_mwes(file, "output.conllu", "misc", "xpos")
```

(copy mwe info from "xpos" to "deprel")
```
with open("input.conllu") as file:
    move_mwes(file, "output.conllu", "xpos", "deprel", keep=True)
```

## evaluate_mwes.py

Calculates three metrics for a given conllu file containing predicted mwe annotations: Per-token recall, Per-token precision and Per-VMWE recall.

Example of usage (for file containing predictions in the XPOS collumn):

```
with open("predictions.conllu", "r", encoding="utf-8") as file:
    evaluate_mwes(file, "xpos")
```
