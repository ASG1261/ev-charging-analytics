import pandas as pd
import os

print("=" * 50)
print("🚀 STARTING DATA CLEANING")
print("=" * 50)

# Load the data
file_path = '../data/raw/ev_charging_patterns.csv'
df = pd.read_csv(file_path)

print(f"✅ Loaded {len(df)} records")
print(f"📋 Columns: {df.columns.tolist()}")

# Save cleaned version
output_path = '../data/processed/cleaned_data.csv'
df.to_csv(output_path, index=False)

print(f"✅ Saved to: {output_path}")
print("🎉 DONE!")