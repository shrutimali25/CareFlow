
from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent

input_file = project_folder / "data" / "processed" / "sepsis_event_log.csv"
output_file = project_folder / "data" / "processed" / "sepsis_cleaned.csv"

df = pd.read_csv(input_file)

print("Original rows:", len(df))

# Remove rows without a case ID
df = df.dropna(subset=["case:concept:name"]).copy()

# Remove exact duplicate rows
df = df.drop_duplicates().copy()

# Convert timestamps into datetime format
df["time:timestamp"] = pd.to_datetime(
    df["time:timestamp"], errors="coerce"
)

# Remove rows with invalid timestamps
df = df.dropna(subset=["time:timestamp"]).copy()

# Sort events by case and timestamp
df = df.sort_values(
    ["case:concept:name", "time:timestamp"]
).reset_index(drop=True)

df.to_csv(output_file, index=False)

print("Cleaned rows:", len(df))
print("Unique cases:", df["case:concept:name"].nunique())
print("Remaining duplicate rows:", df.duplicated().sum())
print("Missing case IDs:", df["case:concept:name"].isna().sum())
print("Missing timestamps:", df["time:timestamp"].isna().sum())
print("Saved to:", output_file)
