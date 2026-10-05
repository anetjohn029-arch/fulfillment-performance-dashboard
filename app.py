import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(
    page_title="Fulfillment Dashboard",
    page_icon="📦",
    layout="wide"
)

# Title
st.title("📦 Fulfillment Performance Dashboard")
st.write("Order fulfillment analysis and KPI dashboard")

# Load orders data
orders = pd.read_csv("orders_50.csv")

# Display the data
st.subheader("📊 Order Data")
st.dataframe(orders)