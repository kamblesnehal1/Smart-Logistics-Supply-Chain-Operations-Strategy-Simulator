
# SMART LOGISTICS SUPPLY CHAIN ANALYTICS


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


# 1. LOAD DATASET


file_path = "smart_logistics_dataset.csv"

df = pd.read_csv(file_path)

print("Dataset Loaded Successfully\n")


# 2. BASIC DATA INSPECTION


print("First 5 Rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())


# 3. DATA CLEANING


# Remove duplicates
df = df.drop_duplicates()

# Convert timestamp column
df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)

# Fill missing numeric values
numeric_cols = [
'Inventory_Level',
'Temperature',
'Humidity',
'Waiting_Time',
'User_Transaction_Amount',
'User_Purchase_Frequency',
'Asset_Utilization',
'Demand_Forecast'
]

df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Fill categorical values
df['Shipment_Status'] = df['Shipment_Status'].fillna("Unknown")
df['Traffic_Status'] = df['Traffic_Status'].fillna("Unknown")
df['Logistics_Delay_Reason'] = df['Logistics_Delay_Reason'].fillna("Unknown")

print("\nData Cleaning Completed")


# 4. FEATURE ENGINEERING


# Waiting category
df['Waiting_Category'] = df['Waiting_Time'].apply(
lambda x: "High Waiting" if x > 30 else "Low Waiting"
)

# Transaction category
df['Transaction_Level'] = df['User_Transaction_Amount'].apply(
lambda x: "High Value" if x > 500 else "Low Value"
)

# Month column
df['Month'] = df['Timestamp'].dt.month

print("\nFeature Engineering Completed")


# 5. EXPLORATORY DATA ANALYSIS


print("\nAverage Waiting Time by Traffic Status")

traffic_analysis = df.groupby('Traffic_Status')['Waiting_Time'].mean()
print(traffic_analysis)

print("\nAsset Utilization Analysis")

asset_util = df.groupby('Asset_ID')['Asset_Utilization'].mean()
print(asset_util)

print("\nTotal Revenue by Asset")

revenue_analysis = df.groupby('Asset_ID')['User_Transaction_Amount'].sum()
print(revenue_analysis)

# 6. VISUALIZATION


sns.set(style="whitegrid")

# Waiting time distribution
plt.figure(figsize=(8,5))
sns.histplot(df['Waiting_Time'], bins=30)
plt.title("Waiting Time Distribution")
plt.xlabel("Waiting Time")
plt.ylabel("Frequency")
plt.show()

# Traffic vs Waiting Time
plt.figure(figsize=(8,5))
sns.boxplot(x='Traffic_Status', y='Waiting_Time', data=df)
plt.title("Traffic Status vs Waiting Time")
plt.show()

# Demand Forecast Trend
plt.figure(figsize=(8,5))
df.groupby('Month')['Demand_Forecast'].mean().plot(kind='line')
plt.title("Monthly Demand Forecast Trend")
plt.xlabel("Month")
plt.ylabel("Average Demand Forecast")
plt.show()

# Asset Utilization
plt.figure(figsize=(10,6))
df.groupby('Asset_ID')['Asset_Utilization'].mean().plot(kind='bar')
plt.title("Asset Utilization by Asset ID")
plt.xlabel("Asset ID")
plt.ylabel("Average Utilization")
plt.show()

# 7. KEY BUSINESS METRICS


total_transactions = df['User_Transaction_Amount'].sum()
avg_waiting = df['Waiting_Time'].mean()
delay_rate = df['Logistics_Delay'].mean() * 100
avg_inventory = df['Inventory_Level'].mean()

print("\n BUSINESS METRICS ")

print("Total Revenue:", total_transactions)
print("Average Waiting Time:", avg_waiting)
print("Logistics Delay Rate:", delay_rate)
print("Average Inventory Level:", avg_inventory)


# 8. SAVE CLEAN DATA


df.to_csv("cleaned_logistics_data.csv", index=False)

print("\nClean dataset saved.")


# 9. LOAD DATA INTO MYSQL DATABASE


# Update credentials before running

username = "root"
password = "Samithnitta$4.8"
host = "localhost"
port=3306
database = "supply_chain_db"

engine = create_engine(
f"mysql+pymysql://{username}:{password}@{host}/{database}"
)

df.to_sql("logistics_data", engine, if_exists="replace", index=False)

print("\nData successfully loaded into MySQL")

