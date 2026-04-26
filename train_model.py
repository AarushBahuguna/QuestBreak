"""
train_model.py — orchestrator that runs the data pipeline and trains the ML models.

Usage:
    python train_model.py
"""

from data_pipeline import DataPipeline
from ml_classifier import MLClassifier

def run_training(csv_path: str = None):
    # 1) Run pipeline (loads CSV or simulates)
    dp = DataPipeline(data_path=csv_path if csv_path else "genz_mental_wellness_synthetic_dataset.csv")
    out = dp.run_full_pipeline(csv_path=csv_path, simulate_if_missing=True, apply_smote=True)

    X_train = out["X_train"]
    X_test = out["X_test"]
    y_train = out["y_train"]
    y_test = out["y_test"]
    feature_names = out["feature_names"]

    # 2) Train models
    clf = MLClassifier(random_state=42)
    clf.train_all(X_train, y_train, apply_scaling=False)  # pipeline already scaled X_train/X_test

    # 3) Evaluate
    eval_info = clf.evaluate_all(X_test, y_test)

    # 4) Feature importances and save best model
    clf.feature_importance(feature_names)
    clf.save_best_model("models/best_model.joblib")

    # 5) Example prediction on one test sample
    sample = X_test[0]
    prob = clf.predict_craving(sample)
    print(f"[train_model] Example predicted doomscroll probability: {prob:.4f}")

    return clf, eval_info

if __name__ == "__main__":
    run_training()