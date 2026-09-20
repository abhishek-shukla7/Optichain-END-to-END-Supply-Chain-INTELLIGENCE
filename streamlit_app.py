import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="OptiChain Supply Chain Intelligence",
    page_icon="📊",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================

DATA_PATH = "data/raw/Car_SupplyChainManagementDataSet.csv"

try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()

# =========================
# TITLE
# =========================

st.title("📊 OptiChain Supply Chain Intelligence")

st.markdown(
    """
    **End-to-End Supply Chain Analytics Dashboard**

    Python • SQL • Power BI • DAX
    """
)

st.divider()

# =========================
# SIDEBAR
# =========================

st.sidebar.title("Dashboard Navigation")

page = st.sidebar.radio(
    "Select Dashboard",
    [
        "Executive Overview",
        "Sales Performance",
        "Operations & Delivery",
        "Customer 360",
        "Data Explorer"
    ]
)

# =========================
# EXECUTIVE OVERVIEW
# =========================

if page == "Executive Overview":

    st.header("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Records",
        f"{len(df):,}"
    )

    # Detect important columns
    revenue_col = next(
        (
            c for c in df.columns
            if any(
                x in c.lower()
                for x in [
                    "sales",
                    "revenue",
                    "orderitemtotal",
                    "sales amount"
                ]
            )
        ),
        None
    )

    supplier_col = next(
        (
            c for c in df.columns
            if "supplier" in c.lower()
        ),
        None
    )

    customer_col = next(
        (
            c for c in df.columns
            if "customer" in c.lower()
        ),
        None
    )

    if revenue_col:

        revenue = pd.to_numeric(
            df[revenue_col],
            errors="coerce"
        ).sum()

        col2.metric(
            "Total Revenue",
            f"${revenue:,.0f}"
        )

    else:

        col2.metric(
            "Revenue",
            "N/A"
        )

    if supplier_col:

        col3.metric(
            "Suppliers",
            f"{df[supplier_col].nunique():,}"
        )

    else:

        col3.metric(
            "Suppliers",
            "N/A"
        )

    if customer_col:

        col4.metric(
            "Customers",
            f"{df[customer_col].nunique():,}"
        )

    else:

        col4.metric(
            "Customers",
            "N/A"
        )

    st.divider()

    # =========================
    # DATA PREVIEW
    # =========================

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    # =========================
    # NUMERIC SUMMARY
    # =========================

    st.subheader("Numerical Summary")

    st.dataframe(
        df.describe().T,
        use_container_width=True
    )


# =========================
# SALES PERFORMANCE
# =========================

elif page == "Sales Performance":

    st.header("📈 Sales Performance")

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        selected_column = st.selectbox(
            "Select Sales Metric",
            numeric_columns
        )

        fig = px.histogram(
            df,
            x=selected_column,
            title=f"{selected_column} Distribution",
            marginal="box"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Top Values")

        top_values = (
            df[selected_column]
            .value_counts()
            .head(15)
            .reset_index()
        )

        top_values.columns = [
            selected_column,
            "Count"
        ]

        fig2 = px.bar(
            top_values,
            x=selected_column,
            y="Count",
            title=f"Top {selected_column} Values"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    else:

        st.info(
            "No numeric columns were detected."
        )


# =========================
# OPERATIONS
# =========================

elif page == "Operations & Delivery":

    st.header("🚚 Operations & Delivery")

    operational_columns = [
        c for c in df.columns
        if any(
            x in c.lower()
            for x in [
                "shipping",
                "ship",
                "delivery",
                "order status",
                "department"
            ]
        )
    ]

    if operational_columns:

        selected_column = st.selectbox(
            "Select Operational Dimension",
            operational_columns
        )

        counts = (
            df[selected_column]
            .astype(str)
            .value_counts()
            .head(20)
            .reset_index()
        )

        counts.columns = [
            selected_column,
            "Count"
        ]

        fig = px.bar(
            counts,
            x="Count",
            y=selected_column,
            orientation="h",
            title=f"{selected_column} Analysis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No operational fields were automatically detected."
        )


# =========================
# CUSTOMER 360
# =========================

elif page == "Customer 360":

    st.header("👥 Customer 360")

    customer_columns = [
        c for c in df.columns
        if "customer" in c.lower()
    ]

    if customer_columns:

        selected_customer = st.selectbox(
            "Customer Field",
            customer_columns
        )

        customer_counts = (
            df[selected_customer]
            .astype(str)
            .value_counts()
            .head(20)
            .reset_index()
        )

        customer_counts.columns = [
            selected_customer,
            "Orders"
        ]

        fig = px.bar(
            customer_counts,
            x="Orders",
            y=selected_customer,
            orientation="h",
            title="Top Customers"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            customer_counts,
            use_container_width=True
        )

    else:

        st.info(
            "No customer column was detected."
        )


# =========================
# DATA EXPLORER
# =========================

elif page == "Data Explorer":

    st.header("🔎 Data Explorer")

    st.write(
        f"**Rows:** {df.shape[0]:,}"
    )

    st.write(
        f"**Columns:** {df.shape[1]:,}"
    )

    st.dataframe(
        df,
        use_container_width=True
    )


# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "OptiChain Supply Chain Intelligence | "
    "Developed by Abhishek Shukla"
)
