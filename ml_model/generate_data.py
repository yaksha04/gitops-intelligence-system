"""
STEP 3: Generate fake deployment training data
Run: python ml_model/generate_data.py
"""
import pandas as pd
import numpy as np
import sqlite3
import os

os.makedirs('data', exist_ok=True)
np.random.seed(42)
n = 1000

print("Generating 1000 fake deployment records...")

data = {
    'files_changed':          np.random.randint(1, 50, n),
    'lines_added':            np.random.randint(1, 800, n),
    'lines_deleted':          np.random.randint(0, 400, n),
    'hour_of_day':            np.random.randint(0, 24, n),
    'day_of_week':            np.random.randint(0, 7, n),
    'days_since_last_deploy': np.random.randint(0, 30, n),
    'recent_failures':        np.random.randint(0, 5, n),
    'test_pass_rate':         np.random.uniform(0.5, 1.0, n),
    'is_main_branch':         np.random.randint(0, 2, n),
    'num_contributors':       np.random.randint(1, 10, n),
}

df = pd.DataFrame(data)

risk_score = (
    (df['files_changed'] > 20).astype(int) * 2 +
    (df['lines_added'] > 400).astype(int) * 2 +
    (df['day_of_week'] == 4).astype(int) * 2 +
    (df['hour_of_day'] >= 18).astype(int) * 1 +
    (df['recent_failures'] >= 2).astype(int) * 3 +
    (df['test_pass_rate'] < 0.75).astype(int) * 3 +
    (df['days_since_last_deploy'] > 14).astype(int) * 1
)

df['deployment_failed'] = (risk_score >= 5).astype(int)
df.to_csv('data/deployments.csv', index=False)

conn = sqlite3.connect('data/deployments.db')
df.to_sql('deployments', conn, if_exists='replace', index=False)
conn.close()

print(f"CSV saved: data/deployments.csv")
print(f"SQLite saved: data/deployments.db")
print(f"Total records: {n}")
print(f"Failure rate: {df['deployment_failed'].mean():.1%}")
print("Done! Now run: python ml_model/train.py")
