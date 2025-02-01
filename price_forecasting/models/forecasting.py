import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from price_forecasting.data.database import fetch_all_data


def load_data_from_db() -> pd.DataFrame:
    """
    Загружает данные из БД, преобразует их в DataFrame.
    """
    records = fetch_all_data()
    # Преобразуем ORM-объекты в список словарей
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
    df = pd.DataFrame(data_dicts)
    return df


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Подготовка (очистка / генерация новых) признаков.
    Пока будем использовать простые признаки.
    """
    # Пример: создадим признак "price * count"
    df["price_x_count"] = df["price"] * df["count"]

    # Если есть конкуренты — "competitor_price", например
    # df["price_diff"] = df["price"] - df["competitor_price"]

    # Оставим только числовые столбцы, убрав категориальные (либо закодировав их при необходимости)
    # Для примера оставим price, count, add_cost и созданный price_x_count
    return df[["price", "count", "add_cost", "price_x_count"]]


class PriceForecaster:
    """
    Класс для обучения и использования модели прогнозирования цен.
    """

    def __init__(self):
        self.model = None

    def train_model(self, df: pd.DataFrame, target_column: str = "price") -> None:
        """
        Обучение модели.
        В зависимости от задачи:
         - Целевой столбец может быть "price" (предсказываем будущую цену).
         - Или отдельный столбец "optimal_price" / "future_price" и т.д.
        """
        X = prepare_features(df)
        y = df[target_column]

        # Обучаем простую линейную регрессию
        self.model = LinearRegression()
        self.model.fit(X, y)

    def predict(self, new_data: pd.DataFrame) -> np.ndarray:
        """
        Прогноз цены для новых данных.
        Предполагается, что в new_data те же столбцы, что и в train_model.
        """
        if not self.model:
            raise ValueError("Модель не обучена. Сначала вызовите train_model().")

        X_new = prepare_features(new_data)
        predictions = self.model.predict(X_new)
        return predictions
