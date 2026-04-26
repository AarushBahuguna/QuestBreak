"""
ml_classifier.py — ML training/evaluation utilities.

Contains MLClassifier (train_all, evaluate_all, feature_importance, predict_craving, save_best_model).
This file does NOT run training by itself — use train_model.py to run the full pipeline.
"""

import os
from typing import List, Optional

import joblib
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

class MLClassifier:
    def __init__(self, random_state: int = 42):
        self.models = {
            "Logistic Regression": LogisticRegression(max_iter=2000, random_state=random_state),
            "Decision Tree": DecisionTreeClassifier(random_state=random_state),
            "Random Forest": RandomForestClassifier(n_estimators=100, random_state=random_state),
            "SVM": SVC(probability=True, max_iter=5000, random_state=random_state),
        }
        self.kmeans = KMeans(n_clusters=3, random_state=random_state)
        self.best_model_name: Optional[str] = None
        self.scaler: Optional[StandardScaler] = None

    def train_all(self, X_train: np.ndarray, y_train: np.ndarray, apply_scaling: bool = True):
        """
        Train all supervised models and the KMeans clustering model.
        If apply_scaling is True, fit and store a StandardScaler on training data.
        """
        if apply_scaling:
            self.scaler = StandardScaler()
            X_train = self.scaler.fit_transform(X_train)
            print("[MLClassifier] Fitted StandardScaler on training data.")

        print("[MLClassifier] Training supervised models...")
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            print(f"  - Trained {name}")

        print("[MLClassifier] Training K-Means (unsupervised)...")
        self.kmeans.fit(X_train)

    def evaluate_all(self, X_test: np.ndarray, y_test: np.ndarray):
        """
        Evaluate all supervised models on test data and pick best by F1 score.
        Returns a dict with per-model metrics and the selected best model.
        """
        if self.scaler is not None:
            X_test_eval = self.scaler.transform(X_test)
        else:
            X_test_eval = X_test

        print("\n[MLClassifier] Advanced Model Evaluation:")
        results = {}
        best_score = -1.0
        best_model = None

        for name, model in self.models.items():
            preds = model.predict(X_test_eval)
            acc = accuracy_score(y_test, preds)
            prec = precision_score(y_test, preds, zero_division=0)
            rec = recall_score(y_test, preds, zero_division=0)
            f1 = f1_score(y_test, preds, zero_division=0)
            cm = confusion_matrix(y_test, preds)

            results[name] = {
                "accuracy": acc,
                "precision": prec,
                "recall": rec,
                "f1": f1,
                "confusion_matrix": cm.tolist(),
            }

            print(f"\n{name}")
            print("-" * 40)
            print(f"Accuracy : {acc:.4f}")
            print(f"Precision: {prec:.4f}")
            print(f"Recall   : {rec:.4f}")
            print(f"F1 Score : {f1:.4f}")
            print("Confusion Matrix:")
            print(cm)

            if f1 > best_score:
                best_score = f1
                best_model = name

        self.best_model_name = best_model or next(iter(self.models.keys()))
        print("\n===================================")
        print(f"Selected Best Model: {self.best_model_name}")
        print(f"Best F1 Score: {best_score:.4f}")
        print("===================================")
        return {"results": results, "best_model": self.best_model_name, "best_f1": best_score}

    def feature_importance(self, feature_names: List[str]):
        """
        Print feature importances if the chosen model supports them.
        """
        if self.best_model_name is None:
            print("[MLClassifier] No best model selected yet.")
            return

        model = self.models[self.best_model_name]
        if hasattr(model, "feature_importances_"):
            importances = getattr(model, "feature_importances_")
            print(f"\n[MLClassifier] Feature Importances ({self.best_model_name}):")
            for name, imp in zip(feature_names, importances):
                print(f"  {name}: {imp:.4f}")
        else:
            print(f"\n[MLClassifier] {self.best_model_name} does not support feature_importances_")

    def predict_craving(self, user_features: np.ndarray) -> float:
        """
        Predict positive-class probability for given features (1D or 2D array).
        Requires that evaluate_all has selected a best model first.
        """
        if self.best_model_name is None:
            raise RuntimeError("Best model is not selected. Run evaluate_all() first.")

        model = self.models[self.best_model_name]
        if user_features.ndim == 1:
            user_features = user_features.reshape(1, -1)

        if self.scaler is not None:
            user_features = self.scaler.transform(user_features)

        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(user_features)
            prob = float(probs[0, 1]) if probs.shape[1] == 2 else float(np.max(probs[0]))
        elif hasattr(model, "decision_function"):
            score = model.decision_function(user_features)[0]
            prob = 1.0 / (1.0 + np.exp(-score))
        else:
            pred = model.predict(user_features)[0]
            prob = float(pred)

        print(f"[MLClassifier] Craving probability predicted: {prob:.4f}")
        return prob

    def save_best_model(self, path: str = "models/best_model.joblib"):
        """
        Save the selected best model and scaler (if present).
        """
        if self.best_model_name is None:
            raise RuntimeError("No best model selected to save.")
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        model = self.models[self.best_model_name]
        joblib.dump({"model": model}, path)
        if self.scaler is not None:
            joblib.dump(self.scaler, os.path.join(os.path.dirname(path), "scaler.joblib"))
        print(f"[MLClassifier] Saved best model ({self.best_model_name}) to {path}")