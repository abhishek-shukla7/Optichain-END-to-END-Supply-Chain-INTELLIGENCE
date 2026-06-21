# OptiChain-END to END Supply Chain INTELLIGENCE — End-to-End BI Solution

A full analytics build for an automotive distributor's order pipeline: raw order-level data is profiled and cleaned in Python, normalized into a star schema in SQL Server, analyzed with joins/CTEs/window functions, and surfaced in a 4-page Power BI dashboard for Sales, Operations, and Customer Experience stakeholders.

**Stack:** Python (pandas, matplotlib, seaborn) · SQL Server (T-SQL) · Power BI Desktop · DAX

---

## 1. Business Problem

A car distributor tracks orders across 360+ suppliers and 880+ vehicle SKUs but has no consolidated view of:
- which suppliers and vehicle lines drive revenue vs. sit on slow-moving inventory,
- whether shipping promises (Same Day / First Class / Second Class / Standard) are actually met,
- which customer segments are most profitable and how satisfied they are.

This project builds that view from raw transactional data to a decision-ready dashboard.

## 2. Data

1,000 order records, 33 attributes spanning supplier, vehicle, customer, order/shipping, and payment details (Jun 2018–Jun 2019). Source dataset is a public Kaggle "Supply Chain Management for Car" CSV.

**Known data-quality issue (documented, not hidden):** shipping analysis surfaced **136 orders where `ShipDate` precedes `OrderDate`** (in one case by 163 days), and shipping-mode SLA does not actually predict delivery speed — average lead time is statistically flat across all four `ShipMode` tiers. This is flagged explicitly in the Operations page and the Python EDA notebook as a data-integrity finding, since it's the kind of thing a real analyst is expected to catch rather than visualize blindly.

## 3. Architecture

```
Kaggle CSV
   │
   ▼
Python ETL  (clean, validate, engineer features, profile)
   │
   ▼
SQL Server  (star schema: dim_customer, dim_car, dim_supplier, dim_date, fact_orders)
   │
   ▼
SQL Analysis Layer  (joins, CTEs, window functions, KPI views)
   │
   ▼
Power BI  (data model, DAX measures, 4-page dashboard, drill-through, navigation)
```

## 4. Repository Structure

```
├── data/
│   ├── raw/                     # original CSV
│   └── processed/                # cleaned + feature-engineered exports for Power BI
├── python/
│   ├── 01_data_cleaning.py
│   ├── 02_eda_and_outliers.py
│   ├── 03_supplier_delivery_cost_analysis.py
│   └── requirements.txt
├── sql/
│   ├── 01_schema_and_load.sql
│   ├── 02_joins_and_views.sql
│   ├── 03_ctes_and_kpis.sql
│   └── 04_window_functions.sql
├── powerbi/
│   └── Automotive_Supply_Chain.pbix
├── docs/
│   ├── BRD-FRD.docx
│   ├── data_dictionary.md
│   └── architecture.png
└── screenshots/
    ├── 01_executive_overview.png
    ├── 02_operations_delivery.png
    ├── 03_sales_performance.png
    └── 04_customer_360.png
```

## 5. Dashboard Pages

| Page | Purpose |
|---|---|
| **Executive Overview** | Top-line KPIs: total revenue, order volume, AOV, fulfillment health, MoM trend |
| **Operations & Delivery** | Supplier performance, shipping-mode SLA adherence, delivery-delay outliers, data-quality flag |
| **Sales Performance** | Revenue by maker/model/color/state, discount-vs-sales relationship, gender/color filters |
| **Customer 360** | Customer segmentation, feedback/sentiment breakdown, drill-through from customer to order detail |

## 6. Key Insights

- **Shipping mode is not a reliable predictor of delivery speed**: average lead time is 97 days for "First Class" vs. 87 days for "Standard Class" — the opposite of what the SLA implies. Worth a carrier/SLA audit in a real operational setting.
- **24.5% of orders (245 of 993) show a ship date earlier than the order date**, including one 163-day reversal — flagged as a data-integrity issue for the source system rather than silently dropped.
- **Discount level shows no measurable relationship with order value** (avg sales is ~$847K–$861K across every discount quartile, r ≈ 0.03) — discounting in this channel is not functioning as a revenue lever, a useful finding for a pricing review.
- Revenue, car price, quantity, discount, lead time, and feedback score are **all uncorrelated with each other** (|r| < 0.1 across the board) — documented in the correlation heatmap as a transparency note on the limits of this dataset for predictive work, while still demonstrating full EDA methodology.

## 7. How to Reproduce

```bash
pip install -r python/requirements.txt
python python/01_data_cleaning.py
python python/02_eda_and_outliers.py
python python/03_supplier_delivery_cost_analysis.py
# then run sql/*.sql against SQL Server in order
# then open powerbi/Automotive_Supply_Chain.pbix and Refresh
```

## 8. Author

[AbhishekShukla] — BCA (Big Data Analytics) | Python · SQL · Power BI · Excel · IBM SPSS
[https://www.linkedin.com/in/abhishek-shukla077/] · [Portfolio]

