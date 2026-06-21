"""
01_data_cleaning.py + 02_eda_and_outliers.py (combined for portfolio readability;
split into two files in the repo as shown in README)

Run: python python_analysis.py
Produces: data/processed/clean_orders.csv, EDA charts, and a printed insight log.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
RAW_PATH = "data/raw/Car_SupplyChainManagementDataSet.csv"
OUT_DIR = "data/processed"

# ------------------------------------------------------------------
# 1. LOAD + DATA CLEANING
# ------------------------------------------------------------------
df = pd.read_csv(RAW_PATH)

# Standardize dtypes
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df["ShipDate"] = pd.to_datetime(df["ShipDate"], errors="coerce")
for col in ["CarMaker", "CarModel", "CarColor", "Gender", "ShipMode", "Shipping",
            "CustomerFeedback", "City", "State", "Country"]:
    df[col] = df[col].astype(str).str.strip()

# Drop exact duplicate rows
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} exact duplicate rows")

# Missing value audit (kept even though this dataset is unusually clean —
# shows the analyst checks rather than assumes)
missing = df.isnull().sum()
missing = missing[missing > 0]
print("Missing values by column:\n", missing if len(missing) else "None found")

# Feature engineering
df["LeadTimeDays"] = (df["ShipDate"] - df["OrderDate"]).dt.days
df["OrderMonth"] = df["OrderDate"].dt.to_period("M")
feedback_map = {"Very Bad": 1, "Bad": 2, "Okay": 3, "Good": 4, "Very Good": 5}
df["FeedbackScore"] = df["CustomerFeedback"].map(feedback_map)
df["RevenuePerUnit"] = df["Sales"] / df["Quantity"]

# Drop columns with no analytical value / PII not needed for BI (keep raw file untouched)
drop_cols = ["SupplierAddress", "SupplierContactDetails", "CustomerAddress",
             "PhoneNumber", "EmailAddress", "CreditCard"]
df_clean = df.drop(columns=[c for c in drop_cols if c in df.columns])

# ------------------------------------------------------------------
# 2. DATA QUALITY FINDING — negative lead times
# ------------------------------------------------------------------
bad_lead = df_clean[df_clean["LeadTimeDays"] < 0]
print(f"\n[DATA QUALITY] {len(bad_lead)} orders ({len(bad_lead)/len(df_clean):.1%}) "
      f"have ShipDate before OrderDate. Worst case: "
      f"{df_clean['LeadTimeDays'].min()} days. Flagging rather than silently dropping.")

# ------------------------------------------------------------------
# 3. OUTLIER DETECTION (IQR method) on Sales and CarPrice
# ------------------------------------------------------------------
def iqr_outliers(series):
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return series[(series < lower) | (series > upper)]

sales_outliers = iqr_outliers(df_clean["Sales"])
price_outliers = iqr_outliers(df_clean["CarPrice"])
print(f"\nSales outliers (IQR method): {len(sales_outliers)}")
print(f"CarPrice outliers (IQR method): {len(price_outliers)}")

plt.figure(figsize=(8, 5))
sns.boxplot(x=df_clean["Sales"], color="#4C72B0")
plt.title("Sales Distribution — Outlier Check (IQR)")
plt.tight_layout()
plt.savefig("outputs/sales_outliers_boxplot.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 4. CORRELATION ANALYSIS
# ------------------------------------------------------------------
numeric_cols = ["CarPrice", "Sales", "Quantity", "Discount", "LeadTimeDays", "FeedbackScore"]
corr = df_clean[numeric_cols].corr()
print("\nCorrelation matrix:\n", corr.round(2))

plt.figure(figsize=(7, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.title("Correlation Matrix — Numeric Order Attributes")
plt.tight_layout()
plt.savefig("outputs/correlation_heatmap.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 5. TREND ANALYSIS — monthly revenue
# ------------------------------------------------------------------
monthly_rev = df_clean.groupby("OrderMonth")["Sales"].sum().reset_index()
monthly_rev["OrderMonth"] = monthly_rev["OrderMonth"].astype(str)

plt.figure(figsize=(10, 5))
sns.lineplot(data=monthly_rev, x="OrderMonth", y="Sales", marker="o", color="#DD8452")
plt.xticks(rotation=45)
plt.title("Monthly Revenue Trend")
plt.ylabel("Total Sales ($)")
plt.tight_layout()
plt.savefig("outputs/monthly_revenue_trend.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 6. SUPPLIER PERFORMANCE ANALYSIS
# ------------------------------------------------------------------
supplier_perf = (
    df_clean.groupby("SupplierName")
    .agg(TotalOrders=("OrderID", "count"),
         TotalRevenue=("Sales", "sum"),
         AvgFeedback=("FeedbackScore", "mean"),
         AvgLeadTime=("LeadTimeDays", "mean"))
    .sort_values("TotalRevenue", ascending=False)
)
print("\nTop 5 suppliers by revenue:\n", supplier_perf.head())

# ------------------------------------------------------------------
# 7. DELIVERY DELAY ANALYSIS
# ------------------------------------------------------------------
delay_by_mode = df_clean.groupby("ShipMode")["LeadTimeDays"].agg(["mean", "median", "std", "count"])
print("\nLead time by ShipMode (note: should differ by tier, doesn't — flag for ops):\n", delay_by_mode)

plt.figure(figsize=(8, 5))
sns.boxplot(data=df_clean, x="ShipMode", y="LeadTimeDays", hue="ShipMode", palette="Set2", legend=False)
plt.title("Delivery Lead Time by Shipping Mode")
plt.tight_layout()
plt.savefig("outputs/delivery_delay_by_shipmode.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 8. COST OPTIMIZATION — discount vs. revenue relationship
# ------------------------------------------------------------------
plt.figure(figsize=(7, 5))
sns.scatterplot(data=df_clean, x="Discount", y="Sales", hue="ShipMode", alpha=0.6)
plt.title("Discount Level vs. Sales Value")
plt.tight_layout()
plt.savefig("outputs/discount_vs_sales.png", dpi=150)
plt.close()

discount_quartile_summary = (
    df_clean.assign(DiscountBand=pd.qcut(df_clean["Discount"], 4))
    .groupby("DiscountBand")["Sales"].mean()
)
print("\nAvg Sales by Discount Band:\n", discount_quartile_summary)

# ------------------------------------------------------------------
# 9. KPI SUMMARY
# ------------------------------------------------------------------
kpis = {
    "Total Revenue": df_clean["Sales"].sum(),
    "Total Orders": df_clean["OrderID"].nunique(),
    "Average Order Value": df_clean["Sales"].mean(),
    "Average Discount": df_clean["Discount"].mean(),
    "Avg Customer Feedback Score (1-5)": df_clean["FeedbackScore"].mean(),
    "Pct Orders with Negative Lead Time (data issue)": len(bad_lead) / len(df_clean),
}
print("\n=== KPI SUMMARY ===")
for k, v in kpis.items():
    print(f"{k}: {v:,.2f}" if isinstance(v, float) else f"{k}: {v}")

# ------------------------------------------------------------------
# 10. EXPORT FOR POWER BI
# ------------------------------------------------------------------
import os
os.makedirs(OUT_DIR, exist_ok=True)
df_clean.to_csv(f"{OUT_DIR}/clean_orders.csv", index=False)
supplier_perf.to_csv(f"{OUT_DIR}/supplier_performance.csv")
monthly_rev.to_csv(f"{OUT_DIR}/monthly_revenue.csv", index=False)
print(f"\nExported processed datasets to {OUT_DIR}/ for Power BI ingestion.")
