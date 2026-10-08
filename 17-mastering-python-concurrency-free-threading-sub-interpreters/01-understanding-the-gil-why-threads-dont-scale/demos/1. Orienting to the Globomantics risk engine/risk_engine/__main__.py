import argparse
import time

from .parallel import run_threads
from .portfolio import demo_portfolio
from .simulate import run_scenarios, summarize


def main() -> None:
    parser = argparse.ArgumentParser(prog="risk_engine")
    parser.add_argument("--mode", choices=["single", "threads"], default="single")
    parser.add_argument("--scenarios", type=int, default=40_000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    positions = demo_portfolio()
    start = time.perf_counter()
    if args.mode == "single":
        pnls = run_scenarios(positions, args.scenarios, args.seed)
    else:
        pnls = run_threads(positions, args.scenarios, args.workers, args.seed)
    wall = time.perf_counter() - start

    report = summarize(pnls)
    print(f"mode={args.mode} scenarios={args.scenarios} "
          f"workers={args.workers} seed={args.seed}")
    print(f"var95={report['var95']:,.2f} es95={report['es95']:,.2f} "
          f"mean={report['mean']:,.2f}")
    print(f"wall={wall:.2f}s")


if __name__ == "__main__":
    main()
