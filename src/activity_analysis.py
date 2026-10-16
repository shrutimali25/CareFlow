
from pathlib import Path
import pandas as pd

base = Path(__file__).resolve().parent.parent

input_file = base / "data" / "processed" / "sepsis_with_times.csv"
output_file = base / "data" / "processed" / "activity_frequency.csv"

df = pd.read_csv(input_file)

activity_summary = (
    df.groupby("concept:name")
    .agg(
        total_occurrences=("concept:name", "count"),
        unique_cases=("case:concept:name", "nunique")
    )
    .reset_index()
    .sort_values("total_occurrences", ascending=False)
)

activity_summary.to_csv(output_file, index=False)

print("Total unique activities:", len(activity_summary))
print("Saved to:", output_file)
print("\nTop 10 most frequent activities:")
print(activity_summary.head(10).to_string(index=False))
