from pathlib import Path

# Root of the project (one level up from this file)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "src" / "globomantics_platform" / "data" / "samples"
CUSTOMERS_CSV = DATA_DIR / "customers_sample.csv"
