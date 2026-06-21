# Portfolio Transformation Guide

## 1. Naming

**Repository name:** `automotive-supply-chain-analytics` (alternatives: `car-orders-bi-pipeline`, `auto-dealer-sales-analytics`)

**Resume project title:** *"Automotive Supply Chain Analytics Dashboard — Python ETL, SQL Server Modeling & Power BI Reporting"*

## 2. Honest Rating

**Before (as downloaded):** 3.5/10 for portfolio purposes.
Reasons: matches a known public repo almost verbatim, README claims (Python/SQL/Kaggle API) aren't backed by files in the repo, no documented insights, generic page names, decorative-only decomposition tree, no acknowledgment that the dataset is synthetic. It would pass a casual resume scan but fail the moment an interviewer asks "walk me through how you built this" or "what did the data tell you."

**After (with the files below applied):** 7.5–8/10 for a fresher/early-career Data/BI Analyst role.
You now have: a real cleaning + EDA + outlier + correlation + trend script you can run and explain line by line, a normalized SQL schema with joins/CTEs/window functions, a documented data-quality finding you discovered yourself (not copied), and a README that matches what's actually in the repo. It won't compete with a real production dataset project, but it stops being recognizable as "that GitHub clone" and starts being defensible.

**Is it worth keeping on your resume?** Yes, conditionally — only after you (a) actually run the Python/SQL yourself and can explain every line, (b) rebuild at least the page names/KPIs/insights so it's visually distinct from the original, and (c) can answer "is this real data?" honestly (see interview answer below). Don't list it as your *only* project — pair it with one project using a dataset nobody else picked (scrape something, use a niche Kaggle set, or your own data from the Deloitte/Walmart simulations).

## 3. What looks copied vs. what's now yours

| Element | Status |
|---|---|
| Raw CSV | Keep — but explicitly cite as public Kaggle dataset, don't claim API ingestion you didn't build |
| Original README | **Remove entirely**, replace with the rewritten one |
| 4 generic page names | Rename (below) |
| PBIX visuals | Keep structure, rename titles, add 2-3 new visuals (below), swap theme |
| "Python + SQL Server" claim with no files | **Fixed** — files now exist and run |
| Decomposition tree (decorative) | Repurpose to answer one real question: "which CarMaker → CarModel → Color drives the most negative feedback?" |

## 4. New Dashboard Page Names & Content

1. **Executive Overview** (was "Home") — KPI cards: Total Revenue, Total Orders, Avg Order Value, Avg Feedback Score, % Orders with Lead-Time Data Issue; MoM revenue trend line.
2. **Operations & Delivery** (was "Orders") — Avg lead time by ShipMode (bar), data-quality callout card, top suppliers table, map by state.
3. **Sales Performance** (was "Sales") — Revenue by CarMaker/Model (column), discount-vs-sales scatter, color/gender slicers, top 15 orders table.
4. **Customer 360** (was "Customer View") — feedback distribution (donut: Very Bad→Very Good), decomposition tree (Maker→Model→Feedback), customer spend-quartile table, drill-through to order detail.

## 5. New KPI Cards
- Total Revenue, Total Orders, Average Order Value
- Average Discount %, Average Feedback Score (1–5 scale)
- % Orders with Negative Lead Time (data-quality KPI — distinctive, shows real analysis)
- Repeat Customer Rate

## 6. New Visualizations (different from the original)
- Correlation heatmap (numeric attributes) — static image or matrix visual
- Discount-band vs. avg-sales bar chart
- Lead-time box plot by ShipMode (shows the SLA mismatch visually)
- Customer spend-quartile bar (from `NTILE(4)` SQL query)
- Supplier scorecard table: revenue, avg feedback, avg lead time side by side

## 7. SQL / Python / Power BI improvements
- **SQL:** Normalize the flat file into the star schema in `sql/01_schema_and_load.sql` — this alone is the single biggest credibility upgrade, since querying one flat CSV table doesn't demonstrate database design skill.
- **Python:** Add the cleaning/EDA/outlier/correlation/trend/supplier/delivery/cost script (provided) and actually run it — keep the printed output as evidence (screenshot it).
- **Power BI:** Switch off the stock "Sunflower Twilight" theme for a custom one matching your README branding; replace decorative images with the new KPI cards and correlation/lead-time visuals; add a bookmark-based nav bar if not already present; add tooltips explaining the data-quality KPI.

## 8. Files to keep / modify / remove

| File | Action |
|---|---|
| `Car_SupplyChainManagementDataSet.csv` | Keep, move to `data/raw/` |
| `Supply_Chain_Project.pbix` | Modify (rename pages, add visuals/KPIs, new theme), move to `powerbi/` |
| `BRD-FRD_Document.docx` | Keep in `docs/`, lightly edit to reflect what you actually built |
| `README.md` | **Replace** with the rewritten version |
| New: `python/python_analysis.py` (or split into 3 files) | Add |
| New: `sql/sql_queries.sql` (or split into 4 files) | Add |
| New: `data/processed/*.csv` (script outputs) | Add — proof the pipeline runs |
| New: `outputs/*.png` (chart exports) | Add as evidence/screenshots |
| New: `docs/data_dictionary.md` | Add — list all 33 columns with type + description |

## 9. Professional Folder Structure
```
automotive-supply-chain-analytics/
├── README.md
├── data/
│   ├── raw/
│   └── processed/
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
│   └── data_dictionary.md
└── screenshots/
```

## 10. Screenshots to create
1. Executive Overview page (full)
2. Operations & Delivery page, zoomed on the data-quality KPI card
3. Sales Performance page
4. Customer 360 page with decomposition tree expanded
5. Terminal output of `python_analysis.py` running (proves it executes)
6. Correlation heatmap and lead-time boxplot (standalone, for LinkedIn posts)
7. SSMS screenshot showing the star schema (Object Explorer) and one window-function query result

## 11. Resume Bullet Points
- Built an end-to-end BI pipeline (Python → SQL Server → Power BI) processing 1,000+ automotive supply chain orders across 360+ suppliers, normalizing a flat dataset into a 5-table star schema.
- Performed data cleaning, outlier detection (IQR), and correlation analysis in Python/pandas; identified and documented a data-integrity issue affecting 24.5% of records that would have invalidated downstream delivery-SLA reporting.
- Wrote 10+ T-SQL queries using CTEs, window functions (RANK, NTILE, LAG), and multi-table joins to power KPI and customer-segmentation views.
- Designed a 4-page Power BI dashboard (Executive, Operations, Sales, Customer 360) with drill-through, DAX measures, and slicers, translating raw order data into supplier and delivery-performance insights.

## 12. Interview Questions & Strong Answers

**Q1: Is this a real-world dataset?**
A: "It's a public Kaggle dataset of synthetic order data — I want to be upfront about that. What I focused on was treating it like a real analyst would: I profiled it, found that 24.5% of records had ship dates before order dates, and that shipping-mode tier didn't actually predict delivery speed — both things you'd flag before trusting any report built on top of this data. The pipeline and SQL design are built the way I'd build them for real data."

**Q2: Walk me through your architecture.**
A: "Raw CSV → Python for cleaning, feature engineering (lead time, feedback score), outlier and correlation analysis → normalized into a star schema in SQL Server with a fact_orders table and four dimension tables → SQL layer with views, CTEs, and window functions for KPIs → Power BI for the final 4-page dashboard with drill-through."

**Q3: Why did you normalize a flat CSV into a star schema instead of just loading it directly?**
A: "The flat file mixes grain — supplier, customer, and car attributes are repeated on every row. Normalizing into dim/fact tables removes redundancy, lets me write real joins and window functions instead of just GROUP BY on one table, and matches how this would actually be modeled in a production warehouse feeding Power BI."

**Q4: What was your most interesting finding?**
A: "That delivery speed didn't correlate with shipping tier at all — First Class averaged 97 days, slower than Standard Class at 87. In a real ops setting that's a red flag worth escalating, not just a chart to show."

**Q5: What would you do differently with more time / real data?**
A: "Validate the source system feed to fix the negative lead-time records at the source rather than just flagging them, add a true sentiment-analysis NLP step on free-text feedback if it existed, and build incremental refresh instead of a full reload given Power BI's row-level display limits on large fact tables."

**Q6 (Python-specific): How did you detect outliers and why that method?**
A: "I used the IQR method on Sales and CarPrice — it's robust to non-normal distributions, which this data has. Interestingly there were zero IQR outliers, which combined with the flat correlation matrix told me the dataset was generated with fairly uniform random distributions rather than real market variance — useful context I documented rather than ignored."

**Q7 (SQL-specific): Give an example of a window function you used and why.**
A: "`NTILE(4)` over customer total spend to build spend quartiles for segmentation, and `LAG()` over monthly revenue to compute month-over-month growth without a self-join — cleaner and more performant than the join-based approach."

## 13. Recruiter-Friendly One-Line Summary
"End-to-end analytics project (Python, SQL Server, Power BI) that cleans and models 1,000 automotive supply chain orders, surfaces a real data-quality finding affecting a quarter of the dataset, and presents supplier/delivery/sales insights across a 4-page interactive dashboard."

## 14. 2–3 Day Action Plan

**Day 1 (3–4 hrs):**
- Replace README, restructure repo folders as above.
- Run `python_analysis.py` end-to-end against your CSV, save terminal output + chart PNGs.
- Set up SQL Server (or Azure SQL free tier / local SQL Express), run `01_schema_and_load.sql`, load `data/processed/clean_orders.csv` via Power Query or BULK INSERT split into the 5 tables.

**Day 2 (3–4 hrs):**
- Run all SQL queries in `02–04`, capture 2-3 SSMS screenshots.
- In Power BI: rename pages, swap theme, add the new KPI cards and 3 new visuals, wire the decomposition tree to Maker→Model→Feedback, add a data-quality callout.
- Fill in the README "Key Insights" section with your own phrasing of the findings (don't copy mine verbatim — explain it the way you'd say it out loud).

**Day 3 (2–3 hrs):**
- Take the 7 screenshots listed above.
- Write LinkedIn/portfolio site blurb using the recruiter-friendly summary.
- Practice the 7 interview answers out loud once, in your own words.
- Push to GitHub with the new repo name; double check no original-repo references remain in commit history if you want a fully clean start (or keep history transparent — your call, but be consistent with what you tell interviewers).
