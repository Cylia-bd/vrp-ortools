from src.benchmark import main as benchmark_main
from src.plot_benchmark import main as plot_bench_main
from src.plot_solution import main as plot_solution_main

def main():
    print("== Benchmark ==")
    benchmark_main()
    print("\n== Benchmark plots ==")
    plot_bench_main()
    print("\n== Solution plots ==")
    plot_solution_main()

if __name__ == "__main__":
    main()