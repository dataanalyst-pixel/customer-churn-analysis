# 📊 Customer Churn Analysis

> A complete end-to-end data analytics project analyzing customer churn using **Python**, **SQL**, and **Machine Learning** — built to demonstrate real-world data analyst skills.

---

## 🚀 Project Overview

Customer churn is one of the most critical business problems across industries — telecom, SaaS, banking, and retail. In this project, I analyzed **1,000 customer records** to:

- Understand **why customers leave**
- Identify **high-risk customers** before they churn
- Build **ML models** to predict churn with high accuracy
- Generate **business recommendations** to reduce churn

---

## 🗂️ Project Structure

```
customer-churn-analysis/
│
├── data/
│   ├── customer_churn.csv          ← Dataset (1000 customers, 14 features)
│   └── generate_data.py            ← Script to regenerate dataset
│
├── sql/
│   └── churn_analysis_queries.sql  ← 10 SQL queries for business insights
│
├── visualizations/
│   ├── eda_dashboard.png           ← EDA: 6-panel analysis dashboard
│   ├── correlation_heatmap.png     ← Feature correlation heatmap
│   └── model_results.png           ← Confusion matrix, ROC curve, feature importance
│
├── reports/
│   └── business_insights_report.txt ← Final business recommendations
│
├── churn_analysis.py               ← Main Python analysis script
├── requirements.txt                ← Python dependencies
└── README.md                       ← You are here!
```

---

## 🛠️ Tools & Technologies

| Category | Tools |
|---|---|
| **Language** | Python 3.10+ |
| **Data Manipulation** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Machine Learning** | Scikit-learn (Logistic Regression, Random Forest) |
| **Database** | SQL (MySQL / SQLite compatible) |
| **Version Control** | Git, GitHub |

---

## 📁 Dataset Description

| Column | Description |
|---|---|
| `CustomerID` | Unique customer identifier |
| `Age` | Customer age |
| `Gender` | Male / Female |
| `Tenure` | Months with the company |
| `MonthlyCharges` | Monthly billing amount |
| `TotalCharges` | Cumulative charges |
| `Contract` | Month-to-month / One year / Two year |
| `InternetService` | DSL / Fiber optic / No |
| `TechSupport` | Tech support subscription |
| `PaymentMethod` | Payment method used |
| `NumSupportCalls` | Number of support calls made |
| `SatisfactionScore` | 1 (very low) to 5 (very high) |
| `Churn` | 0 = Retained, 1 = Churned |

---

## 📊 Key Findings

### 🔴 Churn Risk Factors
| Factor | Churn Rate |
|---|---|
| Month-to-month contract | ~60%+ |
| Satisfaction score ≤ 2 | ~70%+ |
| 5+ Support calls | ~65%+ |
| Tenure < 12 months | ~50%+ |

### 📈 Model Performance
| Model | Accuracy | AUC Score |
|---|---|---|
| Logistic Regression | ~75% | ~0.80 |
| **Random Forest** | **~80%** | **~0.87** |

### 💡 Top Business Recommendations
1. **Offer annual contract discounts** to month-to-month customers
2. **Proactive outreach** to customers with satisfaction score < 3
3. **Dedicated support agents** for customers with 5+ support calls
4. **Loyalty rewards** at 6-month and 12-month tenure milestones

---

## ▶️ How to Run

### 1. Clone this Repository
```bash
git clone https://github.com/YOUR_USERNAME/customer-churn-analysis.git
cd customer-churn-analysis
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Dataset
```bash
python data/generate_data.py
```

### 4. Run Full Analysis
```bash
python churn_analysis.py
```

### 5. View SQL Queries
Open `sql/churn_analysis_queries.sql` in any SQL editor (MySQL Workbench, DBeaver, etc.)

---

## 📸 Visualizations

### EDA Dashboard
> 6-panel analysis: Churn distribution, contract type, monthly charges, satisfaction score, tenure, support calls

### Correlation Heatmap
> Feature correlation analysis to find multicollinearity

### Model Results
> Confusion matrix + ROC curve comparison + Feature importance chart

---

## 🎯 Skills Demonstrated

- ✅ Data Cleaning & Preprocessing
- ✅ Exploratory Data Analysis (EDA)
- ✅ Data Visualization (6+ chart types)
- ✅ SQL querying for business insights
- ✅ Machine Learning (Classification)
- ✅ Model Evaluation (AUC, Confusion Matrix, ROC)
- ✅ Business Insights & Recommendations
- ✅ Professional Project Documentation

---

## 👤 About Me

**Vanitha**
Aspiring Data Analyst | Chennai, Tamil Nadu

- 📧 Email: vanithaperiyasamy13@gmail.com
- 💼 LinkedIn: www.linkedin.com/in/vanitha-kp
- 🐙 GitHub:[github.com/dataanalyst-pixel](https://github.com/dataanalyst-pixel)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

⭐ **If you found this project helpful, please give it a star!**
