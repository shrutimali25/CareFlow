from pathlib import Path
import pandas as pd

base = Path(__file__).resolve().parent.parent

input_file = base / "data" / "processed" / "sepsis_with_times.csv"
output_file = base / "data" / "processed" / "activity_time_differences.csv"

df = pd.read_csv(input_file)

df["time:timestamp"] = pd.to_datetime(
    df["time:timestamp"], utc=True
)

df = df.sort_values(
    ["case:concept:name", "time:timestamp"]
).copy()

df["previous_activity"] = (
    df.groupby("case:concept:name")["concept:name"].shift(1)
)

df["time_difference_minutes"] = df["elapsed_minutes"]

time_summary = (
    df.dropna(subset=["previous_activity"])
    .groupby(["previous_activity", "concept:name"])
    .agg(
        total_transitions=("time_difference_minutes", "count"),
        average_minutes=("time_difference_minutes", "mean"),
        median_minutes=("time_difference_minutes", "median")
    )
    .reset_index()
    .sort_values("total_transitions", ascending=False)
)

time_summary.to_csv(output_file, index=False)

print("Total activity transitions:", len(time_summary))
print("Saved to:", output_file)
print("\nTop 10 activity transitions:")
print(time_summary.head(10).to_string(index=False))