# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 13:49:18 2025

@author: Sneha B
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta

# Load the dataset
df = pd.read_csv(r"C:\Users\sneha\OneDrive\Desktop\DataCoSupplyChainDataset 567.csv", encoding='unicode_escape')

# Convert date columns to datetime format
df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'], errors='coerce')
df['shipping date (DateOrders)'] = pd.to_datetime(df['shipping date (DateOrders)'], errors='coerce')

# Clean the Delivery Status column (strip leading/trailing spaces)
df['Delivery Status'] = df['Delivery Status'].str.strip()

# --- Refined Churn Calculation ---
# 1. Define Churn Window (6 months)
churn_window = timedelta(days=180)  # 6 months = 180 days

# 2. Find the latest date in the dataset
latest_date = df['order date (DateOrders)'].max()

# 3. Calculate the date before the churn window
churn_before_date = latest_date - churn_window

# 4. Group by Customer and find the *last* order with 'Late Delivery' or 'Shipping Cancelled'
bad_delivery = df[df['Delivery Status'].isin(['Late Delivery', 'Shipping Cancelled'])] \
    .sort_values('order date (DateOrders)') \
    .groupby('Order Customer Id') \
    .tail(1) #find the last order with bad delivery status for each customer

# 5. Filter churned customers based on these criteria:
#    a) Last order was a 'bad delivery'
#    b) Last order was *before* the churn window.
churned_customers = bad_delivery[bad_delivery['order date (DateOrders)'] <= churn_before_date]

# 6. Calculate Churn Rate
churn_rate = churned_customers['Order Customer Id'].nunique() / df['Order Customer Id'].nunique() * 100

# Print the churn rate
print(f"Churn Rate: {churn_rate:.2f}%")

# --- Visualization (Churn by Delivery Status) ---
# 1. Prepare data: Count churned customers per delivery status
delivery_churn_counts = churned_customers['Delivery Status'].value_counts()

# 2. Create bar plot
plt.figure(figsize=(8, 6))
if delivery_churn_counts.empty:
    print("Warning: No data to plot for Churn by Delivery Status.")
else:
    delivery_churn_counts.plot(kind='bar', color=['red', 'orange'])
    plt.title('Churn by Delivery Status', fontsize=14)
    plt.xlabel('Delivery Status')
    plt.ylabel('Number of Churned Customers')
    plt.grid()
    plt.show()

# Add a Period column for retention analysis (monthly granularity)
df['Period'] = df['order date (DateOrders)'].dt.to_period('M')

# Calculate Customer Retention Rate (CRR)
def calculate_retention_rate(df):
    customers_per_period = df.groupby('Period')['Order Customer Id'].nunique()
    retention_rate = customers_per_period.shift(-1) / customers_per_period * 100
    return retention_rate

retention_rate = calculate_retention_rate(df)

# Calculate Repeat Purchase Rate (RPR)
repeat_customers = df.groupby('Order Customer Id').size()
repeat_purchase_rate = (repeat_customers[repeat_customers > 1].count() / repeat_customers.count()) * 100

# Print metrics
print(f"Retention Rate:\n{retention_rate}")
print(f"Repeat Purchase Rate: {repeat_purchase_rate:.2f}%")
print(f"Churn Rate: {churn_rate:.2f}%")

# Visualizations

## Retention Rate Over Time
plt.figure(figsize=(10, 6))
if retention_rate.dropna().empty:
    print("Warning: No data to plot for Retention Rate Over Time.")
else:
    retention_rate.dropna().plot(kind='line', marker='o', color='blue')
    plt.title('Customer Retention Rate Over Time', fontsize=14)
    plt.xlabel('Period')
    plt.ylabel('Retention Rate (%)')
    plt.grid()
    plt.show()

## Repeat Purchase Distribution
plt.figure(figsize=(10, 6))
if repeat_customers.empty:
    print("Warning: No data to plot for Repeat Purchase Distribution.")
else:
    sns.histplot(repeat_customers, bins=20, kde=True, color='green')
    plt.title('Distribution of Repeat Purchases per Customer', fontsize=14)
    plt.xlabel('Number of Purchases')
    plt.ylabel('Count of Customers')
    plt.grid()
    plt.show()

## Retention by Delivery Status
retention_by_status = df.groupby('Delivery Status')['Order Customer Id'].nunique()
plt.figure(figsize=(8, 6))
if retention_by_status.empty:
    print("Warning: No data to plot for Retention by Delivery Status.")
else:
    retention_by_status.plot(kind='bar', color=['blue', 'green', 'yellow', 'purple'])
    plt.title('Retention by Delivery Status', fontsize=14)
    plt.xlabel('Delivery Status')
    plt.ylabel('Number of Customers Retained')
    plt.grid()
    plt.show()
