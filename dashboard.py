import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="College Canteen Sales Analysis",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ College Canteen Sales Analysis")
st.write("Interactive dashboard for analyzing canteen sales.")

# Load dataset
df = pd.read_csv("college_canteen_sales_analysis_dataset.csv")

df["Date"] = pd.to_datetime(df["Date"])

# Sidebar filters
st.sidebar.header("Filter Sales Data")

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["Date"].min().date(),
    min_value=df["Date"].min().date(),
    max_value=df["Date"].max().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["Date"].max().date(),
    min_value=df["Date"].min().date(),
    max_value=df["Date"].max().date()
)

categories = sorted(df["Category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Categories",
    categories,
    default=categories
)

payment_modes = sorted(df["Payment_Mode"].dropna().unique())

selected_payments = st.sidebar.multiselect(
    "Select Payment Modes",
    payment_modes,
    default=payment_modes
)

# Apply filters
if start_date > end_date:
    st.error("Start Date cannot be after End Date.")
    st.stop()

filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date) &
    (df["Category"].isin(selected_categories)) &
    (df["Payment_Mode"].isin(selected_payments))
]

if filtered_df.empty:
    st.warning("No sales data available for the selected filters.")
    st.stop()

# KPI metrics
total_revenue = filtered_df["Total_Amount_INR"].sum()
total_orders = filtered_df["Order_ID"].nunique()
total_items = filtered_df["Quantity"].sum()
average_order_value = total_revenue / total_orders if total_orders else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Items Sold", f"{total_items:,}")
col4.metric("Average Order Value", f"₹{average_order_value:,.2f}")

st.divider()

# Top-selling items
st.subheader("🏆 Top 10 Best-Selling Items")

top_items = (
    filtered_df.groupby("Item_Name")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

fig1, ax1 = plt.subplots(figsize=(10, 5))
top_items.plot(kind="barh", ax=ax1)
ax1.set_xlabel("Quantity Sold")
ax1.set_ylabel("Food Item")
ax1.set_title("Top 10 Best-Selling Items")
st.pyplot(fig1)
plt.close(fig1)

# Revenue by category and payment mode
col5, col6 = st.columns(2)

with col5:
    st.subheader("📊 Revenue by Category")
    category_revenue = (
        filtered_df.groupby("Category")["Total_Amount_INR"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_revenue)

with col6:
    st.subheader("💳 Revenue by Payment Mode")
    payment_revenue = (
        filtered_df.groupby("Payment_Mode")["Total_Amount_INR"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(payment_revenue)

# Daily sales trend
st.subheader("📈 Daily Sales Trend")

daily_sales = (
    filtered_df.groupby("Date")["Total_Amount_INR"]
    .sum()
    .sort_index()
)

st.line_chart(daily_sales)

# Monthly sales
st.subheader("📅 Monthly Revenue")

monthly_data = filtered_df.copy()
monthly_data["Month"] = monthly_data["Date"].dt.to_period("M").astype(str)

monthly_sales = (
    monthly_data.groupby("Month")["Total_Amount_INR"]
    .sum()
    .sort_index()
)

st.bar_chart(monthly_sales)

# Detailed sales table
st.subheader("📋 Sales Data")

st.dataframe(
    filtered_df.sort_values("Date", ascending=False),
    width="stretch"
)

st.success("Dashboard loaded successfully!")
