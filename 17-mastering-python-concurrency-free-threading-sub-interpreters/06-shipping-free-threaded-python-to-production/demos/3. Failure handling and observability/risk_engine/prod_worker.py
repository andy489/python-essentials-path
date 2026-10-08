import math
import time
from .portfolio import demo_portfolio
from .simulate import run_scenarios, summarize

HANG_SECONDS = 6.0

def inject_fault(fault: str, seed: int) -> None:
    if fault == "crash":
        raise ValueError(f"injected crash (seed={seed})")
    if fault == "hang":
        deadline = time.perf_counter() + HANG_SECONDS
        spin = 0.0
        while time.perf_counter() < deadline:
            spin = math.sqrt(spin + 1.0)

def simulate_job(scenarios: int, seed: int, fault: str = "") -> dict[str, float]:
    inject_fault(fault, seed)
    report = summarize(run_scenarios(demo_portfolio(), scenarios, seed))
    return {
        "var95": round(report["var95"], 2),
        "es95": round(report["es95"], 2),
        "mean": round(report["mean"], 2),
    }
