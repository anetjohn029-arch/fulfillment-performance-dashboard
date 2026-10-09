import streamlit as st
import pandas as pd
from pathlib import Path

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

project_folder = Path(__file__).resolve().parent
orders_path = project_folder / "orders_50.csv"

try:
    orders = pd.read_csv(orders_path)
except FileNotFoundError:
    st.error(f"Orders file not found: {orders_path.name}")
    st.stop()
except pd.errors.EmptyDataError:
    st.error("The orders file is empty or has no column headers.")
    st.stop()

required_order_columns = {
    "Order_ID",
    "Customer",
    "Product",
    "Priority",
    "Deadline",
    "Location",
    "Status",
}
missing_order_columns = required_order_columns.difference(orders.columns)

if missing_order_columns:
    st.error(
        "The orders file is missing required columns: "
        + ", ".join(sorted(missing_order_columns))
    )
    st.stop()

# ---------------------------------------------------
# CALCULATE KPIs
# ---------------------------------------------------

total_orders = len(orders)

order_status = orders["Status"].fillna("").astype(str).str.strip().str.lower()
order_priority = orders["Priority"].fillna("").astype(str).str.strip().str.lower()

delayed_orders = orders[order_status == "delayed"]

delayed_count = len(delayed_orders)

delay_rate = (delayed_count / total_orders) * 100 if total_orders else 0

high_priority_orders = orders[order_priority == "high"]

high_priority_count = len(high_priority_orders)

high_priority_delayed = high_priority_orders[
    order_status.loc[high_priority_orders.index] == "delayed"
]

high_priority_delayed_count = len(high_priority_delayed)
high_priority_delay_rate = (
    high_priority_delayed_count / high_priority_count * 100
    if high_priority_count
    else 0
)

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
    filtered_orders = delayed_orders.copy()

else:
    filtered_orders = orders[
        order_status == selected_status.lower()
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

col1, col2, col3 = st.columns(3)

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

with col3:

    st.metric(
        "High-Priority Delay Rate",
        f"{high_priority_delay_rate:.1f}%"
    )

# ---------------------------------------------------
# INVENTORY HEALTH
# ---------------------------------------------------

st.divider()

st.subheader("Inventory Health")

inventory_path = project_folder / "inventory.csv"
inventory = pd.DataFrame()
inventory_loaded = True

try:
    inventory = pd.read_csv(inventory_path)
except FileNotFoundError:
    inventory_loaded = False
    st.error(f"Inventory file not found: {inventory_path.name}")
except pd.errors.EmptyDataError:
    inventory_loaded = False
    st.error("The inventory file is empty or has no column headers.")
except pd.errors.ParserError as error:
    inventory_loaded = False
    st.error(f"Could not read the inventory file: {error}")

inventory_display_columns = [
    "SKU",
    "Product",
    "System_Stock",
    "Physical_Stock",
    "Difference",
    "Status",
]
missing_inventory_columns = [
    column for column in inventory_display_columns
    if column not in inventory.columns
]

if inventory_loaded and missing_inventory_columns:
    st.warning(
        "Some inventory fields are unavailable: "
        + ", ".join(missing_inventory_columns)
    )

if inventory_loaded:
    inventory_table = inventory.copy()
    if (
        "Difference" not in inventory_table.columns
        and {"System_Stock", "Physical_Stock"}.issubset(inventory_table.columns)
    ):
        system_stock = pd.to_numeric(
            inventory_table["System_Stock"], errors="coerce"
        )
        physical_stock = pd.to_numeric(
            inventory_table["Physical_Stock"], errors="coerce"
        )
        inventory_table["Difference"] = physical_stock - system_stock

    mismatch_mask = pd.Series(False, index=inventory_table.index)
    if "Status" in inventory_table.columns:
        mismatch_mask |= (
            inventory_table["Status"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
            == "mismatch"
        )
    elif "Difference" in inventory_table.columns:
        mismatch_mask |= (
            pd.to_numeric(inventory_table["Difference"], errors="coerce")
            .fillna(0)
            .ne(0)
        )

    inventory_count = len(inventory_table)
    mismatch_count = int(mismatch_mask.sum())
    mismatch_rate = mismatch_count / inventory_count * 100 if inventory_count else 0
    mismatch_supported = (
        "Status" in inventory_table.columns
        or "Difference" in inventory_table.columns
    )

    inventory_col1, inventory_col2, inventory_col3 = st.columns(3)
    with inventory_col1:
        st.metric("Total Inventory Records", inventory_count)
    with inventory_col2:
        st.metric(
            "Inventory Mismatches",
            mismatch_count if mismatch_supported else "N/A",
        )
    with inventory_col3:
        st.metric(
            "Inventory Mismatch Rate",
            f"{mismatch_rate:.1f}%" if mismatch_supported else "N/A",
        )

    available_inventory_columns = [
        column for column in inventory_display_columns
        if column in inventory_table.columns
    ]
    if available_inventory_columns:
        inventory_display = inventory_table[available_inventory_columns].copy()
        inventory_display = inventory_display.rename(
            columns={
                "System_Stock": "System Stock",
                "Physical_Stock": "Physical Stock",
                "Difference": "Stock Difference",
            }
        )

        def highlight_inventory_mismatches(row):
            if mismatch_mask.loc[row.name]:
                return [
                    "background-color: #ffcccc; color: #b30000; font-weight: bold;"
                ] * len(row)
            return [""] * len(row)

        st.dataframe(
            inventory_display.style.apply(
                highlight_inventory_mismatches,
                axis=1,
            ),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No supported inventory fields are available to display.")

# ---------------------------------------------------
# OPEN FULFILLMENT ISSUES
# ---------------------------------------------------

st.divider()

st.subheader("Open Fulfillment Issues")

issues_path = project_folder / "issues.csv"
issues = pd.DataFrame()
issues_loaded = True

try:
    issues = pd.read_csv(issues_path)
except FileNotFoundError:
    issues_loaded = False
    st.error(f"Issues file not found: {issues_path.name}")
except pd.errors.EmptyDataError:
    issues_loaded = False
    st.error("The issues file is empty or has no column headers.")
except pd.errors.ParserError as error:
    issues_loaded = False
    st.error(f"Could not read the issues file: {error}")

issue_display_columns = [
    "Issue_ID",
    "Order_ID",
    "Issue_Type",
    "Priority",
    "Description",
    "Status",
]

if issues_loaded:
    missing_issue_columns = [
        column for column in issue_display_columns
        if column not in issues.columns
    ]
    if missing_issue_columns:
        st.warning(
            "Some issue fields are unavailable: "
            + ", ".join(missing_issue_columns)
        )

    total_issue_count = len(issues)
    open_issue_mask = None
    high_priority_open_mask = None

    if "Status" in issues.columns:
        issue_status = (
            issues["Status"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
        )
        open_issue_mask = issue_status == "open"

    if "Priority" in issues.columns and open_issue_mask is not None:
        issue_priority = (
            issues["Priority"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
        )
        high_priority_open_mask = open_issue_mask & (issue_priority == "high")

    issue_col1, issue_col2, issue_col3 = st.columns(3)
    with issue_col1:
        st.metric("Total Issues", total_issue_count)
    with issue_col2:
        st.metric(
            "Open Issues",
            int(open_issue_mask.sum()) if open_issue_mask is not None else "N/A",
        )
    with issue_col3:
        st.metric(
            "High-Priority Open Issues",
            (
                int(high_priority_open_mask.sum())
                if high_priority_open_mask is not None
                else "N/A"
            ),
        )

    available_issue_columns = [
        column for column in issue_display_columns
        if column in issues.columns
    ]
    if available_issue_columns:
        issues_display = issues[available_issue_columns].copy()

        if high_priority_open_mask is not None:
            def highlight_urgent_issues(row):
                if high_priority_open_mask.loc[row.name]:
                    return [
                        "background-color: #ffcccc; "
                        "color: #b30000; "
                        "font-weight: bold;"
                    ] * len(row)
                return [""] * len(row)

            issues_display = issues_display.style.apply(
                highlight_urgent_issues,
                axis=1,
            )

        st.dataframe(
            issues_display,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No supported issue fields are available to display.")

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

inventory_csv_data = (
    inventory_display.to_csv(index=False)
    if inventory_loaded and available_inventory_columns
    else ""
)

st.download_button(
    label="Download Inventory Data as CSV",
    data=inventory_csv_data,
    file_name="xyz_fulfillment_inventory_data.csv",
    mime="text/csv",
    disabled=not inventory_loaded or not available_inventory_columns,
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "XYZ E-commerce Fulfillment Analytics | "
    "Built using Python, Pandas and Streamlit"
)
