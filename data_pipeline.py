"""
data_pipeline.py — DataPipeline for loading, cleaning, feature-engineering and splitting.

This version is tolerant of the provided CSV header (Age, Gender, Country, ..., Burnout_Risk, etc.)
and maps those columns into the canonical features used by the ML pipeline:

- session_duration_mins (from Screen_Time_Hours)
- quests_completed (from Motivation_Level)
- login_hour (from Night_Scrolling_Frequency)
- streak_days (proxy if missing)
- doomscroll_triggered (from Burnout_Risk)

It saves processed arrays and feature names to data/processed and returns train/test splits
(scale is applied inside split_and_scale).
"""

import json
import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Optional SMOTE
try:
    from imblearn.over_sampling import SMOTE  # type: ignore
    HAS_SMOTE = True
except Exception:
    HAS_SMOTE = False


class DataPipeline:
    def __init__(self, data_path: str = "genz_mental_wellness_synthetic_dataset.csv"):
        self.data_path = data_path
        self.scaler: Optional[StandardScaler] = None

    def simulate_data(self, n_users: int = 500, n_days: int = 30, seed: int = 42) -> pd.DataFrame:
        np.random.seed(seed)
        n_records = n_users * n_days

        user_ids = np.repeat(np.arange(1, n_users + 1), n_days)
        dates = np.tile(pd.date_range("2024-01-01", periods=n_days), n_users)
        session_duration = np.random.exponential(scale=25, size=n_records)
        quests_completed = np.random.poisson(lam=3, size=n_records)
        login_hour = np.random.randint(0, 24, size=n_records)
        streak_days = np.clip(np.random.geometric(p=0.1, size=n_records), 1, 60)

        doomscroll_prob = (
            0.05
            + 0.30 * ((login_hour >= 22) | (login_hour <= 4)).astype(float)
            + 0.20 * (quests_completed == 0).astype(float)
            - 0.10 * (streak_days > 7).astype(float)
        ).clip(0, 1)

        doomscroll_triggered = np.random.binomial(1, doomscroll_prob)

        df = pd.DataFrame({
            "user_id": user_ids,
            "date": dates,
            "session_duration_mins": np.round(session_duration, 2),
            "quests_completed": quests_completed,
            "login_hour": login_hour,
            "streak_days": streak_days,
            "doomscroll_triggered": doomscroll_triggered
        })
        return df

    def load_csv(self, csv_path: Optional[str] = None) -> pd.DataFrame:
        path = csv_path or self.data_path
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset not found at: {path}")
        df = pd.read_csv(path)
        print(f"[DataPipeline] Loaded CSV: {path}, rows: {len(df)}")
        return df

    def clean_and_engineer(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize headers from the provided CSV, coerce numeric types, create canonical columns,
        and add engineered features required by the ML models.
        """
        import numpy as _np

        df = df.copy()
        df = df.drop_duplicates()
        df = df.dropna(how="all")  # drop rows that are fully empty

        # --- Direct mappings from common header variants to canonical names ---
        # If the CSV already has canonical columns, this will be a no-op.
        # Map Screen_Time_Hours -> session_duration_mins (hours -> minutes)
        if "Screen_Time_Hours" in df.columns and "session_duration_mins" not in df.columns:
            df["session_duration_mins"] = pd.to_numeric(df["Screen_Time_Hours"], errors="coerce") * 60.0

        # Map Motivation_Level -> quests_completed
        if "Motivation_Level" in df.columns and "quests_completed" not in df.columns:
            df["quests_completed"] = pd.to_numeric(df["Motivation_Level"], errors="coerce")

        # Map Night_Scrolling_Frequency -> login_hour (heuristic)
        if "Night_Scrolling_Frequency" in df.columns and "login_hour" not in df.columns:
            nsf = pd.to_numeric(df["Night_Scrolling_Frequency"], errors="coerce")
            # If values fall in 0-23, assume they are hours
            if not nsf.dropna().empty and nsf.dropna().between(0, 23).all():
                df["login_hour"] = nsf
            else:
                # Map frequency into a late-night hour range [20, 24]
                valid = nsf.fillna(nsf.mean() if not nsf.dropna().empty else 0.0)
                vmin, vmax = valid.min(), valid.max()
                if vmax == vmin:
                    df["login_hour"] = 22.0
                else:
                    scaled = (valid - vmin) / (vmax - vmin)
                    df["login_hour"] = 20.0 + scaled * 4.0

        # Map Burnout_Risk -> doomscroll_triggered (target)
        if "Burnout_Risk" in df.columns and "doomscroll_triggered" not in df.columns:
            br = df["Burnout_Risk"].astype(str).str.strip()
            # Try numeric first
            numeric_br = pd.to_numeric(df["Burnout_Risk"], errors="coerce")
            if numeric_br.notna().any():
                # Interpret numeric > 0.5 (or > 50 if it's a percent) as positive
                # Normalize if values > 1 (assume percent)
                if numeric_br.max() > 1.0:
                    df["doomscroll_triggered"] = (numeric_br / 100.0 > 0.5).astype(int)
                else:
                    df["doomscroll_triggered"] = (numeric_br > 0.5).astype(int)
            else:
                # Fallback: textual mapping, e.g., "High" -> 1, else 0
                df["doomscroll_triggered"] = (br.str.lower() == "high").astype(int)

        # If streak_days not present, create a proxy using Daily_Social_Media_Hours if available
        if "streak_days" not in df.columns:
            if "Daily_Social_Media_Hours" in df.columns:
                dsm = pd.to_numeric(df["Daily_Social_Media_Hours"], errors="coerce").fillna(0.0)
                proxy = (30.0 - dsm).round().astype(int)
                proxy = _np.clip(proxy, 1, 30)
                df["streak_days"] = proxy
            else:
                df["streak_days"] = 1  # conservative fallback

        # --- Coerce numeric types for canonical core columns ---
        for col in ["session_duration_mins", "quests_completed", "login_hour", "streak_days", "doomscroll_triggered"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Drop rows missing mandatory canonical columns (if any exist)
        mandatory = [c for c in ["session_duration_mins", "quests_completed", "login_hour", "streak_days", "doomscroll_triggered"] if c in df.columns]
        if mandatory:
            df = df.dropna(subset=mandatory)

        # Clip & transform session duration
        if "session_duration_mins" in df.columns:
            df["session_duration_mins"] = df["session_duration_mins"].clip(lower=0, upper=1440)
            df["session_duration_mins"] = _np.log1p(df["session_duration_mins"])

        # Engineered features (safe guards for missing columns)
        safe_duration = df.get("session_duration_mins", pd.Series(1, index=df.index)).replace(0, 1)
        quests_series = df.get("quests_completed", pd.Series(0, index=df.index)).fillna(0)
        streak_series = df.get("streak_days", pd.Series(1, index=df.index)).fillna(1)
        login_series = df.get("login_hour", pd.Series(0, index=df.index)).fillna(0)

        df["hourly_intensity"] = (quests_series / (safe_duration / 60)).replace([_np.inf, -_np.inf], 0).fillna(0)
        df["quest_overdue_flag"] = ((streak_series > 3) & (quests_series == 0)).astype(int)
        df["late_night_flag"] = ((login_series >= 22) | (login_series <= 4)).astype(int)

        return df

    def split_and_scale(
        self,
        df: pd.DataFrame,
        feature_cols: Optional[List[str]] = None,
        test_size: float = 0.2,
        random_state: int = 42,
        apply_smote: bool = True
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[str], Optional[StandardScaler]]:
        default_features = [
            "session_duration_mins",
            "quests_completed",
            "login_hour",
            "streak_days",
            "hourly_intensity",
            "quest_overdue_flag",
            "late_night_flag",
        ]
        present_features = [c for c in (feature_cols or default_features) if c in df.columns]
        if "doomscroll_triggered" not in df.columns:
            raise KeyError("Target column 'doomscroll_triggered' not found in DataFrame.")

        X = df[present_features].values
        y = df["doomscroll_triggered"].astype(int).values

        stratify = y if len(np.unique(y)) > 1 else None
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, stratify=stratify, random_state=random_state
        )

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        self.scaler = scaler

        if apply_smote and HAS_SMOTE and len(np.unique(y_train)) > 1:
            try:
                sm = SMOTE(random_state=random_state)
                X_train, y_train = sm.fit_resample(X_train, y_train)
                print("[DataPipeline] Applied SMOTE to training set.")
            except Exception:
                pass

        return X_train, X_test, y_train, y_test, present_features, scaler

    def save_processed(self, X: np.ndarray, y: np.ndarray, out_dir: str = "data/processed") -> None:
        os.makedirs(out_dir, exist_ok=True)
        np.save(os.path.join(out_dir, "X.npy"), X)
        np.save(os.path.join(out_dir, "y.npy"), y)
        print(f"[DataPipeline] Saved processed arrays to {out_dir}")

    def save_feature_names(self, feature_names: List[str], out_dir: str = "data/processed") -> None:
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "feature_names.json"), "w", encoding="utf-8") as f:
            json.dump(feature_names, f)
        print(f"[DataPipeline] Saved feature names to {out_dir}/feature_names.json")

    def run_full_pipeline(
        self,
        csv_path: Optional[str] = None,
        simulate_if_missing: bool = True,
        apply_smote: bool = True,
        out_dir: str = "data/processed"
    ) -> Dict[str, object]:
        try:
            df = self.load_csv(csv_path) if (csv_path or os.path.exists(self.data_path)) else None
            if df is None:
                raise FileNotFoundError()
        except FileNotFoundError:
            if simulate_if_missing:
                df = self.simulate_data()
                print("[DataPipeline] CSV not found — using synthetic data.")
            else:
                raise

        df = self.clean_and_engineer(df)
        X_train, X_test, y_train, y_test, feature_names, scaler = self.split_and_scale(
            df, apply_smote=apply_smote
        )

        # Save processed arrays (train+test as full arrays for convenience)
        full_X = np.vstack([X_train, X_test])
        full_y = np.concatenate([y_train, y_test])
        self.save_processed(full_X, full_y, out_dir=out_dir)
        self.save_feature_names(feature_names, out_dir=out_dir)

        return {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test,
            "feature_names": feature_names,
            "scaler": scaler,
            "processed_dir": out_dir
        }


if __name__ == "__main__":
    dp = DataPipeline()
    out = dp.run_full_pipeline(simulate_if_missing=True, apply_smote=True)
    print(f"[DataPipeline] Finished. Features: {out['feature_names']}. Train samples: {out['X_train'].shape[0]}")