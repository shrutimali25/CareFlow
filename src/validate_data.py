from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent
input_file = project_folder / "data" / "processed" / "sepsis_with_times.csv"

if not input_file.exists():
    raise FileNotFoundError(f"Dataset not found: {input_file}")

df = pd.read_csv(input_file)

report = {
    "Total rows": len(df),
    "Total columns": len(df.columns),
    "Unique patient cases": df["case:concept:name"].nunique(),
    "Missing case IDs": df["case:concept:name"].isna().sum(),
    "Missing activities": df["concept:name"].isna().sum(),
    "Missing timestamps": df["time:timestamp"].isna().sum(),
    "Duplicate rows": df.duplicated().sum(),
    "Negative elapsed times": (df["elapsed_minutes"] < 0).sum(),
}

report_folder = project_folder / "reports"
report_folder.mkdir(parents=True, exist_ok=True)

report_df = pd.DataFrame(list(report.items()), columns=["Metric", "Value"])
output_file = report_folder / "data_quality_report.csv"
report_df.to_csv(output_file, index=False)

print(report_df.to_string(index=False))
print(f"\nReport saved to: {output_file}")