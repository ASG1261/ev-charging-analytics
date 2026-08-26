import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("=" * 60)
print("EV CHARGING DATA ANALYSIS")
print("=" * 60)

# Load cleaned data
df = pd.read_csv('../data/processed/cleaned_data.csv')

# Convert date columns
df['Charging Start Time'] = pd.to_datetime(df['Charging Start Time'])
df['Charging End Time'] = pd.to_datetime(df['Charging End Time'])

# Create time features
df['Hour'] = df['Charging Start Time'].dt.hour
df['Month'] = df['Charging Start Time'].dt.month
df['Day of Week Num'] = df['Charging Start Time'].dt.dayofweek
df['Is Weekend'] = df['Day of Week Num'].isin([5, 6])

# 1. KEY PERFORMANCE INDICATORS (KPIs)
print("\n" + "=" * 60)
print("KEY PERFORMANCE INDICATORS")
print("=" * 60)

total_sessions = len(df)
total_energy = df['Energy Consumed (kWh)'].sum()
total_revenue = df['Charging Cost (USD)'].sum()
avg_duration = df['Charging Duration (hours)'].mean()
avg_energy = df['Energy Consumed (kWh)'].mean()
avg_cost = df['Charging Cost (USD)'].mean()

print(f"Total Sessions:          {total_sessions:,}")
print(f"Total Energy:            {total_energy:,.1f} kWh")
print(f"Total Revenue:           ${total_revenue:,.2f}")
print(f"Average Duration:        {avg_duration:.2f} hours")
print(f"Average Energy/Session:  {avg_energy:.1f} kWh")
print(f"Average Cost/Session:    ${avg_cost:.2f}")

# 2. CHARGER TYPE ANALYSIS
print("\n" + "=" * 60)
print("CHARGER TYPE PERFORMANCE")
print("=" * 60)

charger_stats = df.groupby('Charger Type').agg({
    'Charging Station ID': 'count',
    'Energy Consumed (kWh)': 'sum',
    'Charging Cost (USD)': 'sum',
    'Charging Duration (hours)': 'mean'
}).round(2)

charger_stats.columns = ['Sessions', 'Total Energy (kWh)', 'Total Revenue ($)', 'Avg Duration (hrs)']
print(charger_stats.sort_values('Total Revenue ($)', ascending=False))


# 3. TIME-BASED ANALYSIS
print("\n" + "=" * 60)
print("PEAK HOURS (Top 5)")
print("=" * 60)

hourly = df.groupby('Hour').agg({
    'Charging Station ID': 'count',
    'Charging Cost (USD)': 'sum'
}).round(2)

hourly.columns = ['Sessions', 'Revenue ($)']
print(hourly.nlargest(5, 'Sessions'))


# 4. USER TYPE ANALYSIS
print("\n" + "=" * 60)
print("USER TYPE DISTRIBUTION")
print("=" * 60)

user_stats = df['User Type'].value_counts()
print(user_stats)


# 5. CREATE VISUALIZATIONS
print("\n" + "=" * 60)
print("GENERATING VISUALIZATIONS...")
print("=" * 60)

# Create images folder if not exists
os.makedirs('../images', exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create subplots
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('EV Charging Analytics Dashboard', fontsize=20, fontweight='bold')

# 1. Sessions by Hour
hour_counts = df['Hour'].value_counts().sort_index()
axes[0, 0].bar(hour_counts.index, hour_counts.values, color='skyblue', edgecolor='black')
axes[0, 0].set_title('Charging Sessions by Hour', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Hour of Day')
axes[0, 0].set_ylabel('Number of Sessions')
axes[0, 0].axvline(x=18, color='red', linestyle='--', alpha=0.7, label='Peak Start (6 PM)')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. Revenue by Charger Type
charger_revenue = df.groupby('Charger Type')['Charging Cost (USD)'].sum().sort_values()
axes[0, 1].barh(charger_revenue.index, charger_revenue.values, color='lightgreen', edgecolor='black')
axes[0, 1].set_title('Revenue by Charger Type', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Revenue ($)')
for i, v in enumerate(charger_revenue.values):
    axes[0, 1].text(v, i, f' ${v:,.0f}', va='center')

# 3. User Type Distribution
user_counts = df['User Type'].value_counts()
axes[0, 2].pie(user_counts.values, labels=user_counts.index, autopct='%1.1f%%')
axes[0, 2].set_title('User Type Distribution', fontsize=12, fontweight='bold')

# 4. Energy by Charger Type
charger_energy = df.groupby('Charger Type')['Energy Consumed (kWh)'].mean()
axes[1, 0].bar(charger_energy.index, charger_energy.values, color='coral', edgecolor='black')
axes[1, 0].set_title('Average Energy by Charger Type', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Charger Type')
axes[1, 0].set_ylabel('Avg Energy (kWh)')
axes[1, 0].tick_params(axis='x', rotation=15)

# 5. Duration Distribution
axes[1, 1].hist(df['Charging Duration (hours)'], bins=20, color='purple', alpha=0.7, edgecolor='black')
axes[1, 1].set_title('Charging Duration Distribution', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Duration (hours)')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].axvline(x=df['Charging Duration (hours)'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {df["Charging Duration (hours)"].mean():.1f}h')
axes[1, 1].legend()

# 6. Weekend vs Weekday
weekend_data = df.groupby('Is Weekend')['Charging Station ID'].count()
labels = ['Weekday', 'Weekend']
axes[1, 2].bar(labels, weekend_data.values, color=['#3498db', '#e74c3c'])
axes[1, 2].set_title('Weekday vs Weekend Usage', fontsize=12, fontweight='bold')
axes[1, 2].set_ylabel('Number of Sessions')
for i, v in enumerate(weekend_data.values):
    axes[1, 2].text(i, v + 5, f'{v:,}', ha='center')

plt.tight_layout()
plt.savefig('../images/analysis_dashboard.png', dpi=300, bbox_inches='tight')
print("Visualization saved to: images/analysis_dashboard.png")

# Show the plot
plt.show()


# 6. BUSINESS INSIGHTS
print("\n" + "=" * 60)
print("BUSINESS INSIGHTS")
print("=" * 60)

# Most profitable charger
top_charger = df.groupby('Charger Type')['Charging Cost (USD)'].sum().idxmax()
print(f"Most Profitable Charger Type: {top_charger}")

# Most common user
top_user = df['User Type'].value_counts().idxmax()
print(f"Most Common User Type: {top_user}")

# Peak hour
peak_hour = df['Hour'].value_counts().idxmax()
print(f"Peak Charging Hour: {peak_hour}:00 - {peak_hour+1}:00")

# Average revenue per session
avg_revenue = df['Charging Cost (USD)'].mean()
print(f"Average Revenue per Session: ${avg_revenue:.2f}")

# Fast charger usage
fast_charger = df[df['Charger Type'] == 'DC Fast Charger']
fast_pct = (len(fast_charger) / len(df)) * 100
print(f"Fast Charger Usage: {fast_pct:.1f}% of all sessions")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)