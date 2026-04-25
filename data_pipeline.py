import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import os

class DataPipeline:
    def __init__(self, data_path="genz_mental_wellness_synthetic_dataset.csv"):
        self.data_path = data_path
        self.scaler = None
        
    def simulate_data(self, n_users=500, n_days=30, seed=42) -> pd.DataFrame:
        np.random.seed(seed)
        n_records = n_users * n_days

        user_ids         = np.repeat(np.arange(1, n_users + 1), n_days)
        dates            = np.tile(pd.date_range("2024-01-01", periods=n_days), n_users)
        session_duration = np.random.exponential(scale=25, size=n_records)
        quests_completed = np.random.poisson(lam=3, size=n_records)
        login_hour       = np.random.randint(0, 24, size=n_records)
        streak_days      = np.clip(np.random.geometric(p=0.1, size=n_records), 1, 60)

        doomscroll_prob = (
            0.05
            + 0.30 * ((login_hour >= 22) | (login_hour <= 4)).astype(float)
            + 0.20 * (quests_completed == 0).astype(float)
            - 0.10 * (streak_days > 7).astype(float)
        ).clip(0, 1)

        doomscroll_triggered = np.random.binomial(1, doomscroll_prob)

        df = pd.DataFrame({
            "user_id":               user_ids,
            "date":                  dates,
            "session_duration_mins": np.round(session_duration, 2),
            "quests_completed":      quests_completed,
            "login_hour":            login_hour,
            "streak_days":           streak_days,
            "doomscroll_triggered":  doomscroll_triggered
        })
        return df

    def clean_and_engineer(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop_duplicates()
        df = df.dropna()
        df["session_duration_mins"] = df["session_duration_mins"].clip(lower=0, upper=840)

        df["user_id"]              = df["user_id"].astype(int)
        df["quests_completed"]     = df["quests_completed"].astype(int)
        df["login_hour"]           = df["login_hour"].astype(int)
        df["streak_days"]          = df["streak_days"].astype(int)
        df["doomscroll_triggered"] = df["doomscroll_triggered"].astype(int)

        # Log transform
        stat, p_value = stats.normaltest(df["session_duration_mins"])
        if p_value < 0.05:
            df["session_duration_mins"] = np.log1p(df["session_duration_mins"])

        # Feature Engineering
        safe_duration = df["session_duration_mins"].replace(0, 1)
        df["hourly_intensity"] = (df["quests_completed"] / (safe_duration / 60)).round(4)
        df["quest_overdue_flag"] = ((df["streak_days"] > 3) & (df["quests_completed"] == 0)).astype(int)
        df["late_night_flag"] = ((df["login_hour"] >= 22) | (df["login_hour"] <= 4)).astype(int)

        return df

    def split_and_scale(self, df: pd.DataFrame):
        numerical_cols = [
            "session_duration_mins",
            "quests_completed",
            "streak_days",
            "hourly_intensity"
        ]
        
        self.scaler = StandardScaler()
        df[numerical_cols] = self.scaler.fit_transform(df[numerical_cols])
        
        all_feature_cols = numerical_cols + ["login_hour", "quest_overdue_flag", "late_night_flag"]
        X = df[all_feature_cols].values
        y = df["doomscroll_triggered"].values

        smote = SMOTE(random_state=42)
        X_res, y_res = smote.fit_resample(X, y)

        X_train, X_test, y_train, y_test = train_test_split(
            X_res, y_res, test_size=0.2, random_state=42, stratify=y_res
        )

        os.makedirs("data/processed", exist_ok=True)
        np.save("data/processed/X_train.npy", X_train)
        np.save("data/processed/X_test.npy",  X_test)
        np.save("data/processed/y_train.npy", y_train)
        np.save("data/processed/y_test.npy",  y_test)

        return X_train, X_test, y_train, y_test

    def run(self, use_real_data=False):
        if use_real_data and os.path.exists(self.data_path):
            df = pd.read_csv(self.data_path)
        else:
            df = self.simulate_data()
            
        df = self.clean_and_engineer(df)
        X_train, X_test, y_train, y_test = self.split_and_scale(df)
        return X_train, X_test, y_train, y_test
