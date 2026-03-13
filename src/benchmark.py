import time
import pandas as pd

from src.instance import generate_instance
from src.heuristics import clarke_wright_savings
from src.solve_ortools import solve_vrp_ortools

def run_benchmark(
    n_instances: int = 20,
    n_customers: int = 50,
    capacity: int = 40,
    n_vehicles: int = 10,
    ortools_time_limit_sec: int = 2,
    base_seed: int = 0,
) -> pd.DataFrame:
    rows = []
    for k in range(n_instances):
        seed = base_seed + k
        inst = generate_instance(n_customers=n_customers, seed=seed, capacity=capacity)

        t0 = time.time()
        h = clarke_wright_savings(inst)
        t1 = time.time()

        o = solve_vrp_ortools(inst, n_vehicles=n_vehicles, time_limit_sec=ortools_time_limit_sec)

        gap = None
        if o.routes:
            gap = (h.total_distance - o.total_distance) / o.total_distance * 100.0

        rows.append({
            "seed": seed,
            "n_customers": n_customers,
            "capacity": capacity,
            "n_vehicles": n_vehicles,

            "savings_dist": h.total_distance,
            "savings_time_sec": t1 - t0,
            "savings_routes": len(h.routes),

            "ortools_dist": o.total_distance if o.routes else None,
            "ortools_time_sec": o.solve_time_sec,
            "ortools_routes": len(o.routes),

            "gap_pct_savings_vs_ortools": gap,
        })

    return pd.DataFrame(rows)

def main():
    df = run_benchmark()
    df.to_csv("reports/benchmark.csv", index=False)

    print("Saved: reports/benchmark.csv")
    print(df.head())

    if df["gap_pct_savings_vs_ortools"].notna().any():
        print("\nSummary (where OR-Tools solved):")
        print("mean_gap_pct:", df["gap_pct_savings_vs_ortools"].mean())
        print("median_gap_pct:", df["gap_pct_savings_vs_ortools"].median())
        print("mean_savings_time:", df["savings_time_sec"].mean())
        print("mean_ortools_time:", df["ortools_time_sec"].mean())

if __name__ == "__main__":
    main()