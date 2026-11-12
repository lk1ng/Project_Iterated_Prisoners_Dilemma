# Prisoner's Dilemma Evolution

This project studies how populations of five-bit strategies evolve in an iterated Prisoner's Dilemma under three action-noise levels (0, 0.01, and 0.05). The notebook estimates payoff and cooperation matrices, runs evolutionary simulations, saves run data, plots the results, and performs statistical comparisons.

## Project files

- `prisoners_dilemma.ipynb` — main simulation and analysis notebook.
- `matchups.py` — game and matchup functions used by the notebook, including its parallel matrix calculation.
- `evolution_results/generation_data.csv` and `evolution_results/run_metadata.csv` — saved simulation results used to restore results for analysis.
- `requirements.txt` — Python dependencies.

## Set up and run

Run these commands from this directory (`Project_Prisoner_Dilemma`):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name prisoners-dilemma --display-name "Python (Prisoner's Dilemma)"
jupyter lab prisoners_dilemma.ipynb
```
Once these steps are performed and the notebook is open, simply run all cells. 

A full run computes matchup matrices for 32 strategies at three noise levels, using 20 independent matches per ordered pair, then evolves 50 populations per noise level for 500 generations. These simulation cells can take a while. They save or overwrite the two CSV files in `evolution_results/`.

## Use the saved results without rerunning the simulation

The repository includes the generated CSV files. To explore their plots and statistical analysis without recalculating the matrices or rerunning evolution, execute the notebook's import, strategy, and configuration setup cells, skip the matrix calculation and evolution/save cells, then run **Reconstruct results from CSV** and the following visualisation and statistical analysis cells.
