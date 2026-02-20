import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import os

def train():
    # 1. Load Data
    data_path = 'data/Training.csv'
    print(f"Loading data from {data_path}...")
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Could not find {data_path}")

    df = pd.read_csv(data_path)

    X = df.drop('prognosis', axis=1)
    y = df['prognosis']

    # 2. Train-Test Split (Optional for final model but good for metrics)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Train Model
    print("Training Decision Tree Classifier...")
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # 4. Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Model Accuracy: {acc:.4f}")

    # 5. Save Artifacts
    os.makedirs('models', exist_ok=True)
    
    model_path = 'models/doctor_model.joblib'
    symptom_path = 'models/symptom_list.joblib'

    print(f"Saving model to {model_path}...")
    joblib.dump(model, model_path)
    
    print(f"Saving symptom list to {symptom_path}...")
    joblib.dump(X.columns.tolist(), symptom_path)

    print("✅ Training Complete & Models Saved!")

if __name__ == "__main__":
    train()
