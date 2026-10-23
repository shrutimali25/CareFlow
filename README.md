\# CareFlow – Clinical Pathway Process Mining



\## Project Overview

CareFlow analyzes timestamped hospital event logs to summarize patient activity sequences, case durations, activity frequencies, and time between consecutive activities.



\## Technology Stack

\- Python

\- Pandas

\- PM4Py

\- CSV

\- Git and GitHub



\## Member 1 Responsibilities



\### 1. Synthetic Data Generation

Generated sample hospital event data containing case IDs, activities, and timestamps.



\### 2. Data Cleaning

Cleaned event data and checked duplicate records and missing values.



\### 3. Data Validation

Validated required columns, missing values, duplicate records, chronological ordering, and negative elapsed times.



\### 4. Time Calculation

Calculated elapsed minutes between consecutive activities for each patient case.



\### 5. Case Summary

Generated patient case summaries containing event counts, first and last event timestamps, and duration in hours.



\### 6. Activity Frequency Analysis

Calculated activity occurrence counts and the number of unique cases for each activity.



\### 7. Activity Transition Analysis

Calculated transition counts, average elapsed minutes, and median elapsed minutes between consecutive activities.



\## Main Output Files

\- `sepsis\_cleaned.csv`

\- `sepsis\_with\_times.csv`

\- `patient\_case\_summary.csv`

\- `activity\_frequency.csv`

\- `activity\_time\_differences.csv`

\- `data\_quality\_report.csv`



\## Validation Results

Latest validation run:

\- Total rows: 15,189

\- Total columns: 34

\- Unique cases: 1,049

\- Missing case IDs: 0

\- Missing activities: 0

\- Missing timestamps: 0

\- Duplicate rows: 0

\- Cases reported out of chronological order: 0

\- Negative elapsed times: 0



\## Limitations

These results describe the available event log. They do not independently prove the causes of hospital delays or improvements in patient outcomes.



\## Future Scope

\- Visualize patient pathways.

\- Identify potential process bottlenecks.

\- Create interactive dashboards.

\- Integrate outputs with the overall team project.

