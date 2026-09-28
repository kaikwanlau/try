"""
paths.py -- where the data of this project are.

Every script in the numbered folders imports this file. That is what lets each script
run from its own folder (press Run in PyCharm, or `python script.py` inside the folder)
while the meshes stay in one place, data/, and are never copied.

To move or rename a data folder, change it here only.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent            # the project folder (the folder of this file)
DATA = ROOT / "data"

# The five groups of skull meshes
FINCHES = DATA / "DF_and_their_relatives"         # 100 Darwin's finches and their relatives
HONEYCREEPERS = DATA / "Honeycreepers_watertight"  # 42 Hawaiian honeycreepers (SI Section S4)
CARDUELINES = DATA / "HC_Relatives_watertight"    # 9 cardueline relatives of the honeycreepers
PEROMYSCUS = DATA / "Peromyscus"                  # 2 rodent skulls
HUMAN = DATA / "Human_cranium"                    # 4 human crania

# The released data tables
DATASET = DATA / "Dataset.xlsx"                   # all measurements of the 100 finch specimens
DATASET_TRAINING = DATA / "Dataset_training.xlsx"  # the 50 training specimens of Eq. (8)
DATASET_OTHER_TAXA = DATA / "Dataset_other_taxa.xlsx"  # per-specimen values of SI Section S4

# Inputs used only by 5_figures/figure.py (the photograph and the meshes shown in Figs 1 and S1)
FIGURE_INPUTS = DATA / "figure_inputs"


def output_dir(script_file):
    """The folder a script writes into: output/<script name>/ next to the script (created if needed)."""
    script = Path(script_file).resolve()
    out = script.parent / "output" / script.stem
    out.mkdir(parents=True, exist_ok=True)
    return out
