

from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent
input_file = (
    project_folder / "data" / "processed" / "sepsis_with_times.csv"
)

df = pd.read_csv(input_file)

print("Total rows:", len(df))
print("Total columns:", len(df.columns))
print("Unique patient cases:", df["case:concept:name"].nunique())
print("Missing case IDs:", df["case:concept:name"].isna().sum())
print("Missing activities:", df["concept:name"].isna().sum())
print("Missing timestamps:", df["time:timestamp"].isna().sum())
print("Duplicate rows:", df.duplicated().sum())

print("\nElapsed time statistics (minutes):")
print(df["elapsed_minutes"].describe())

print("\nNegative elapsed times:", (df["elapsed_minutes"] < 0).sum())
print("Saved dataset exists:", input_file.exists())
