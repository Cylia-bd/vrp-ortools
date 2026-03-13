# VRP (Capacitated) — OR-Tools vs Clarke & Wright Savings

Projet RO (Vehicle Routing Problem avec capacité) :
- Génération d'instances VRP (dépôt + clients + demandes)
- Heuristique **Clarke & Wright Savings**
- Solveur **Google OR-Tools (Routing)**
- Benchmark multi-instances : qualité (distance) vs temps
- Visualisation des tournées

---

## Installation

```bash
python -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

---

## Reproduire

**1) Lancer le benchmark (CSV)**
```bash
./.venv/bin/python -m src.benchmark
```
Sortie : `reports/benchmark.csv`

**2) Générer les figures benchmark**
```bash
./.venv/bin/python -m src.plot_benchmark
```
Sorties :
- `reports/figures/gap_hist.png`
- `reports/figures/runtime_scatter.png`

**3) Visualiser une solution (1 instance)**
```bash
./.venv/bin/python -m src.plot_solution
```
Sorties :
- `reports/figures/solution_savings.png`
- `reports/figures/solution_ortools.png`

---

## Structure

```
src/
├── instance.py        # génération instance + matrice distances
├── solve_ortools.py   # solveur OR-Tools (VRP capacité)
├── heuristics.py      # Clarke & Wright Savings
├── benchmark.py       # benchmark multi-instances -> CSV
├── plot_benchmark.py  # figures (gap + temps)
└── plot_solution.py   # visualisation routes (Savings vs OR-Tools)
reports/
├── benchmark.csv
└── figures/
```

---

## Notes

- OR-Tools est exécuté avec un time limit (par défaut 2s), donc la solution n'est pas forcément optimale.
- Le benchmark compare la distance totale des tournées et le temps de calcul.