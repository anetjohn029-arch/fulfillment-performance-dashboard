import streamlit as st
import pandas as pd

# ---------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------

st.set_page_config(
    page_title="XYZ Fulfillment Dashboard",
    page_icon="📦",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📦 XYZ E-commerce Fulfillment Dashboard")

st.write(
    "Operational dashboard for monitoring orders, delays, "
    "priority orders and fulfillment locations."
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

orders = pd.read_csv("orders_50.csv")

# ---------------------------------------------------
# CALCULATE KPIs
# ---------------------------------------------------

total_orders = len(orders)

delayed_orders = orders[
    orders["Status"].str.strip().str.lower() == "delayed"
]

delayed_count = len(delayed_orders)

delay_rate = (delayed_count / total_orders) * 100

high_priority_orders = orders[
    orders["Priority"].str.strip().str.lower() == "high"
]

high_priority_count = len(high_priority_orders)

high_priority_delayed = high_priority_orders[
    high_priority_orders["Status"].str.strip().str.lower() == "delayed"
]

high_priority_delayed_count = len(high_priority_delayed)

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Orders",
        total_orders
    )

with col2:
    st.metric(
        "Delayed Orders",
        delayed_count
    )

with col3:
    st.metric(
        "Overall Delay Rate",
        f"{delay_rate:.0f}%"
    )

with col4:
    st.metric(
        "High Priority Orders",
        high_priority_count
    )

st.divider()

# ---------------------------------------------------
# FILTER
# ---------------------------------------------------

st.subheader("🔎 Order Status Filter")

status_options = [
    "All Orders",
    "Delayed Only",
    "Processing",
    "Picking",
    "Packing",
    "Staging"
]

selected_status = st.selectbox(
    "Select the order status you want to view:",
    status_options
)

if selected_status == "All Orders":
    filtered_orders = orders.copy()

elif selected_status == "Delayed Only":
    filtered_orders = orders[
        orders["Status"].str.strip().str.lower() == "delayed"
    ].copy()

else:
    filtered_orders = orders[
        orders["Status"].str.strip().str.lower()
        == selected_status.lower()
    ].copy()

# ---------------------------------------------------
# ORDER DATA
# ---------------------------------------------------

st.subheader("📋 Order Data")

st.write(
    f"Showing **{len(filtered_orders)}** order(s)."
)

# ---------------------------------------------------
# HIGHLIGHT DELAYED STATUS
# ---------------------------------------------------

def highlight_delayed(row):

    styles = [""] * len(row)

    status_column_position = orders.columns.get_loc("Status")

    if str(row["Status"]).strip().lower() == "delayed":
        styles[status_column_position] = (
            "background-color: #ffcccc; "
            "color: #b30000; "
            "font-weight: bold;"
        )

    return styles


styled_orders = filtered_orders.style.apply(
    highlight_delayed,
    axis=1
)

st.dataframe(
    styled_orders,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------
# DELAYED ORDERS SECTION
# ---------------------------------------------------

st.divider()

st.subheader("🚨 Delayed Orders Requiring Attention")

if delayed_count > 0:

    delayed_display = delayed_orders[
        [
            "Order_ID",
            "Customer",
            "Product",
            "Priority",
            "Deadline",
            "Location",
            "Status"
        ]
    ].copy()

    st.dataframe(
        delayed_display.style.apply(
            lambda row: [
                "background-color: #ffcccc; "
                "color: #b30000; "
                "font-weight: bold;"
            ] * len(row),
            axis=1
        ),
        use_container_width=True,
        hide_index=True
    )

else:

    st.success("No delayed orders found.")

# ---------------------------------------------------
# HIGH PRIORITY ANALYSIS
# ---------------------------------------------------

st.divider()

st.subheader("⭐ High Priority Order Analysis")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "High Priority Orders",
        high_priority_count
    )

with col2:

    st.metric(
        "High Priority Delayed",
        high_priority_delayed_count
    )

# ---------------------------------------------------
# LOCATION-WISE DELAY ANALYSIS
# ---------------------------------------------------

st.divider()

st.subheader("📍 Location-Wise Delayed Orders")

location_delays = (
    delayed_orders["Location"]
    .value_counts()
    .rename_axis("Location")
    .to_frame("Delayed Orders")
)

st.bar_chart(location_delays)

# ---------------------------------------------------
# DELAY RATE BY LOCATION
# ---------------------------------------------------

st.subheader("📈 Delay Rate by Location")

location_total = (
    orders["Location"]
    .value_counts()
)

location_delayed = (
    delayed_orders["Location"]
    .value_counts()
)

location_delay_rate = (
    location_delayed
    .div(location_total)
    .fillna(0)
    * 100
).sort_values(ascending=False)

location_delay_rate = location_delay_rate.rename(
    "Delay Rate (%)"
)

st.dataframe(
    location_delay_rate.round(2),
    use_container_width=True
)

# ---------------------------------------------------
# DOWNLOAD DATA
# ---------------------------------------------------

st.divider()

st.subheader("📥 Export Data")

csv_data = filtered_orders.to_csv(index=False)

st.download_button(
    label="Download Current Data as CSV",
    data=csv_data,
    file_name="xyz_fulfillment_filtered_data.csv",
    mime="text/csv"
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "XYZ E-commerce Fulfillment Analytics | "
    "Built using Python, Pandas and Streamlit"
)
