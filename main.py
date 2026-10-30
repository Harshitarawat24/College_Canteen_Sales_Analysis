import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("college_canteen_sales_analysis_dataset.csv")

print("COLLEGE CANTEEN SALES ANALYSIS")
print("-" * 40)

print("\nFirst 5 Records:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nTotal Revenue: ₹", df["Total_Amount_INR"].sum())

print("\nTotal Orders:", df["Order_ID"].nunique())

print("\nTotal Items Sold:", df["Quantity"].sum())
print("\n" + "=" * 50)
print("DATA CLEANING")
print("=" * 50)

print("\nDuplicate Rows:", df.duplicated().sum())

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

df.drop_duplicates(inplace=True)

df.dropna(inplace=True)

df["Date"] = pd.to_datetime(df["Date"])

df["Time"] = pd.to_datetime(
    df["Time"], format="%H:%M"
).dt.time

df["Quantity"] = df["Quantity"].astype(int)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nDataset Shape After Cleaning:")
print(df.shape)

print("\nData Cleaning Completed Successfully!")

print("\n" + "=" * 50)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 50)

# 1. Overall Sales Analysis
total_revenue = df["Total_Amount_INR"].sum()
total_orders = df["Order_ID"].nunique()
total_items_sold = df["Quantity"].sum()
average_order_value = total_revenue / total_orders

print("\n--- Overall Sales ---")
print(f"Total Revenue: Rs. {total_revenue:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Total Items Sold: {total_items_sold}")
print(f"Average Order Value: Rs. {average_order_value:.2f}")

# 2. Best-Selling Items
item_sales = df.groupby("Item_Name")["Quantity"].sum()
item_sales = item_sales.sort_values(ascending=False)

print("\n--- Top 5 Best-Selling Items ---")
print(item_sales.head(5))

# 3. Revenue by Category
category_revenue = df.groupby("Category")["Total_Amount_INR"].sum()
category_revenue = category_revenue.sort_values(ascending=False)

print("\n--- Revenue by Category ---")
print(category_revenue)

# 4. Payment Mode Analysis
payment_analysis = df.groupby("Payment_Mode")["Total_Amount_INR"].sum()
payment_analysis = payment_analysis.sort_values(ascending=False)

print("\n--- Revenue by Payment Mode ---")
print(payment_analysis)

# 5. Daily Sales Analysis
daily_sales = df.groupby("Day_of_Week")["Total_Amount_INR"].sum()
daily_sales = daily_sales.sort_values(ascending=False)

print("\n--- Sales by Day of Week ---")
print(daily_sales)

print("\nSales Analysis Completed Successfully!")

# ==========================================
# STEP 6: DATA VISUALIZATION
# ==========================================

import os
os.makedirs("charts", exist_ok=True)

# Graph 1: Top 10 Best-Selling Items
top_items = df.groupby("Item_Name")["Quantity"].sum()
top_items = top_items.sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
top_items.sort_values().plot(kind="barh")

plt.title("Top 10 Best-Selling Canteen Items")
plt.xlabel("Quantity Sold")
plt.ylabel("Food Item")
plt.tight_layout()
plt.savefig("charts/top_10_items.png")
plt.show()

# Graph 2: Revenue by Category
category_sales = df.groupby("Category")["Total_Amount_INR"].sum()
category_sales = category_sales.sort_values(ascending=False)

plt.figure(figsize=(9, 5))
category_sales.plot(kind="bar")

plt.title("Revenue by Food Category")
plt.xlabel("Category")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/revenue_by_category.png")
plt.show()

# Graph 3: Revenue by Payment Mode
payment_sales = df.groupby("Payment_Mode")["Total_Amount_INR"].sum()

plt.figure(figsize=(7, 7))
payment_sales.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Revenue Share by Payment Mode")
plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/payment_mode.png")
plt.show()

# Graph 4: Daily Sales Trend
df["Date"] = pd.to_datetime(df["Date"])

daily_revenue = df.groupby("Date")["Total_Amount_INR"].sum()

plt.figure(figsize=(12, 5))
plt.plot(daily_revenue.index, daily_revenue.values)

plt.title("Daily Canteen Sales Trend")
plt.xlabel("Date")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/daily_sales_trend.png")
plt.show()

print("\nAll graphs generated successfully!")
print("Graphs are saved in the charts folder.")
# ==========================================
# STEP 7: ADVANCED SALES ANALYSIS
# ==========================================

print("\n" + "=" * 50)
print("ADVANCED SALES ANALYSIS")
print("=" * 50)

# 1. Peak Ordering Hours
df["Hour"] = df["Time"].apply(lambda t: t.hour)

hourly_orders = df.groupby("Hour")["Order_ID"].nunique()
hourly_orders = hourly_orders.sort_values(ascending=False)

print("\n--- Orders by Hour ---")
print(hourly_orders.sort_index())

print("\nPeak Ordering Hour:",
      hourly_orders.idxmax(), ":00")

# Graph: Orders by Hour
plt.figure(figsize=(10, 5))
hourly_orders.sort_index().plot(kind="bar")

plt.title("Orders by Hour")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig("charts/orders_by_hour.png")
plt.show()


# 2. Monthly Sales Analysis
df["Month"] = df["Date"].dt.to_period("M")

monthly_sales = df.groupby("Month")["Total_Amount_INR"].sum()
monthly_sales = monthly_sales.sort_index()

print("\n--- Monthly Revenue ---")
print(monthly_sales)

print("\nHighest Sales Month:",
      monthly_sales.idxmax())

# Graph: Monthly Revenue
plt.figure(figsize=(10, 5))
monthly_sales.plot(kind="bar")

plt.title("Monthly Canteen Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/monthly_sales.png")
plt.show()

# 3. Top Revenue-Generating Items
item_revenue = df.groupby("Item_Name")["Total_Amount_INR"].sum()
item_revenue = item_revenue.sort_values(ascending=False)

print("\n--- Top 5 Items by Revenue ---")
print(item_revenue.head(5))

# 4. Quantity vs Revenue
item_performance = df.groupby("Item_Name").agg(
    Total_Quantity=("Quantity", "sum"),
    Total_Revenue=("Total_Amount_INR", "sum")
)

item_performance = item_performance.sort_values(
    by="Total_Revenue", ascending=False
)

print("\n--- Top 10 Items by Revenue and Quantity ---")
print(item_performance.head(10))
print("\nAdvanced Sales Analysis Completed Successfully!")