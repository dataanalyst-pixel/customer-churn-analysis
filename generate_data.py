import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000

data = {
    'CustomerID': [f'CUST{str(i).zfill(4)}' for i in range(1, n+1)],
    'Age': np.random.randint(18, 70, n),
    'Gender': np.random.choice(['Male', 'Female'], n),
    'Tenure': np.random.randint(1, 72, n),
    'MonthlyCharges': np.round(np.random.uniform(20, 120, n), 2),
    'TotalCharges': np.round(np.random.uniform(100, 8000, n), 2),
    'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n, p=[0.5, 0.3, 0.2]),
    'InternetService': np.random.choice(['DSL', 'Fiber optic', 'No'], n, p=[0.4, 0.4, 0.2]),
    'TechSupport': np.random.choice(['Yes', 'No'], n),
    'PaymentMethod': np.random.choice(
        ['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'], n
    ),
    'NumSupportCalls': np.random.randint(0, 10, n),
    'SatisfactionScore': np.random.randint(1, 6, n),
}

# Churn logic: realistic probabilities
churn_prob = (
    (np.array(data['Contract']) == 'Month-to-month') * 0.3 +
    (np.array(data['SatisfactionScore']) <= 2) * 0.4 +
    (np.array(data['NumSupportCalls']) >= 5) * 0.2 +
    (np.array(data['Tenure']) < 12) * 0.1
)
churn_prob = np.clip(churn_prob, 0, 1)
data['Churn'] = (np.random.rand(n) < churn_prob).astype(int)
data['Churn_Label'] = ['Yes' if c == 1 else 'No' for c in data['Churn']]

df = pd.DataFrame(data)
df.to_csv('customer_churn.csv', index=False)
print(f"Dataset created: {len(df)} rows")
print(df['Churn_Label'].value_counts())
print(df.head())
