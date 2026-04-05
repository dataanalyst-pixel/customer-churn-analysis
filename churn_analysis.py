# ============================================================
#  Customer Churn Analysis
#  Author: [Your Name]
#  Tools : Python | Pandas | Matplotlib | Seaborn | Scikit-learn
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, roc_curve, accuracy_score
)
import warnings
warnings.filterwarnings('ignore')

# ── Style ─────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
COLORS = {"churn": "#E74C3C", "no_churn": "#2ECC71", "accent": "#3498DB"}
plt.rcParams.update({'figure.dpi': 150, 'font.family': 'DejaVu Sans'})

# ── 1. LOAD DATA ──────────────────────────────────────────────
print("=" * 55)
print("  CUSTOMER CHURN ANALYSIS")
print("=" * 55)

df = pd.read_csv("data/customer_churn.csv")
print(f"\n✅ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns\n")

# ── 2. EXPLORATORY DATA ANALYSIS (EDA) ────────────────────────
print("─" * 40)
print("📊 SECTION 1 — EDA")
print("─" * 40)

print("\n[1] Dataset Overview:")
print(df.head())
print("\n[2] Data Types & Nulls:")
print(df.info())
print("\n[3] Summary Statistics:")
print(df.describe().round(2))
print("\n[4] Churn Distribution:")
print(df['Churn_Label'].value_counts())
churn_rate = df['Churn'].mean() * 100
print(f"\n⚠️  Overall Churn Rate: {churn_rate:.1f}%")

# ── 3. VISUALIZATIONS ─────────────────────────────────────────
print("\n─" * 40)
print("🎨 SECTION 2 — VISUALIZATIONS")
print("─" * 40)

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle("Customer Churn Analysis — Exploratory Data Analysis",
             fontsize=16, fontweight='bold', y=1.01)

# (a) Churn Distribution Pie
ax = axes[0, 0]
sizes = df['Churn_Label'].value_counts()
colors_pie = [COLORS["no_churn"], COLORS["churn"]]
ax.pie(sizes, labels=sizes.index, autopct='%1.1f%%',
       colors=colors_pie, startangle=90,
       wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax.set_title("Overall Churn Distribution", fontsize=13, fontweight='bold')

# (b) Churn by Contract Type
ax = axes[0, 1]
contract_churn = df.groupby(['Contract', 'Churn_Label']).size().unstack()
contract_churn.plot(kind='bar', ax=ax,
                    color=[COLORS["no_churn"], COLORS["churn"]],
                    edgecolor='white', width=0.6)
ax.set_title("Churn by Contract Type", fontsize=13, fontweight='bold')
ax.set_xlabel("")
ax.set_ylabel("Number of Customers")
ax.tick_params(axis='x', rotation=15)
ax.legend(title="Churn")

# (c) Monthly Charges — Churn vs No Churn
ax = axes[0, 2]
for label, color, name in [("No", COLORS["no_churn"], "No Churn"),
                             ("Yes", COLORS["churn"], "Churn")]:
    data = df[df['Churn_Label'] == label]['MonthlyCharges']
    ax.hist(data, bins=25, alpha=0.6, color=color, label=name, edgecolor='white')
ax.set_title("Monthly Charges Distribution", fontsize=13, fontweight='bold')
ax.set_xlabel("Monthly Charges (₹)")
ax.set_ylabel("Frequency")
ax.legend()

# (d) Satisfaction Score vs Churn
ax = axes[1, 0]
satisfaction_churn = df.groupby(['SatisfactionScore', 'Churn_Label']).size().unstack(fill_value=0)
satisfaction_churn.plot(kind='bar', ax=ax,
                         color=[COLORS["no_churn"], COLORS["churn"]],
                         edgecolor='white', width=0.7)
ax.set_title("Satisfaction Score vs Churn", fontsize=13, fontweight='bold')
ax.set_xlabel("Satisfaction Score (1=Low, 5=High)")
ax.set_ylabel("Number of Customers")
ax.tick_params(axis='x', rotation=0)
ax.legend(title="Churn")

# (e) Tenure Distribution
ax = axes[1, 1]
sns.kdeplot(df[df['Churn_Label'] == 'No']['Tenure'], ax=ax,
            color=COLORS["no_churn"], fill=True, alpha=0.5, label="No Churn")
sns.kdeplot(df[df['Churn_Label'] == 'Yes']['Tenure'], ax=ax,
            color=COLORS["churn"], fill=True, alpha=0.5, label="Churn")
ax.set_title("Customer Tenure vs Churn", fontsize=13, fontweight='bold')
ax.set_xlabel("Tenure (Months)")
ax.set_ylabel("Density")
ax.legend()

# (f) Support Calls vs Churn
ax = axes[1, 2]
calls_churn = df.groupby(['NumSupportCalls', 'Churn_Label']).size().unstack(fill_value=0)
calls_churn.plot(kind='bar', ax=ax,
                  color=[COLORS["no_churn"], COLORS["churn"]],
                  edgecolor='white', width=0.8)
ax.set_title("Support Calls vs Churn", fontsize=13, fontweight='bold')
ax.set_xlabel("Number of Support Calls")
ax.set_ylabel("Number of Customers")
ax.tick_params(axis='x', rotation=0)
ax.legend(title="Churn")

plt.tight_layout()
plt.savefig("visualizations/eda_dashboard.png", bbox_inches='tight', dpi=150)
plt.close()
print("✅ EDA dashboard saved → visualizations/eda_dashboard.png")

# ── 4. CORRELATION HEATMAP ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))
numeric_cols = df.select_dtypes(include='number').drop(columns=['Churn'])
corr = numeric_cols.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdYlGn",
            ax=ax, square=True, linewidths=0.5,
            cbar_kws={"shrink": 0.8})
ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig("visualizations/correlation_heatmap.png", bbox_inches='tight', dpi=150)
plt.close()
print("✅ Correlation heatmap saved → visualizations/correlation_heatmap.png")

# ── 5. MACHINE LEARNING MODEL ─────────────────────────────────
print("\n─" * 40)
print("🤖 SECTION 3 — MACHINE LEARNING")
print("─" * 40)

# Encode categoricals
df_ml = df.copy()
cat_cols = ['Gender', 'Contract', 'InternetService', 'TechSupport', 'PaymentMethod']
le = LabelEncoder()
for col in cat_cols:
    df_ml[col] = le.fit_transform(df_ml[col])

features = ['Age', 'Gender', 'Tenure', 'MonthlyCharges', 'TotalCharges',
            'Contract', 'InternetService', 'TechSupport', 'PaymentMethod',
            'NumSupportCalls', 'SatisfactionScore']
X = df_ml[features]
y = df_ml['Churn']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain size: {len(X_train)} | Test size: {len(X_test)}")

# --- Logistic Regression ---
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)
lr_acc = accuracy_score(y_test, lr_pred)
lr_auc = roc_auc_score(y_test, lr.predict_proba(X_test)[:, 1])

# --- Random Forest ---
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)
rf_auc = roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])

print(f"\n📌 Logistic Regression → Accuracy: {lr_acc:.2%} | AUC: {lr_auc:.3f}")
print(f"📌 Random Forest       → Accuracy: {rf_acc:.2%} | AUC: {rf_auc:.3f}")
print(f"\n📋 Random Forest Classification Report:\n")
print(classification_report(y_test, rf_pred, target_names=['No Churn', 'Churn']))

# ── 6. MODEL VISUALIZATIONS ───────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle("Machine Learning Model Results", fontsize=15, fontweight='bold')

# (a) Confusion Matrix
ax = axes[0]
cm = confusion_matrix(y_test, rf_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
            xticklabels=['No Churn', 'Churn'],
            yticklabels=['No Churn', 'Churn'],
            linewidths=1, linecolor='white')
ax.set_title("Confusion Matrix\n(Random Forest)", fontsize=13, fontweight='bold')
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")

# (b) ROC Curve — both models
ax = axes[1]
for model, name, color in [
    (lr, "Logistic Regression", COLORS["accent"]),
    (rf, "Random Forest", COLORS["churn"])
]:
    fpr, tpr, _ = roc_curve(y_test, model.predict_proba(X_test)[:, 1])
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    ax.plot(fpr, tpr, color=color, lw=2, label=f"{name} (AUC={auc:.3f})")
ax.plot([0, 1], [0, 1], 'k--', lw=1)
ax.fill_between([0, 1], [0, 1], alpha=0.05, color='gray')
ax.set_title("ROC Curve Comparison", fontsize=13, fontweight='bold')
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.legend(loc='lower right')

# (c) Feature Importance
ax = axes[2]
fi = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=True)
colors_bar = [COLORS["churn"] if v > fi.median() else COLORS["accent"] for v in fi]
fi.plot(kind='barh', ax=ax, color=colors_bar, edgecolor='white')
ax.set_title("Feature Importance\n(Random Forest)", fontsize=13, fontweight='bold')
ax.set_xlabel("Importance Score")

# Legend
high = mpatches.Patch(color=COLORS["churn"], label='High Impact')
low  = mpatches.Patch(color=COLORS["accent"], label='Low Impact')
ax.legend(handles=[high, low], loc='lower right')

plt.tight_layout()
plt.savefig("visualizations/model_results.png", bbox_inches='tight', dpi=150)
plt.close()
print("\n✅ Model results saved → visualizations/model_results.png")

# ── 7. BUSINESS INSIGHTS REPORT ───────────────────────────────
print("\n─" * 40)
print("💡 SECTION 4 — BUSINESS INSIGHTS")
print("─" * 40)

top_features = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
contract_churn_rate = df[df['Contract'] == 'Month-to-month']['Churn'].mean() * 100
low_sat_churn_rate  = df[df['SatisfactionScore'] <= 2]['Churn'].mean() * 100
high_calls_churn    = df[df['NumSupportCalls'] >= 5]['Churn'].mean() * 100

report = f"""
╔══════════════════════════════════════════════════════╗
║         CUSTOMER CHURN ANALYSIS — FINAL REPORT       ║
╚══════════════════════════════════════════════════════╝

📌 DATASET     : 1,000 Customers | 14 Features
📌 CHURN RATE  : {churn_rate:.1f}%

── KEY INSIGHTS ────────────────────────────────────────
1. Month-to-month contract customers churn at {contract_churn_rate:.1f}%
   → Recommend long-term contract incentives

2. Customers with satisfaction score ≤ 2 churn at {low_sat_churn_rate:.1f}%
   → Proactive outreach & service improvement needed

3. Customers with 5+ support calls churn at {high_calls_churn:.1f}%
   → Reduce resolution time; improve first-call resolution

4. Top Churn Predictors (ML Model):
"""
for feat, score in top_features.head(5).items():
    report += f"   • {feat:<22} → {score:.4f}\n"

report += f"""
── MODEL PERFORMANCE ───────────────────────────────────
   Logistic Regression  → Accuracy: {lr_acc:.2%} | AUC: {lr_auc:.3f}
   Random Forest        → Accuracy: {rf_acc:.2%} | AUC: {rf_auc:.3f}

── BUSINESS RECOMMENDATIONS ────────────────────────────
   ✅ Target Month-to-month customers with upgrade offers
   ✅ Set up automated alerts for satisfaction score < 3
   ✅ Assign dedicated support reps for high-call customers
   ✅ Offer discounts at months 6, 12 to improve retention

═══════════════════════════════════════════════════════
"""
print(report)
with open("reports/business_insights_report.txt", "w") as f:
    f.write(report)
print("✅ Report saved → reports/business_insights_report.txt")
print("\n🎉 ANALYSIS COMPLETE! Check the 'visualizations/' folder.\n")
