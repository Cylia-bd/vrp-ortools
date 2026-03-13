from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

OUTDIR = Path("reports/figures")

def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv("reports/benchmark.csv")

    # 1) Histogram gap
    g = df["gap_pct_savings_vs_ortools"].dropna()
    plt.figure()
    plt.hist(g, bins=12)
    plt.title("Gap%: Savings vs OR-Tools (lower is better for Savings)")
    plt.xlabel("gap % = (Savings - ORTools) / ORTools * 100")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(OUTDIR / "gap_hist.png", dpi=150)
    plt.close()

    # 2) Time comparison
    plt.figure()
    plt.scatter(df["ortools_time_sec"], df["savings_time_sec"])
    plt.title("Runtime comparison")
    plt.xlabel("OR-Tools time (sec)")
    plt.ylabel("Savings time (sec)")
    plt.tight_layout()
    plt.savefig(OUTDIR / "runtime_scatter.png", dpi=150)
    plt.close()

    print(f"Saved figures to: {OUTDIR.resolve()}")

if __name__ == "__main__":
    main()