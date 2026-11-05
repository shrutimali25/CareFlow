from pathlib import Path
import pandas as pd
import pm4py

# Project paths
ROOT = Path(__file__).resolve().parents[1]

XES_FILE = ROOT / "data" / "raw" / "sepsis.xes.gz"
CSV_FILE = ROOT / "data" / "processed" / "sepsis_with_times.csv"

OUTPUT = ROOT / "reports"
OUTPUT.mkdir(exist_ok=True)

# Read original XES file
print("Reading original XES file...")
event_log = pm4py.read_xes(str(XES_FILE))
xes_df = pm4py.convert_to_dataframe(event_log)

# Read processed CSV
print("Reading processed CSV file...")
csv_df = pd.read_csv(CSV_FILE)

# Detect column names
def find_column(df, possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    raise ValueError(f"Could not find any of these columns: {possible_names}")

xes_case = find_column(xes_df, ["case:concept:name", "Case_ID"])
xes_activity = find_column(xes_df, ["concept:name", "Activity"])
xes_time = find_column(xes_df, ["time:timestamp", "Timestamp"])

csv_case = find_column(csv_df, ["case:concept:name", "Case_ID"])
csv_activity = find_column(csv_df, ["concept:name", "Activity"])
csv_time = find_column(csv_df, ["time:timestamp", "Timestamp"])

# Create standard comparison tables
def prepare_data(df, case_col, activity_col, time_col):
    result = pd.DataFrame({
        "case_id": df[case_col].astype(str).str.strip(),
        "activity": df[activity_col].astype(str).str.strip(),
        "timestamp": pd.to_datetime(df[time_col], errors="coerce", utc=True)
    })

    return result.dropna(subset=["timestamp"])

xes = prepare_data(xes_df, xes_case, xes_activity, xes_time)
csv = prepare_data(csv_df, csv_case, csv_activity, csv_time)

# Count repeated event combinations correctly
keys = ["case_id", "activity", "timestamp"]

xes_counts = xes.groupby(keys).size().reset_index(name="xes_count")
csv_counts = csv.groupby(keys).size().reset_index(name="csv_count")

comparison = xes_counts.merge(csv_counts, on=keys, how="outer").fillna(0)

comparison["xes_count"] = comparison["xes_count"].astype(int)
comparison["csv_count"] = comparison["csv_count"].astype(int)

# Events missing from CSV
missing = comparison[
    comparison["xes_count"] > comparison["csv_count"]
].copy()

missing["difference"] = missing["xes_count"] - missing["csv_count"]

# Events present in CSV but not in XES
extra = comparison[
    comparison["csv_count"] > comparison["xes_count"]
].copy()

extra["difference"] = extra["csv_count"] - extra["xes_count"]

# Save reports
missing.to_csv(OUTPUT / "events_missing_from_csv.csv", index=False)
extra.to_csv(OUTPUT / "extra_events_in_csv.csv", index=False)

summary = pd.DataFrame({
    "Metric": [
        "XES total events",
        "CSV total events",
        "XES unique cases",
        "CSV unique cases",
        "XES unique activities",
        "CSV unique activities",
        "Different event combinations",
        "Missing event occurrences",
        "Extra event occurrences"
    ],
    "Value": [
        len(xes),
        len(csv),
        xes["case_id"].nunique(),
        csv["case_id"].nunique(),
        xes["activity"].nunique(),
        csv["activity"].nunique(),
        len(missing) + len(extra),
        missing["difference"].sum(),
        extra["difference"].sum()
    ]
})

summary.to_csv(OUTPUT / "reconciliation_summary.csv", index=False)

print("\nReconciliation completed!")
print(summary.to_string(index=False))
print("\nReports saved in the reports folder.")