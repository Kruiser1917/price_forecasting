# price_forecasting/models/forecasting.py

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from price_forecasting.data.database import fetch_all_data

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    df["price_x_count"] = df["price"] * df["count"]
    return df[["price", "count", "add_cost", "price_x_count"]]

class PriceForecaster:
    def __init__(self):
        self.model = None

    def load_data_from_db(self) -> pd.DataFrame:
        records = fetch_all_data()
        data_dicts = [
            {
                "price": rec.price,
                "count": rec.count,
                "add_cost": rec.add_cost,
                "company": rec.company,
                "product": rec.product
            }
            for rec in records
        ]
        return pd.DataFrame(data_dicts)

    def train_model(self, df: pd.DataFrame, target_column: str = "price") -> None:
        X = prepare_features(df)
        y = df[target_column]
        self.model = LinearRegression()
        self.model.fit(X, y)

    def predict(self, new_data: pd.DataFrame) -> np.ndarray:
        if not self.model:
            raise ValueError("Модель не обучена. Сначала вызовите train_model().")
        X_new = prepare_features(new_data)
        return self.model.predict(X_new)
