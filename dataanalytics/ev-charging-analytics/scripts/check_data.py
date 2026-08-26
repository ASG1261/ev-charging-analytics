import pandas as pd

# Load the cleaned data
df = pd.read_csv('../data/processed/cleaned_data.csv')

print("=" * 50)
print("📊 CLEANED DATA PREVIEW")
print("=" * 50)

print(f"Total Records: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")
print("\nColumn Names:")
for col in df.columns:
    print(f"  - {col}")

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)