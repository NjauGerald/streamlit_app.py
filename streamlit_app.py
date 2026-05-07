import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Performance Interactive Dashboard")
st.write("This dashboard allows users to explore sales performance by region, category, and date.")

@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.sidebar.header("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Date"].min(), df["Date"].max()]
)

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].nunique()
average_sales = filtered_df["Sales"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", total_orders)
col4.metric("Average Sales", f"${average_sales:,.2f}")

st.markdown("---")

col5, col6 = st.columns(2)

with col5:
    sales_by_region = filtered_df.groupby("Region", as_index=False)["Sales"].sum()
    fig_region = px.bar(
        sales_by_region,
        x="Region",
        y="Sales",
        title="Sales by Region",
        text_auto=True
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col6:
    profit_by_category = filtered_df.groupby("Category", as_index=False)["Profit"].sum()
    fig_category = px.pie(
        profit_by_category,
        names="Category",
        values="Profit",
        title="Profit by Category"
    )
    st.plotly_chart(fig_category, use_container_width=True)

monthly_sales = filtered_df.groupby(
    filtered_df["Date"].dt.to_period("M").astype(str),
    as_index=False
)["Sales"].sum()

monthly_sales.rename(columns={"Date": "Month"}, inplace=True)

fig_monthly = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig_monthly, use_container_width=True)

st.subheader("Filtered Data Preview")
st.dataframe(filtered_df, use_container_width=True)

st.caption("Dashboard created using Streamlit, Pandas, and Plotly.")
