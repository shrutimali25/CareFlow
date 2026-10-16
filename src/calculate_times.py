
from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent

input_file = (
    project_folder / "data" / "processed" / "sepsis_cleaned.csv"
)
output_file = (
    project_folder / "data" / "processed" / "sepsis_with_times.csv"
)

df = pd.read_csv(input_file)

# Convert timestamps to datetime
df["time:timestamp"] = pd.to_datetime(df["time:timestamp"])

# Sort events within each patient case
df = df.sort_values(
    ["case:concept:name", "time:timestamp"]
).copy()

# Calculate time since the previous event for each case
df["previous_event_time"] = (
    df.groupby("case:concept:name")["time:timestamp"].shift(1)
)

df["elapsed_minutes"] = (
    df["time:timestamp"] - df["previous_event_time"]
).dt.total_seconds() / 60

# Save the result
df.to_csv(output_file, index=False)

print("Total events:", len(df))
print("Unique cases:", df["case:concept:name"].nunique())
print("First events without a previous event:",
      df["elapsed_minutes"].isna().sum())
print("Saved to:", output_file)

print("\nSample results:")
print(
    df[
        [
            "case:concept:name",
            "concept:name",
            "time:timestamp",
            "elapsed_minutes"
        ]
    ].head(10).to_string(index=False)
)
