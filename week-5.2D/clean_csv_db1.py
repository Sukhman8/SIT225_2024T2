import pandas as pd

# Load CSV file
df = pd.read_csv("gyroscope_data.csv")

# Check for missing values
print("Missing values before cleaning:")
print(df.isnull().sum())

# Drop rows with any missing or non-numeric values
df_cleaned = df.dropna()

# Save cleaned data
cleaned_filename = "gyroscope_data_cleaned.csv"
df_cleaned.to_csv(cleaned_filename, index=False)

print(f"Cleaned data saved to {cleaned_filename}")
