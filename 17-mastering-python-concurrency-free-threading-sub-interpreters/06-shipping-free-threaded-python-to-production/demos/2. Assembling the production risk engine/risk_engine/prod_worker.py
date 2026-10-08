from .portfolio import demo_portfolio
from .simulate import run_scenarios, summarize


def simulate_job(scenarios: int, seed: int) -> dict[str, float]:
    report = summarize(run_scenarios(demo_portfolio(), scenarios, seed))
    return {
        "var95": round(report["var95"], 2),
        "es95": round(report["es95"], 2),
        "mean": round(report["mean"], 2),
    }
