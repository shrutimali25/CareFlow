
from pathlib import Path
import pandas as pd

base = Path(__file__).resolve().parent.parent

input_file = base / "data" / "processed" / "sepsis_with_times.csv"
output_file = base / "data" / "processed" / "patient_case_summary.csv"

df = pd.read_csv(input_file)

df["time:timestamp"] = pd.to_datetime(
    df["time:timestamp"], utc=True
)

summary = df.groupby("case:concept:name").agg(
    total_events=("concept:name", "count"),
    first_event_time=("time:timestamp", "min"),
    last_event_time=("time:timestamp", "max")
).reset_index()

summary["treatment_duration_hours"] = (
    summary["last_event_time"] - summary["first_event_time"]
).dt.total_seconds() / 3600

summary.to_csv(output_file, index=False)

print("Total patient cases:", len(summary))
print("Average events per case:", round(summary["total_events"].mean(), 2))
print("Average duration (hours):", round(summary["treatment_duration_hours"].mean(), 2))
print("Saved to:", output_file)
print("\nSample results:")
print(summary.head().to_string(index=False))
