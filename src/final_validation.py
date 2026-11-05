from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "processed" / "sepsis_with_times.csv"
REPORT_FOLDER = ROOT / "reports"

REPORT_FOLDER.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_FILE)

# Identify required columns
def find_column(possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

case_col = find_column(["Case_ID", "case:concept:name"])
activity_col = find_column(["Activity", "concept:name"])
time_col = find_column(["Timestamp", "time:timestamp"])
elapsed_col = find_column(["elapsed_minutes"])

# Basic validation
results = []

def add_result(check, value, status):
    results.append({
        "Validation_Check": check,
        "Result": value,
        "Status": status
    })

add_result("Total Events", len(df), "INFO")

if case_col:
    add_result(
        "Unique Cases",
        df[case_col].nunique(),
        "PASS"
    )
else:
    add_result("Case ID Column", "Not found", "FAIL")

if activity_col:
    add_result(
        "Unique Activities",
        df[activity_col].nunique(),
        "PASS"
    )
else:
    add_result("Activity Column", "Not found", "FAIL")

# Missing values
for col in [case_col, activity_col, time_col]:
    if col:
        missing = int(df[col].isna().sum())
        add_result(
            f"Missing values in {col}",
            missing,
            "PASS" if missing == 0 else "FAIL"
        )

# Duplicate records
if case_col and activity_col and time_col:
    duplicate_count = int(
        df.duplicated(subset=[case_col, activity_col, time_col]).sum()
    )

    add_result(
        "Duplicate event combinations",
        duplicate_count,
        "CHECK" if duplicate_count > 0 else "PASS"
    )

# Timestamp validation
if time_col:
    timestamps = pd.to_datetime(df[time_col], errors="coerce", utc=True)
    invalid = int(timestamps.isna().sum())

    add_result(
        "Invalid timestamps",
        invalid,
        "PASS" if invalid == 0 else "FAIL"
    )

# Negative elapsed time validation
if elapsed_col:
    elapsed = pd.to_numeric(df[elapsed_col], errors="coerce")
    negative = int((elapsed < 0).sum())

    add_result(
        "Negative elapsed times",
        negative,
        "PASS" if negative == 0 else "FAIL"
    )
else:
    add_result(
        "Elapsed time column",
        "Not found",
        "CHECK"
    )

# Save report
report = pd.DataFrame(results)

report.to_csv(
    REPORT_FOLDER / "final_data_validation_report.csv",
    index=False
)

print("\nFINAL DATA VALIDATION")
print(report.to_string(index=False))

print("\nReport saved successfully!")