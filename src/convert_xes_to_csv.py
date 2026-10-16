
from pathlib import Path
import pm4py

project_folder = Path(__file__).resolve().parent.parent

input_file = project_folder / "data" / "raw" / "sepsis.xes.gz"
output_folder = project_folder / "data" / "processed"
output_file = output_folder / "sepsis_event_log.csv"

output_folder.mkdir(parents=True, exist_ok=True)

log = pm4py.read_xes(str(input_file))
df = pm4py.convert_to_dataframe(log)

df.to_csv(output_file, index=False)

print("Dataset converted successfully!")
print("Rows and columns:", df.shape)
print("Columns:", df.columns.tolist())
print("Saved to:", output_file)
