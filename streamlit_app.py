import streamlit as st
import pandas as pd
import numpy as np
import os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="OptiChain | Supply Chain Intelligence",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.metric-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f5f5;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">OptiChain Supply Chain Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">End-to-End Supply Chain Analytics Dashboard | Python • SQL • Power BI</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# FIND DATA
# --------------------------------------------------

possible_files = [
    "data/raw/Car_SupplyChainManagementDataSet.csv",
    "data/raw/Car_SupplyChainManagementDataSet.xlsx",
    "data/Car_SupplyChainManagementDataSet.csv"
]

data_file = None

for file in possible_files:
    if os.path.exists(file):
        data_file = file
        break

if data_file is None:

    st.warning(
        "Dataset file was not found. Please check the repository data path."
    )

    st.info(
        "The dashboard structure is ready. Add the dataset to the expected data folder."
    )

    st.stop()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:

    if data_file.endswith(".csv"):
        df = pd.read_csv(data_file)

    else:
        df = pd.read_excel(data_file)

except Exception as e:

    st.error(f"Unable to load dataset: {e}")
    st.stop()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Dashboard Navigation")

page = st.sidebar.radio(
    "Select Section",
    [
        "Executive Overview",
        "Sales Performance",
        "Operations & Delivery",
        "Customer 360",
        "Data Explorer"
    ]
)

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.sidebar.markdown("### Filters")

filtered_df = df.copy()

# Detect categorical columns automatically

categorical_columns = df.select_dtypes(
    include=["object"]
).columns.tolist()

for column in categorical_columns[:3]:

    values = sorted(
        df[column].dropna().astype(str).unique().tolist()
    )

    if len(values) <= 100:

        selected = st.sidebar.multiselect(
            column,
            values,
            default=values
        )

        if selected:
            filtered_df = filtered_df[
                filtered_df[column].astype(str).isin(selected)
            ]

# --------------------------------------------------
# EXECUTIVE OVERVIEW
# --------------------------------------------------

if page == "Executive Overview":

    st.header("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Records",
        f"{len(filtered_df):,}"
    )

    # Try to identify revenue column

    revenue_column = None

    for column in filtered_df.columns:

        name = column.lower()

        if "sales" in name or "revenue" in name or "orderitemtotal" in name:

            revenue_column = column
            break

    if revenue_column:

        revenue = pd.to_numeric(
            filtered_df[revenue_column],
            errors="coerce"
        ).sum()

        col2.metric(
            "Total Revenue",
            f"${revenue:,.0f}"
        )

    else:

        col2.metric(
            "Total Revenue",
            "N/A"
        )

    # Supplier count

    supplier_column = None

    for column in filtered_df.columns:

        if "supplier" in column.lower():

            supplier_column = column
            break

    if supplier_column:

        suppliers = filtered_df[
            supplier_column
        ].nunique()

        col3.metric(
            "Suppliers",
            f"{suppliers:,}"
        )

    else:

        col3.metric(
            "Suppliers",
            "N/A"
        )

    # Customer count

    customer_column = None

    for column in filtered_df.columns:

        if "customer" in column.lower():

            customer_column = column
            break

    if customer_column:

        customers = filtered_df[
            customer_column
        ].nunique()

        col4.metric(
            "Customers",
            f"{customers:,}"
        )

    else:

        col4.metric(
            "Customers",
            "N/A"
        )

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        filtered_df.head(20),
        use_container_width=True
    )

# --------------------------------------------------
# SALES PERFORMANCE
# --------------------------------------------------

elif page == "Sales Performance":

    st.header("Sales Performance")

    st.subheader("Revenue / Sales Analysis")

    numeric_columns = filtered_df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if numeric_columns:

        selected_metric = st.selectbox(
            "Select Metric",
            numeric_columns
        )

        st.line_chart(
            filtered_df[selected_metric]
        )

        st.subheader("Distribution")

        st.bar_chart(
            filtered_df[selected_metric]
            .value_counts()
            .head(15)
        )

    else:

        st.info("No numeric columns were found.")

# --------------------------------------------------
# OPERATIONS
# --------------------------------------------------

elif page == "Operations & Delivery":

    st.header("Operations & Delivery")

    st.subheader("Shipping / Delivery Analysis")

    shipping_columns = [
        column for column in filtered_df.columns
        if "ship" in column.lower()
        or "delivery" in column.lower()
    ]

    if shipping_columns:

        selected_column = st.selectbox(
            "Select operational field",
            shipping_columns
        )

        st.dataframe(
            filtered_df[selected_column]
            .value_counts()
            .reset_index(),
            use_container_width=True
        )

    else:

        st.info(
            "No shipping or delivery column was automatically detected."
        )

# --------------------------------------------------
# CUSTOMER 360
# --------------------------------------------------

elif page == "Customer 360":

    st.header("Customer 360")

    customer_columns = [
        column for column in filtered_df.columns
        if "customer" in column.lower()
    ]

    if customer_columns:

        selected_customer = st.selectbox(
            "Select Customer Field",
            customer_columns
        )

        customer_summary = (
            filtered_df[selected_customer]
            .value_counts()
            .head(20)
            .reset_index()
        )

        st.dataframe(
            customer_summary,
            use_container_width=True
        )

        st.bar_chart(
            customer_summary.set_index(
                selected_customer
            )
        )

    else:

        st.info(
            "Customer fields were not automatically detected."
        )

# --------------------------------------------------
# DATA EXPLORER
# --------------------------------------------------

elif page == "Data Explorer":

    st.header("Data Explorer")

    st.write(
        f"Rows: **{filtered_df.shape[0]:,}**"
    )

    st.write(
        f"Columns: **{filtered_df.shape[1]:,}**"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "OptiChain Supply Chain Intelligence | "
    "Python • SQL Server • Power BI • DAX"
)
