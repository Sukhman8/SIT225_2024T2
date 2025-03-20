import pandas as pd

# Load the CSV
df = pd.read_csv("gyroscope_data_db2.csv")

# Remove rows with NaN (empty) values
df = df.dropna()

# Ensure x, y, z are numeric
df = df[pd.to_numeric(df["x"], errors="coerce").notnull()]
df = df[pd.to_numeric(df["y"], errors="coerce").notnull()]
df = df[pd.to_numeric(df["z"], errors="coerce").notnull()]

# Save cleaned data
df.to_csv("gyroscope_data_db2_cleaned.csv", index=False)
print("✅ Cleaned CSV Saved: gyroscope_data_db2_cleaned.csv")
