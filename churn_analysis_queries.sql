-- ============================================================
--  Customer Churn Analysis — SQL Queries
--  Database: customer_churn_db
--  Table   : customers
-- ============================================================

-- ── CREATE TABLE ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS customers (
    CustomerID       VARCHAR(10) PRIMARY KEY,
    Age              INT,
    Gender           VARCHAR(10),
    Tenure           INT,
    MonthlyCharges   DECIMAL(8,2),
    TotalCharges     DECIMAL(10,2),
    Contract         VARCHAR(20),
    InternetService  VARCHAR(20),
    TechSupport      VARCHAR(5),
    PaymentMethod    VARCHAR(30),
    NumSupportCalls  INT,
    SatisfactionScore INT,
    Churn            INT,
    Churn_Label      VARCHAR(5)
);

-- ── QUERY 1: Overall Churn Rate ───────────────────────────────
-- Business Question: What % of our customers are churning?
SELECT
    COUNT(*)                                      AS Total_Customers,
    SUM(Churn)                                    AS Churned_Customers,
    ROUND(AVG(Churn) * 100, 2)                    AS Churn_Rate_Percent
FROM customers;

-- ── QUERY 2: Churn by Contract Type ──────────────────────────
-- Business Question: Which contract types have the most churn?
SELECT
    Contract,
    COUNT(*)                           AS Total_Customers,
    SUM(Churn)                         AS Churned,
    ROUND(AVG(Churn) * 100, 2)         AS Churn_Rate_Percent
FROM customers
GROUP BY Contract
ORDER BY Churn_Rate_Percent DESC;

-- ── QUERY 3: Churn by Satisfaction Score ─────────────────────
-- Business Question: Does satisfaction drive churn?
SELECT
    SatisfactionScore,
    COUNT(*)                           AS Total_Customers,
    SUM(Churn)                         AS Churned,
    ROUND(AVG(Churn) * 100, 2)         AS Churn_Rate_Percent
FROM customers
GROUP BY SatisfactionScore
ORDER BY SatisfactionScore ASC;

-- ── QUERY 4: High-Risk Customers (Priority Alert List) ────────
-- Business Question: Who are our most at-risk customers?
SELECT
    CustomerID,
    Age,
    Contract,
    MonthlyCharges,
    SatisfactionScore,
    NumSupportCalls,
    Tenure
FROM customers
WHERE
    Contract = 'Month-to-month'
    AND SatisfactionScore <= 2
    AND NumSupportCalls >= 3
    AND Churn = 0          -- Still active! Reach out before they leave
ORDER BY SatisfactionScore ASC, NumSupportCalls DESC
LIMIT 20;

-- ── QUERY 5: Revenue at Risk ──────────────────────────────────
-- Business Question: How much monthly revenue will we lose to churn?
SELECT
    ROUND(SUM(MonthlyCharges), 2)      AS Total_Monthly_Revenue,
    ROUND(SUM(CASE WHEN Churn = 1 THEN MonthlyCharges ELSE 0 END), 2)
                                       AS Revenue_Lost_To_Churn,
    ROUND(
        SUM(CASE WHEN Churn = 1 THEN MonthlyCharges ELSE 0 END)
        / SUM(MonthlyCharges) * 100, 2
    )                                  AS Revenue_Loss_Percent
FROM customers;

-- ── QUERY 6: Churn by Internet Service & Tech Support ─────────
SELECT
    InternetService,
    TechSupport,
    COUNT(*)                           AS Total_Customers,
    ROUND(AVG(Churn) * 100, 2)         AS Churn_Rate_Percent
FROM customers
GROUP BY InternetService, TechSupport
ORDER BY Churn_Rate_Percent DESC;

-- ── QUERY 7: Average Tenure of Churned vs Retained ───────────
SELECT
    Churn_Label,
    ROUND(AVG(Tenure), 1)              AS Avg_Tenure_Months,
    ROUND(AVG(MonthlyCharges), 2)      AS Avg_Monthly_Charges,
    ROUND(AVG(SatisfactionScore), 2)   AS Avg_Satisfaction
FROM customers
GROUP BY Churn_Label;

-- ── QUERY 8: Payment Method vs Churn ─────────────────────────
SELECT
    PaymentMethod,
    COUNT(*)                           AS Total_Customers,
    SUM(Churn)                         AS Churned,
    ROUND(AVG(Churn) * 100, 2)         AS Churn_Rate_Percent
FROM customers
GROUP BY PaymentMethod
ORDER BY Churn_Rate_Percent DESC;

-- ── QUERY 9: Support Calls Buckets ───────────────────────────
SELECT
    CASE
        WHEN NumSupportCalls = 0     THEN '0 Calls'
        WHEN NumSupportCalls BETWEEN 1 AND 2 THEN '1-2 Calls'
        WHEN NumSupportCalls BETWEEN 3 AND 5 THEN '3-5 Calls'
        ELSE '6+ Calls'
    END                                AS Call_Bucket,
    COUNT(*)                           AS Total_Customers,
    ROUND(AVG(Churn) * 100, 2)         AS Churn_Rate_Percent
FROM customers
GROUP BY Call_Bucket
ORDER BY Churn_Rate_Percent DESC;

-- ── QUERY 10: Monthly Cohort Retention Simulation ─────────────
-- Customers grouped by tenure milestones
SELECT
    CASE
        WHEN Tenure < 12  THEN '< 1 Year'
        WHEN Tenure < 24  THEN '1-2 Years'
        WHEN Tenure < 36  THEN '2-3 Years'
        ELSE '3+ Years'
    END                                AS Tenure_Group,
    COUNT(*)                           AS Total_Customers,
    SUM(Churn)                         AS Churned,
    ROUND(AVG(Churn) * 100, 2)         AS Churn_Rate_Percent
FROM customers
GROUP BY Tenure_Group
ORDER BY Churn_Rate_Percent DESC;
