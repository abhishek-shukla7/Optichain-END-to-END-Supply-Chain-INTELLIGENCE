/* =========================================================
   01_schema_and_load.sql
   Normalize the flat CSV into a star schema in SQL Server.
   ========================================================= */

CREATE TABLE dim_supplier (
    SupplierID          INT PRIMARY KEY,
    SupplierName         VARCHAR(100),
    SupplierAddress       VARCHAR(200),
    SupplierContactDetails VARCHAR(50)
);

CREATE TABLE dim_car (
    ProductID    INT PRIMARY KEY,
    CarMaker      VARCHAR(50),
    CarModel       VARCHAR(50),
    CarColor       VARCHAR(30),
    CarModelYear  INT,
    CarPrice       DECIMAL(12,2)
);

CREATE TABLE dim_customer (
    CustomerID       VARCHAR(20) PRIMARY KEY,
    CustomerName      VARCHAR(100),
    Gender             VARCHAR(10),
    JobTitle           VARCHAR(100),
    PhoneNumber        VARCHAR(20),
    EmailAddress        VARCHAR(100),
    City                VARCHAR(50),
    State               VARCHAR(50),
    Country             VARCHAR(50),
    CountryCode         VARCHAR(5),
    CustomerAddress      VARCHAR(200),
    PostalCode           VARCHAR(10)
);

CREATE TABLE dim_date (
    DateKey   INT PRIMARY KEY,    -- yyyymmdd
    [Date]    DATE,
    [Year]    INT,
    [Quarter] INT,
    [Month]   INT,
    MonthName VARCHAR(15),
    [Day]     INT,
    Weekday    VARCHAR(15)
);

CREATE TABLE fact_orders (
    OrderID          VARCHAR(20) PRIMARY KEY,
    CustomerID       VARCHAR(20) FOREIGN KEY REFERENCES dim_customer(CustomerID),
    ProductID        INT          FOREIGN KEY REFERENCES dim_car(ProductID),
    SupplierID       INT          FOREIGN KEY REFERENCES dim_supplier(SupplierID),
    OrderDateKey     INT          FOREIGN KEY REFERENCES dim_date(DateKey),
    ShipDateKey      INT          FOREIGN KEY REFERENCES dim_date(DateKey),
    ShipMode         VARCHAR(20),
    Shipping         VARCHAR(20),  -- Truck / Air
    Sales            DECIMAL(12,2),
    Quantity         INT,
    Discount         DECIMAL(4,2),
    CreditCardType   VARCHAR(40),
    CustomerFeedback VARCHAR(15)
);

-- Load via SSIS / BULK INSERT / Power Query from data/processed/*.csv
-- (produced by python/01_data_cleaning.py)


/* =========================================================
   02_joins_and_views.sql
   ========================================================= */

-- Full order detail (4-way join) — base view feeding most dashboard visuals
CREATE VIEW vw_order_detail AS
SELECT
    f.OrderID,
    d.[Date]               AS OrderDate,
    c.CustomerName, c.Gender, c.City, c.State,
    car.CarMaker, car.CarModel, car.CarColor, car.CarModelYear,
    s.SupplierName,
    f.ShipMode, f.Shipping, f.Sales, f.Quantity, f.Discount,
    f.CustomerFeedback
FROM fact_orders f
JOIN dim_customer c ON f.CustomerID = c.CustomerID
JOIN dim_car      car ON f.ProductID = car.ProductID
JOIN dim_supplier s   ON f.SupplierID = s.SupplierID
JOIN dim_date     d   ON f.OrderDateKey = d.DateKey;

-- Revenue by supplier (inner join + aggregation)
SELECT s.SupplierName,
       COUNT(f.OrderID)        AS TotalOrders,
       SUM(f.Sales)            AS TotalRevenue,
       AVG(f.Discount)         AS AvgDiscount
FROM fact_orders f
JOIN dim_supplier s ON f.SupplierID = s.SupplierID
GROUP BY s.SupplierName
ORDER BY TotalRevenue DESC;

-- Customers with below-average feedback (LEFT JOIN to catch zero-order edge case)
SELECT c.CustomerName, f.OrderID, f.CustomerFeedback
FROM dim_customer c
LEFT JOIN fact_orders f ON c.CustomerID = f.CustomerID
WHERE f.CustomerFeedback IN ('Bad','Very Bad');


/* =========================================================
   03_ctes_and_kpis.sql
   ========================================================= */

-- CTE: monthly revenue, then rank months by performance
WITH monthly_sales AS (
    SELECT d.[Year], d.[Month],
           SUM(f.Sales) AS MonthlyRevenue,
           COUNT(f.OrderID) AS MonthlyOrders
    FROM fact_orders f
    JOIN dim_date d ON f.OrderDateKey = d.DateKey
    GROUP BY d.[Year], d.[Month]
)
SELECT *,
       RANK() OVER (ORDER BY MonthlyRevenue DESC) AS RevenueRank
FROM monthly_sales;

-- CTE: top supplier per car maker (one analytical question, cleanly composed)
WITH supplier_maker_sales AS (
    SELECT car.CarMaker, s.SupplierName, SUM(f.Sales) AS Revenue
    FROM fact_orders f
    JOIN dim_car car ON f.ProductID = car.ProductID
    JOIN dim_supplier s ON f.SupplierID = s.SupplierID
    GROUP BY car.CarMaker, s.SupplierName
),
ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY CarMaker ORDER BY Revenue DESC) AS rn
    FROM supplier_maker_sales
)
SELECT CarMaker, SupplierName, Revenue
FROM ranked
WHERE rn = 1;

-- KPI: On-time delivery rate proxy and avg lead time by ShipMode
SELECT f.ShipMode,
       COUNT(*) AS Orders,
       AVG(DATEDIFF(DAY, od.[Date], sd.[Date])) AS AvgLeadTimeDays,
       SUM(CASE WHEN DATEDIFF(DAY, od.[Date], sd.[Date]) < 0 THEN 1 ELSE 0 END) AS DataQualityFlag_NegativeLeadTime
FROM fact_orders f
JOIN dim_date od ON f.OrderDateKey = od.DateKey
JOIN dim_date sd ON f.ShipDateKey  = sd.DateKey
GROUP BY f.ShipMode;

-- KPI: Average Order Value and Discount impact
SELECT
    AVG(Sales)                                  AS AvgOrderValue,
    AVG(Discount)                                AS AvgDiscount,
    SUM(Sales * Quantity)                        AS GrossRevenue
FROM fact_orders;


/* =========================================================
   04_window_functions.sql
   ========================================================= */

-- Running total of revenue over time (cumulative trend)
SELECT d.[Date], f.Sales,
       SUM(f.Sales) OVER (ORDER BY d.[Date] ROWS UNBOUNDED PRECEDING) AS RunningRevenue
FROM fact_orders f
JOIN dim_date d ON f.OrderDateKey = d.DateKey;

-- Month-over-month revenue growth using LAG
WITH monthly AS (
    SELECT d.[Year], d.[Month], SUM(f.Sales) AS Revenue
    FROM fact_orders f
    JOIN dim_date d ON f.OrderDateKey = d.DateKey
    GROUP BY d.[Year], d.[Month]
)
SELECT [Year], [Month], Revenue,
       LAG(Revenue) OVER (ORDER BY [Year], [Month]) AS PrevMonthRevenue,
       ROUND(
         100.0 * (Revenue - LAG(Revenue) OVER (ORDER BY [Year], [Month]))
         / NULLIF(LAG(Revenue) OVER (ORDER BY [Year], [Month]), 0), 2
       ) AS MoM_Growth_Pct
FROM monthly;

-- Customer revenue rank + percentile (segmentation input for Power BI)
SELECT c.CustomerName,
       SUM(f.Sales) AS TotalSpend,
       NTILE(4) OVER (ORDER BY SUM(f.Sales) DESC) AS SpendQuartile,
       RANK() OVER (ORDER BY SUM(f.Sales) DESC) AS SpendRank
FROM fact_orders f
JOIN dim_customer c ON f.CustomerID = c.CustomerID
GROUP BY c.CustomerName;

-- Top 3 highest-sale orders per supplier (ranking within group)
SELECT *
FROM (
    SELECT s.SupplierName, f.OrderID, f.Sales,
           DENSE_RANK() OVER (PARTITION BY s.SupplierName ORDER BY f.Sales DESC) AS rnk
    FROM fact_orders f
    JOIN dim_supplier s ON f.SupplierID = s.SupplierID
) t
WHERE rnk <= 3;
