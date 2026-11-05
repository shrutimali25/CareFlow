from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data" / "processed"
POWERBI = ROOT / "data" / "powerbi"

POWERBI.mkdir(parents=True, exist_ok=True)

files = [
    "patient_case_summary.csv",
    "activity_frequency.csv",
    "activity_time_differences.csv"
]

for filename in files:
    source = DATA / filename

    if not source.exists():
        print(f"File not found: {filename}")
        continue

    df = pd.read_csv(source)

    output = POWERBI / filename
    df.to_csv(output, index=False)

    print(f"Prepared: {output.name}")

print("\nPower BI data preparation completed!")