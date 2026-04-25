from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
import numpy as np

class MLClassifier:
    def __init__(self):
        self.models = {
            "Logistic Regression": LogisticRegression(),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier(),
            "SVM": SVC(probability=True, max_iter=1000)
        }
        self.kmeans = KMeans(n_clusters=3, random_state=42)
        self.best_model_name = "Random Forest" # Default
        
    def train_all(self, X_train, y_train):
        print("[MLClassifier] Training supervised models...")
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            print(f"  - Trained {name}")
            
        print("[MLClassifier] Training unsupervised K-Means clustering...")
        self.kmeans.fit(X_train)
        


def evaluate_all(self, X_test, y_test):
    print("\n[MLClassifier] Advanced Model Evaluation:")

    best_score = 0
    best_model = None

    for name, model in self.models.items():
        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, zero_division=0)
        rec = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)
        cm = confusion_matrix(y_test, preds)

        print(f"\n{name}")
        print("-" * 40)
        print(f"Accuracy : {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall   : {rec:.4f}")
        print(f"F1 Score : {f1:.4f}")
        print("Confusion Matrix:")
        print(cm)

        # Select best model based on F1 Score
        if f1 > best_score:
            best_score = f1
            best_model = name

    self.best_model_name = best_model

    print("\n===================================")
    print(f"Selected Best Model: {self.best_model_name}")
    print(f"Best F1 Score: {best_score:.4f}")
    print("===================================")
        
    def feature_importance(self, feature_names):
        if hasattr(self.models[self.best_model_name], "feature_importances_"):
            importances = self.models[self.best_model_name].feature_importances_
            print(f"\n[MLClassifier] Feature Importances ({self.best_model_name}):")
            for name, imp in zip(feature_names, importances):
                print(f"  {name}: {imp:.4f}")
        else:
            print(f"\n[MLClassifier] {self.best_model_name} does not support feature_importances_")

    def predict_craving(self, user_features):
        """Predicts the probability of doomscrolling (craving)"""
        if len(user_features.shape) == 1:
            user_features = user_features.reshape(1, -1)
            
        model = self.models[self.best_model_name]
        prob = model.predict_proba(user_features)[0][1]
        print(f"[MLClassifier] Craving probability predicted: {prob:.2f}")
        return prob
