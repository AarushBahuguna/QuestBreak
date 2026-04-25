from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
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
        print("\n[MLClassifier] Model Evaluation:")
        best_acc = 0
        for name, model in self.models.items():
            preds = model.predict(X_test)
            acc = accuracy_score(y_test, preds)
            print(f"  - {name} Accuracy: {acc:.4f}")
            if acc > best_acc:
                best_acc = acc
                self.best_model_name = name
                
        print(f"-> Selected Best Model: {self.best_model_name}")
        
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
