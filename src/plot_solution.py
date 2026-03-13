from pathlib import Path
import matplotlib.pyplot as plt

from src.instance import generate_instance
from src.heuristics import clarke_wright_savings
from src.solve_ortools import solve_vrp_ortools

OUTDIR = Path("reports/figures")

def plot_routes(coords, routes, title, filename):
    OUTDIR.mkdir(parents=True, exist_ok=True)
    plt.figure()

    x = coords[:, 0]
    y = coords[:, 1]
    plt.scatter(x[0:1], y[0:1], marker="s", label="depot")  # depot
    plt.scatter(x[1:], y[1:], label="customers")

    for r in routes:
        xs = [coords[i, 0] for i in r]
        ys = [coords[i, 1] for i in r]
        plt.plot(xs, ys)

    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.savefig(OUTDIR / filename, dpi=150)
    plt.close()

def main():
    inst = generate_instance(n_customers=50, seed=0, capacity=40)

    h = clarke_wright_savings(inst)
    o = solve_vrp_ortools(inst, n_vehicles=10, time_limit_sec=2)

    plot_routes(inst.coords, h.routes, f"Savings solution (dist={h.total_distance})", "solution_savings.png")
    plot_routes(inst.coords, o.routes, f"OR-Tools solution (dist={o.total_distance})", "solution_ortools.png")

    print(f"Saved to: {OUTDIR.resolve()}")

if __name__ == "__main__":
    main()