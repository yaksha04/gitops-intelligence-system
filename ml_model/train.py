"""
STEP 4: Train the ML risk prediction model
Run: python ml_model/train.py
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

os.makedirs('ml_model', exist_ok=True)
os.makedirs('data', exist_ok=True)

print("Training Deployment Risk Predictor...")
print("=" * 50)

df = pd.read_csv('data/deployments.csv')

FEATURES = [
    'files_changed', 'lines_added', 'lines_deleted',
    'hour_of_day', 'day_of_week', 'days_since_last_deploy',
    'recent_failures', 'test_pass_rate', 'is_main_branch',
    'num_contributors'
]

X = df[FEATURES]
y = df['deployment_failed']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training samples : {len(X_train)}")
print(f"Test samples     : {len(X_test)}")
print("\nTraining model (this takes a few seconds)...")

model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel trained successfully!")
print(f"Accuracy : {accuracy:.2%}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Safe Deploy', 'Failed Deploy']))

# Save feature importance
importance_df = pd.DataFrame({
    'feature': FEATURES,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

importance_df.to_csv('data/feature_importance.csv', index=False)
print("\nTop Risk Factors:")
print(importance_df.to_string(index=False))

# Save model
joblib.dump(model, 'ml_model/model.pkl')
print("\nModel saved: ml_model/model.pkl")
print("Next step: streamlit run dashboard/app.py")
