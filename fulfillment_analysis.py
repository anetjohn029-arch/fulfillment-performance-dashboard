import pandas as pd
import openpyxl
import matplotlib.pyplot as plt

print("======================================")
print("      FULFILLMENT HUB PROJECT")
print("======================================")

# Load the data files

fulfillment = pd.read_csv("Fulfillment_Hub_Sample_Data.csv")

inventory = pd.read_csv("inventory.csv")

issues = pd.read_csv("issues.csv")

orders = pd.read_csv("orders_50.csv")

products = pd.read_csv("products.csv")


print("\nData loaded successfully!")

print("\n--------------------------------------")
print("NUMBER OF RECORDS")
print("--------------------------------------")

print("Fulfillment records:", len(fulfillment))
print("Inventory records:", len(inventory))
print("Issues records:", len(issues))
print("Orders records:", len(orders))
print("Products records:", len(products))


print("\n--------------------------------------")
print("DATA LOADING COMPLETE")
print("--------------------------------------")
# ==========================================
# STEP 2 - DATA INSPECTION
# ==========================================

print("\n======================================")
print("          DATA INSPECTION")
print("======================================")


# Show column names

print("\nFULFILLMENT COLUMNS:")
print(fulfillment.columns.tolist())

print("\nINVENTORY COLUMNS:")
print(inventory.columns.tolist())

print("\nISSUES COLUMNS:")
print(issues.columns.tolist())

print("\nORDERS COLUMNS:")
print(orders.columns.tolist())

print("\nPRODUCTS COLUMNS:")
print(products.columns.tolist())


# ==========================================
# SHOW FIRST 5 ROWS
# ==========================================

print("\n======================================")
print("          SAMPLE DATA")
print("======================================")


print("\nFULFILLMENT SAMPLE:")
print(fulfillment.head())

print("\nINVENTORY SAMPLE:")
print(inventory.head())

print("\nISSUES SAMPLE:")
print(issues.head())

print("\nORDERS SAMPLE:")
print(orders.head())

print("\nPRODUCTS SAMPLE:")
print(products.head())
print("\n========== COLUMN NAMES ==========")

print("\nFulfillment:")
print(fulfillment.columns.tolist())

print("\nInventory:")
print(inventory.columns.tolist())

print("\nIssues:")
print(issues.columns.tolist())

print("\nOrders:")
print(orders.columns.tolist())

print("\nProducts:")
print(products.columns.tolist())
# ==========================================
# STEP 3 - CHECK FOR MISSING VALUES
# ==========================================

print("\n========== MISSING VALUES ==========")

print("\nFulfillment:")
print(fulfillment.isnull().sum())

print("\nInventory:")
print(inventory.isnull().sum())

print("\nIssues:")
print(issues.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

# ==========================================
# STEP 4 - CHECK FOR DUPLICATES
# ==========================================

print("\n========== DUPLICATE CHECK ==========")

print("\nDuplicate Fulfillment records:")
print(fulfillment.duplicated().sum())

print("\nDuplicate Inventory records:")
print(inventory.duplicated().sum())

print("\nDuplicate Issue records:")
print(issues.duplicated().sum())

print("\nDuplicate Order records:")
print(orders.duplicated().sum())

print("\nDuplicate Product records:")
print(products.duplicated().sum())

# ==========================================
# STEP 5 - CHECK ORDER STATUS AND PRIORITY
# ==========================================

print("\n========== ORDER STATUS ==========")

print(orders["Status"].value_counts())

print("\n========== ORDER PRIORITY ==========")

print(orders["Priority"].value_counts())

# ==========================================
# STEP 6 - CHECK INVENTORY STATUS
# ==========================================

print("\n========== INVENTORY STATUS ==========")

print(inventory["Status"].value_counts())

# ==========================================
# STEP 7 - CHECK ISSUE TYPES
# ==========================================

print("\n========== ISSUE TYPES ==========")

print(issues["Issue_Type"].value_counts())

# ==========================================
# STEP 8 - CHECK DATE COLUMNS
# ==========================================

print("\n========== DATE DATA TYPES ==========")

print("\nOrders data types:")
print(orders.dtypes)

print("\nFulfillment data types:")
print(fulfillment.dtypes)

# ==========================================
# STEP 9 - CONVERT DATE COLUMNS
# ==========================================

orders["Order_Date"] = pd.to_datetime(orders["Order_Date"])
orders["Deadline"] = pd.to_datetime(orders["Deadline"])

fulfillment["Order_Date"] = pd.to_datetime(fulfillment["Order_Date"])
fulfillment["Deadline"] = pd.to_datetime(fulfillment["Deadline"])

print("\n========== DATE CONVERSION COMPLETE ==========")

print("\nOrders:")
print(orders[["Order_Date", "Deadline"]].dtypes)

print("\nFulfillment:")
print(fulfillment[["Order_Date", "Deadline"]].dtypes)

# ==========================================
# STEP 10 - CHECK DATE RANGE
# ==========================================

print("\n========== DATE RANGE ==========")

print("\nOrders:")
print("Earliest Order Date:", orders["Order_Date"].min())
print("Latest Order Date:", orders["Order_Date"].max())

print("\nEarliest Deadline:", orders["Deadline"].min())
print("Latest Deadline:", orders["Deadline"].max())

# ==========================================
# STEP 11 - CALCULATE KEY ORDER KPIs
# ==========================================

total_orders = len(orders)

delayed_orders = (orders["Status"] == "Delayed").sum()

high_priority_orders = (orders["Priority"] == "High").sum()

high_priority_delayed = (
    (orders["Priority"] == "High") &
    (orders["Status"] == "Delayed")
).sum()

delayed_rate = (delayed_orders / total_orders) * 100

high_priority_rate = (high_priority_orders / total_orders) * 100

print("\n========== KEY ORDER KPIs ==========")

print("Total Orders:", total_orders)

print("Delayed Orders:", delayed_orders)

print("Delayed Rate:", round(delayed_rate, 2), "%")

print("High Priority Orders:", high_priority_orders)

print("High Priority Rate:", round(high_priority_rate, 2), "%")

print("High Priority Delayed Orders:", high_priority_delayed)

# ==========================================
# STEP 12 - INVENTORY KPI
# ==========================================

total_inventory = len(inventory)

inventory_mismatches = (
    inventory["Status"] == "Mismatch"
).sum()

inventory_mismatch_rate = (
    inventory_mismatches / total_inventory
) * 100

print("\n========== INVENTORY KPI ==========")

print("Total Inventory Records:", total_inventory)

print("Inventory Mismatches:", inventory_mismatches)

print(
    "Inventory Mismatch Rate:",
    round(inventory_mismatch_rate, 2),
    "%"
)

# ==========================================
# STEP 13 - ISSUE KPI
# ==========================================

total_issues = len(issues)

print("\n========== ISSUE KPI ==========")

print("Total Issues:", total_issues)

print(
    "Issue Rate:",
    round((total_issues / total_orders) * 100, 2),
    "%"
)

# ==========================================
# STEP 14 - FULFILLMENT KPI
# ==========================================

total_fulfillment = len(fulfillment)

print("\n========== FULFILLMENT KPI ==========")

print("Total Fulfillment Records:", total_fulfillment)

successful_fulfillment = len(
    fulfillment[fulfillment["Status"] == "Completed"]
)

fulfillment_success_rate = (
    successful_fulfillment / total_fulfillment
) * 100

print("Successful Fulfillment:", successful_fulfillment)
print("Fulfillment Success Rate:", round(fulfillment_success_rate, 2), "%")

print("\n========== FULFILLMENT STATUS ==========")
print(fulfillment["Status"].value_counts())

delayed_fulfillment = len(
    fulfillment[fulfillment["Status"] == "Delayed"]
)

fulfillment_delay_rate = (
    delayed_fulfillment / total_fulfillment
) * 100

print("Delayed Fulfillment:", delayed_fulfillment)
print("Fulfillment Delay Rate:", round(fulfillment_delay_rate, 2), "%")

# ==========================================
# STEP 15 - ORDER KPI
# ==========================================

total_orders = len(orders)

delayed_orders = len(
    orders[orders["Status"] == "Delayed"]
)

order_delay_rate = (
    delayed_orders / total_orders
) * 100

print("\n========== ORDER KPI ==========")
print("Total Orders:", total_orders)
print("Delayed Orders:", delayed_orders)
print("Order Delay Rate:", round(order_delay_rate, 2), "%")

# ==========================================
# STEP 16 - ORDER STATUS CHART
# ==========================================

status_counts = orders["Status"].value_counts()

plt.figure(figsize=(8, 5))
status_counts.plot(kind="bar")

plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

# ==========================================
# STEP 17 - ORDER PRIORITY CHART
# ==========================================

priority_counts = orders["Priority"].value_counts()

plt.figure(figsize=(8, 5))
priority_counts.plot(kind="bar")

plt.title("Order Priority Distribution")
plt.xlabel("Order Priority")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

# ==========================================
# STEP 17 - ORDER PRIORITY CHART
# ==========================================

priority_counts = orders["Priority"].value_counts()

plt.figure(figsize=(8, 5))
priority_counts.plot(kind="bar")

plt.title("Order Priority Distribution")
plt.xlabel("Order Priority")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

# ============================================
# STEP 18 - INVENTORY STATUS CHART
# ============================================

inventory_counts = inventory["Status"].value_counts()

plt.figure(figsize=(8, 5))
inventory_counts.plot(kind="bar")

plt.title("Inventory Status Distribution")
plt.xlabel("Inventory Status")
plt.ylabel("Number of Records")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

# ============================================
# STEP 18 - INVENTORY STATUS CHART
# ============================================

inventory_counts = inventory["Status"].value_counts()

plt.figure(figsize=(8, 5))
inventory_counts.plot(kind="bar")

plt.title("Inventory Status Distribution")
plt.xlabel("Inventory Status")
plt.ylabel("Number of Records")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

# ==========================================
# STEP 19 - INVENTORY MISMATCH CHART
# ==========================================

mismatch_counts = inventory["Status"].value_counts()

plt.figure(figsize=(8, 5))
mismatch_counts.plot(kind="pie", autopct="%1.1f%%")

plt.title("Inventory Status Percentage")
plt.ylabel("")

plt.tight_layout()
plt.show()

# ==========================================
# STEP 20 - HIGH PRIORITY DELAYED ORDERS
# ==========================================

high_priority_delayed = len(
    orders[
        (orders["Priority"] == "High") &
        (orders["Status"] == "Delayed")
    ]
)

print("\n===== HIGH PRIORITY DELAYED ORDERS =====")
print("High Priority Delayed Orders:", high_priority_delayed)

# ==========================================
# STEP 21 - HIGH PRIORITY DELAY RATE
# ==========================================

high_priority_orders = len(
    orders[orders["Priority"] == "High"]
)

high_priority_delay_rate = (
    high_priority_delayed / high_priority_orders
) * 100

print("\n===== HIGH PRIORITY DELAY RATE =====")
print("High Priority Orders:", high_priority_orders)
print("High Priority Delayed Orders:", high_priority_delayed)
print("High Priority Delay Rate:", round(high_priority_delay_rate, 2), "%")

# ==========================================
# STEP 22 - LOCATION-WISE ORDER DISTRIBUTION
# ==========================================

location_counts = orders["Location"].value_counts()

print("\n===== LOCATION-WISE ORDER DISTRIBUTION =====")
print(location_counts)

# ==========================================
# STEP 23 - LOCATION-WISE DELAY ANALYSIS
# ==========================================

location_delayed = orders[orders["Status"] == "Delayed"]["Location"].value_counts()

print("\n===== LOCATION-WISE DELAYED ORDERS =====")
print(location_delayed)

# ==========================================
# STEP 24 - LOCATION-WISE DELAYED ORDERS CHART
# ==========================================

location_delayed.plot(kind="bar", figsize=(8, 5))

plt.title("Location-Wise Delayed Orders")
plt.xlabel("Location")
plt.ylabel("Number of Delayed Orders")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# ==========================================
# STEP 25 - DELAY RATE BY LOCATION
# ==========================================

location_delay_rate = (
    orders.groupby("Location")["Status"]
    .apply(lambda x: (x == "Delayed").mean() * 100)
)

print("\n===== DELAY RATE BY LOCATION =====")
print(location_delay_rate.round(2))

# ==========================================
# STEP 26 - DELAY RATE BY LOCATION CHART
# ==========================================

location_delay_rate.plot(kind="bar", figsize=(9, 5))

plt.title("Delay Rate by Location")
plt.xlabel("Location")
plt.ylabel("Delay Rate (%)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# ==========================================
# STEP 27 - HIGH PRIORITY DELAY RATE CHART
# ==========================================

priority_data = {
    "High Priority Orders": high_priority_orders,
    "High Priority Delayed": high_priority_delayed
}

plt.figure(figsize=(7, 5))

plt.bar(
    priority_data.keys(),
    priority_data.values()
)

plt.title("High Priority Order Delay Analysis")
plt.xlabel("Order Category")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.show()

# ==========================================
# STEP 28 - STATUS-WISE DELAY ANALYSIS
# ==========================================

status_delayed = orders[orders["Status"] == "Delayed"]["Status"].value_counts()

print("\n===== STATUS-WISE DELAY ANALYSIS =====")
print(status_delayed)

# ==========================================
# STEP 29 - STATUS-WISE DELAY CHART
# ==========================================

status_delayed.plot(kind="bar", figsize=(7, 5))

plt.title("Status-Wise Delayed Orders")
plt.xlabel("Order Status")
plt.ylabel("Number of Delayed Orders")

plt.tight_layout()
plt.show()

# ==========================================
# STEP 30 - FINAL KPI SUMMARY
# ==========================================

delay_rate = (delayed_orders / len(orders)) * 100

print("\n===================================")
print("       FULFILLMENT KPI SUMMARY")
print("===================================")

print("Total Orders:", len(orders))
print("Delayed Orders:", delayed_orders)
print("Overall Delay Rate:", round(delay_rate, 2), "%")
print("High Priority Orders:", high_priority_orders)
print("High Priority Delayed:", high_priority_delayed)
print("High Priority Delay Rate:", round(high_priority_delay_rate, 2), "%")

print("\nTop Delayed Locations:")
print(location_delayed.sort_values(ascending=False).head(5))

print("\nDelay Rate by Location:")
print(location_delay_rate.sort_values(ascending=False))