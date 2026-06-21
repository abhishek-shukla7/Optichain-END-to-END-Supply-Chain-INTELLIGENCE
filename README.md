# OptiChain: End-to-End Supply Chain Intelligence Dashboard

An end-to-end Data Analytics and Business Intelligence project built using Python, SQL Server, and Power BI to analyze supply chain operations, sales performance, customer behavior, and delivery efficiency for an automotive distribution business.

---

## Project Overview

Organizations generate large volumes of supply chain data but often struggle to convert it into actionable insights. This project demonstrates a complete analytics workflow, starting from raw transactional data and ending with interactive business dashboards.

The solution combines:

* Data Cleaning and Exploratory Data Analysis (Python)
* Data Modeling and Business Queries (SQL Server)
* Interactive Reporting and KPI Tracking (Power BI)
* Business Documentation and Dashboard Storytelling

The objective is to help decision-makers monitor supplier performance, sales trends, customer behavior, and operational efficiency through a centralized analytics platform.

---

## Business Problem

A vehicle distribution company manages:

* 360+ suppliers
* 880+ vehicle products
* Multiple shipping methods
* Thousands of customer transactions

The company lacks visibility into:

* Revenue-driving suppliers and vehicle models
* Customer purchasing patterns
* Shipping and delivery performance
* Discount effectiveness
* Operational bottlenecks

This project addresses these challenges through data-driven analytics and visualization.

---

## Technology Stack

| Tool       | Purpose                 |
| ---------- | ----------------------- |
| Python     | Data Cleaning & EDA     |
| Pandas     | Data Manipulation       |
| Matplotlib | Visualization           |
| Seaborn    | Statistical Analysis    |
| SQL Server | Data Modeling & Queries |
| Power BI   | Dashboard Development   |
| DAX        | KPI Calculations        |
| Excel      | Initial Data Validation |

---

## Project Architecture

Raw Dataset (CSV)

↓

Python Data Cleaning & Feature Engineering

↓

SQL Server Analysis Layer

↓

Power BI Data Model & DAX Measures

↓

Interactive Dashboard Reporting

---

## Dataset Information

Source:
Supply Chain Management for Car Dataset (Kaggle)

Dataset Size:

* 1,000 Records
* 33 Columns
* Period: June 2018 – June 2019

Key Attributes:

* Supplier Information
* Product Information
* Customer Information
* Order Details
* Shipping Details
* Pricing & Discounts
* Customer Feedback

---

## Repository Structure

```text

Optichain-End-to-End-Supplychain-intelligence
|
├── data
│ ├── raw
│ │ ├── Car_SupplyChainManagementDataSet.csv
│ │ └── Car_SupplyChainManagementDataSet.xlsx
│ │
│ └── processed
│ ├── clean_orders.csv
│ ├── monthly_revenue.csv
│ └── supplier_performance.csv
|
├── outputs
│   ├── correlation_heatmap.png
│   ├── delivery_delay_by_shipping.png
│   ├── discount_vs_sales.png
│   ├── monthly_revenue_trend.png
│   └── sales_outliers_boxplot.png
│
├── powerbi
│   └── OptiChain_Supply_Intelligence.pbix
│
├── Python
│   └── python_analysis.py
│
├── Screenshots
│   ├── Executive overview.png
│   ├── Operations & Delivery.png
│   ├── Sales Performance.png
│   └── Customer 360.png
│
├── Sql
│   └── sql_queries.sql
│
├── BRD-FRD Document.docx
└── README.md
```

## Dashboard Pages

### 1. Executive Overview

Provides high-level business KPIs including:

* Revenue Overview
* Supply Chain Fundamentals
* Navigation Across Reports
* Business Context

### 2. Operations & Delivery

Focuses on:

* Delivery Performance
* Shipping Mode Analysis
* Supplier Availability
* Order Tracking
* Geographic Distribution

### 3. Sales Performance

Provides:

* Revenue Trends
* Discount Analysis
* Shipping Impact on Sales
* Product Performance
* Customer Segmentation

### 4. Customer 360

Provides:

* Customer Insights
* Feedback Analysis
* Product Preferences
* Geographic Analysis
* Customer-Level Drillthrough

---

## Python Analysis

The Python workflow performs:

### Data Cleaning

* Missing Value Checks
* Data Type Conversion
* Date Processing
* Validation Checks

### Exploratory Data Analysis

* Correlation Analysis
* Revenue Trend Analysis
* Discount Impact Analysis
* Delivery Performance Analysis
* Outlier Detection

Generated Visualizations:

* Correlation Heatmap
* Monthly Revenue Trend
* Discount vs Sales Analysis
* Delivery Delay Analysis
* Sales Outlier Detection

---

## SQL Analysis

Implemented SQL concepts include:

### Joins

* Supplier Analysis
* Customer Analysis
* Product Analysis

### Aggregations

* Revenue KPIs
* Sales Metrics
* Order Metrics

### Window Functions

* Ranking
* Running Totals
* Revenue Comparison

### Business Queries

* Top Customers
* Top Products
* Revenue Contribution
* Supplier Performance

---

## Key Business Insights

### Delivery Issues

* Several records showed inconsistencies between OrderDate and ShipDate.
* Delivery timelines require validation before operational reporting.

### Discount Analysis

* Discounts demonstrated minimal impact on overall sales performance.

### Revenue Trends

* Monthly sales remained relatively stable throughout the reporting period.

### Customer Behavior

* Revenue was distributed across multiple customer segments without significant concentration.

---

## Dashboard Features

* Interactive Navigation
* Cross Filtering
* Drill Through
* Dynamic KPIs
* Geographic Analysis
* Customer-Level Insights
* DAX Measures
* Multi-Page Reporting

---

## How to Run

### Python

```bash
pip install pandas matplotlib seaborn
python python_analysis.py
```

### SQL

1. Open SQL Server Management Studio
2. Execute sql_queries.sql
3. Review generated outputs

### Power BI

1. Open OptiChain_Supply_Intelligence.pbix
2. Refresh Data
3. Explore Dashboard Pages

---

## Skills Demonstrated

* Data Cleaning
* Exploratory Data Analysis
* SQL Query Writing
* Data Modeling
* Dashboard Development
* DAX Calculations
* Business Analysis
* Data Visualization
* Supply Chain Analytics

---

## Author

### Abhishek Shukla

BCA (Big Data Analytics)

Skills:
Python | SQL | Power BI | Excel | IBM SPSS | Data Analytics

LinkedIn:
https://www.linkedin.com/in/abhishek-shukla077/

---

⭐ If you found this project interesting, feel free to connect and provide feedback.
