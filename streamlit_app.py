
import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# OptiChain Supply Chain Intelligence
# Live Streamlit recreation of the Power BI portfolio dashboard
# ============================================================

st.set_page_config(
    page_title="OptiChain Supply Chain Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background: #f3e98b;
    }

    [data-testid="stSidebar"] {
        background: #8f0000;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .title-box {
        background: #a90000;
        color: white;
        padding: 14px 20px;
        border-radius: 6px;
        text-align: center;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 14px;
    }

    .section-title {
        background: #a90000;
        color: white;
        padding: 9px 14px;
        border-radius: 5px;
        font-size: 21px;
        font-weight: 700;
        margin: 6px 0 12px 0;
    }

    .kpi {
        background: white;
        border: 4px solid #990000;
        border-radius: 7px;
        padding: 10px;
        text-align: center;
        min-height: 105px;
    }

    .kpi-label {
        color: #a90000;
        font-size: 15px;
        font-weight: 700;
    }

    .kpi-value {
        color: #111827;
        font-size: 28px;
        font-weight: 800;
        margin-top: 10px;
    }

    .small-note {
        color: #6b7280;
        font-size: 13px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 3px solid #990000;
        border-radius: 7px;
        padding: 8px;
    }

    .footer {
        text-align: center;
        color: #6b1a1a;
        font-size: 13px;
        padding: 20px 0 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
RAW_PATH = "data/raw/Car_SupplyChainManagementDataSet.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)

    for col in ["OrderDate", "ShipDate"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    text_cols = [
        "CarMaker", "CarModel", "CarColor", "Gender", "ShipMode",
        "Shipping", "CustomerFeedback", "City", "State", "Country",
        "SupplierName", "CustomerName"
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    df = df.drop_duplicates()

    if {"ShipDate", "OrderDate"}.issubset(df.columns):
        df["LeadTimeDays"] = (df["ShipDate"] - df["OrderDate"]).dt.days

    if "OrderDate" in df.columns:
        df["OrderMonth"] = df["OrderDate"].dt.to_period("M").astype(str)
        df["OrderMonthName"] = df["OrderDate"].dt.month_name().str[:3]
        df["OrderQuarter"] = "Q" + df["OrderDate"].dt.quarter.astype(str)

    feedback_map = {
        "Very Bad": 1, "Bad": 2, "Okay": 3, "Good": 4, "Very Good": 5
    }
    if "CustomerFeedback" in df.columns:
        df["FeedbackScore"] = df["CustomerFeedback"].map(feedback_map)

    if {"Sales", "Quantity"}.issubset(df.columns):
        df["RevenuePerUnit"] = np.where(
            df["Quantity"].ne(0),
            df["Sales"] / df["Quantity"],
            np.nan
        )

    return df

if not os.path.exists(RAW_PATH):
    st.error(
        f"Dataset not found at `{RAW_PATH}`. "
        "Make sure the GitHub repository contains the data/raw CSV."
    )
    st.stop()

df = load_data(RAW_PATH)

# ---------- Helpers ----------
def money(value):
    if pd.isna(value):
        return "$0"
    if abs(value) >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value/1_000:.1f}K"
    return f"${value:,.0f}"

def kpi_card(label, value):
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def red_chart(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor="#a90000",
        plot_bgcolor="#a90000",
        font=dict(color="white"),
        margin=dict(l=45, r=25, t=55, b=45),
        legend=dict(font=dict(color="white")),
        xaxis=dict(
            gridcolor="rgba(255,255,255,.35)",
            zerolinecolor="rgba(255,255,255,.35)"
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,.35)",
            zerolinecolor="rgba(255,255,255,.35)"
        ),
    )
    return fig

def apply_filters(data):
    out = data.copy()

    with st.sidebar:
        st.markdown("### Dashboard Filters")

        if "Gender" in out.columns:
            vals = sorted(out["Gender"].dropna().astype(str).unique())
            selected = st.multiselect("Gender", vals, default=vals)
            if selected:
                out = out[out["Gender"].astype(str).isin(selected)]

        if "CarColor" in out.columns:
            vals = sorted(out["CarColor"].dropna().astype(str).unique())
            selected = st.multiselect("Car Color", vals, default=vals)
            if selected:
                out = out[out["CarColor"].astype(str).isin(selected)]

        if "ShipMode" in out.columns:
            vals = sorted(out["ShipMode"].dropna().astype(str).unique())
            selected = st.multiselect("Ship Mode", vals, default=vals)
            if selected:
                out = out[out["ShipMode"].astype(str).isin(selected)]

    return out

# ---------- Sidebar navigation ----------
with st.sidebar:
    st.markdown("## 📊 OptiChain")
    st.markdown("### Supply Chain Intelligence")
    page = st.radio(
        "Select Dashboard",
        [
            "Executive Overview",
            "Operations & Delivery",
            "Sales Performance",
            "Customer 360",
        ],
        index=0,
    )
    st.divider()
    st.caption("Python • SQL • Power BI • DAX")
    st.caption("Portfolio project by Abhishek Shukla")

filtered = apply_filters(df)

# ============================================================
# 1. EXECUTIVE OVERVIEW
# ============================================================
if page == "Executive Overview":
    st.markdown('<div class="title-box">Supply Chain Management</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:white;padding:18px;border-radius:6px;">
        <h2 style="color:#a90000;margin-top:0;">What is Supply Chain?</h2>
        <p>
        A supply chain is a network of companies and people involved in the
        production and delivery of a product or service, including suppliers,
        warehouses, transportation, distribution and customers.
        </p>
        <p>
        This interactive portfolio dashboard analyzes order, sales, supplier,
        delivery and customer data using Python, SQL and BI techniques.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Executive KPIs</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card("Total Sales", money(filtered["Sales"].sum()))
    with c2:
        kpi_card("Total Orders", f"{filtered['OrderID'].nunique():,}")
    with c3:
        kpi_card("Suppliers", f"{filtered['SupplierName'].nunique():,}")
    with c4:
        kpi_card("Customers", f"{filtered['CustomerName'].nunique():,}")

    st.markdown("")
    c1, c2 = st.columns(2)

    monthly = (
        filtered.groupby("OrderMonth", as_index=False)["Sales"]
        .sum()
        .sort_values("OrderMonth")
    )
    fig = px.bar(
        monthly,
        x="OrderMonth",
        y="Sales",
        title="Monthly Sales Trend",
        text_auto=".2s"
    )
    c1.plotly_chart(red_chart(fig), use_container_width=True)

    supplier = (
        filtered.groupby("SupplierName", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )
    fig = px.bar(
        supplier.sort_values("Sales"),
        x="Sales",
        y="SupplierName",
        orientation="h",
        title="Top Suppliers by Revenue"
    )
    c2.plotly_chart(red_chart(fig), use_container_width=True)

    st.markdown('<div class="section-title">Data Quality & Analytical Findings</div>', unsafe_allow_html=True)
    negative = int((filtered["LeadTimeDays"] < 0).sum())
    outlier_q3 = filtered["Sales"].quantile(.75)
    outlier_q1 = filtered["Sales"].quantile(.25)
    iqr = outlier_q3 - outlier_q1
    sales_outliers = int(((filtered["Sales"] < outlier_q1 - 1.5*iqr) |
                          (filtered["Sales"] > outlier_q3 + 1.5*iqr)).sum())

    a, b, c = st.columns(3)
    a.metric("Negative lead-time records", f"{negative:,}")
    b.metric("Sales outliers (IQR)", f"{sales_outliers:,}")
    c.metric("Avg customer feedback", f"{filtered['FeedbackScore'].mean():.2f}/5")

# ============================================================
# 2. OPERATIONS & DELIVERY
# ============================================================
elif page == "Operations & Delivery":
    st.markdown('<div class="title-box">Order Detail Summary</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        kpi_card("Car Models", f"{filtered['CarModel'].nunique():,}")
    with c2:
        kpi_card("Car Makers", f"{filtered['CarMaker'].nunique():,}")

    st.markdown("")
    left, right = st.columns([1, 1.35])

    # State map
    state_orders = (
        filtered.groupby("State", as_index=False)["OrderID"]
        .count()
        .rename(columns={"OrderID": "Orders"})
    )

    with left:
        fig = px.choropleth(
            state_orders,
            locations="State",
            locationmode="USA-states",
            color="Orders",
            scope="usa",
            title="Orders by State",
            color_continuous_scale=["#fee5d9", "#a90000"]
        )
        fig.update_layout(
            height=430,
            paper_bgcolor="#a90000",
            geo=dict(bgcolor="#a90000"),
            font=dict(color="white"),
            margin=dict(l=10, r=10, t=55, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        top_orders = (
            filtered.sort_values("OrderDate", ascending=False)
            .loc[:, ["CustomerName", "CarModel", "OrderDate", "Sales"]]
            .head(15)
            .copy()
        )
        top_orders["Sales"] = top_orders["Sales"].map(money)
        st.markdown("#### Top 15 Orders by Date")
        st.dataframe(
            top_orders,
            use_container_width=True,
            hide_index=True,
            height=400
        )

    st.markdown('<div class="section-title">Delivery Performance</div>', unsafe_allow_html=True)
    mode = (
        filtered.groupby("ShipMode", as_index=False)
        .agg(
            Orders=("OrderID", "count"),
            AvgLeadTime=("LeadTimeDays", "mean"),
            MedianLeadTime=("LeadTimeDays", "median")
        )
    )
    fig = px.bar(
        mode,
        x="ShipMode",
        y="AvgLeadTime",
        text_auto=".2f",
        title="Average Delivery Lead Time by Shipping Mode"
    )
    st.plotly_chart(red_chart(fig), use_container_width=True)

# ============================================================
# 3. SALES PERFORMANCE
# ============================================================
elif page == "Sales Performance":
    st.markdown('<div class="title-box">Sales Detail Summary</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        kpi_card("Total Sales", money(filtered["Sales"].sum()))
    with c2:
        kpi_card("Sum of Discount", f"{filtered['Discount'].sum():,.2f}")

    st.markdown("")
    monthly = (
        filtered.groupby("OrderMonth", as_index=False)["Sales"]
        .sum()
        .sort_values("OrderMonth")
    )

    left, right = st.columns([1.05, 1])

    with left:
        fig = px.bar(
            monthly,
            x="OrderMonth",
            y="Sales",
            title="Sum of Sales by Order Month",
            text_auto=".2s"
        )
        st.plotly_chart(red_chart(fig), use_container_width=True)

        shipmode = (
            filtered.groupby("ShipMode", as_index=False)["Sales"]
            .sum()
        )
        fig = px.pie(
            shipmode,
            names="ShipMode",
            values="Sales",
            hole=.52,
            title="Sum of Sales by Ship Mode"
        )
        fig.update_layout(
            height=340,
            paper_bgcolor="#a90000",
            font=dict(color="white"),
            margin=dict(l=20, r=20, t=55, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        shipping = (
            filtered.groupby("Shipping", as_index=False)["Sales"]
            .sum()
        )
        fig = px.line(
            shipping,
            x="Shipping",
            y="Sales",
            markers=True,
            title="Sum of Sales by Shipping"
        )
        st.plotly_chart(red_chart(fig), use_container_width=True)

        quarter = (
            filtered.groupby("OrderQuarter", as_index=False)["Sales"]
            .sum()
            .sort_values("OrderQuarter")
        )
        fig = px.bar(
            quarter,
            x="OrderQuarter",
            y="Sales",
            title="Sum of Sales by Order Quarter"
        )
        st.plotly_chart(red_chart(fig), use_container_width=True)

# ============================================================
# 4. CUSTOMER 360
# ============================================================
elif page == "Customer 360":
    st.markdown('<div class="title-box">Customer View Detail Summary</div>', unsafe_allow_html=True)

    left, right = st.columns([.75, 1.4])

    with left:
        top = (
            filtered.sort_values("OrderDate", ascending=False)
            .loc[:, ["CustomerName", "CarMaker", "OrderDate"]]
            .head(20)
        )
        st.markdown("#### Top Orders by Date")
        st.dataframe(
            top,
            use_container_width=True,
            hide_index=True,
            height=470
        )

    with right:
        feedback = (
            filtered.groupby("CustomerFeedback", as_index=False)["Sales"]
            .sum()
            .sort_values("Sales", ascending=False)
        )
        fig = px.bar(
            feedback,
            x="CustomerFeedback",
            y="Sales",
            title="Sum of Sales by Customer Feedback",
            text_auto=".2s"
        )
        st.plotly_chart(red_chart(fig), use_container_width=True)

        st.markdown("#### Customer / Product / Geography Breakdown")

        # A Sankey-style flow to approximate the Power BI decomposition view.
        temp = filtered.copy()
        temp["State"] = temp["State"].fillna("Unknown")
        temp["CarModel"] = temp["CarModel"].fillna("Unknown")
        temp["CustomerName"] = temp["CustomerName"].fillna("Unknown")

        top_models = temp.groupby("CarModel")["Sales"].sum().nlargest(8).index
        temp = temp[temp["CarModel"].isin(top_models)]

        model_sales = temp.groupby("CarModel")["Sales"].sum().sort_values(ascending=False)
        state_sales = temp.groupby("State")["Sales"].sum().nlargest(8)
        customer_sales = temp.groupby("CustomerName")["Sales"].sum().nlargest(8)

        labels = (
            ["Total Sales"] +
            model_sales.index.tolist() +
            state_sales.index.tolist() +
            customer_sales.index.tolist()
        )
        index = {name: i for i, name in enumerate(labels)}

        sources, targets, values = [], [], []

        for name, value in model_sales.items():
            sources.append(index["Total Sales"])
            targets.append(index[name])
            values.append(float(value))

        for model in model_sales.index:
            subset = temp[temp["CarModel"] == model]
            state = subset.groupby("State")["Sales"].sum().nlargest(3)
            for name, value in state.items():
                sources.append(index[model])
                targets.append(index[name])
                values.append(float(value))

        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=18,
                line=dict(color="white", width=.5),
                label=labels,
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
            )
        ))
        fig.update_layout(
            height=520,
            title="Sales Decomposition: Product → Geography",
            paper_bgcolor="#a90000",
            font=dict(color="white"),
            margin=dict(l=10, r=10, t=60, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------- Footer ----------
st.markdown(
    '<div class="footer">OptiChain Supply Chain Intelligence • Python • SQL • Power BI • DAX • Portfolio Project by Abhishek Shukla</div>',
    unsafe_allow_html=True
)
