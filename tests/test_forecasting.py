import pandas as pd

from price_forecasting.models.forecasting import PriceForecaster


def test_forecasting_flow():
    # Создаем фейковый DataFrame
    df = pd.DataFrame({
        "price": [100, 150, 200],
        "count": [10, 12, 8],
        "add_cost": [5000, 6000, 7000],
        "company": ["A", "B", "C"],
        "product": ["X", "Y", "Z"]
    })

    forecaster = PriceForecaster()
    forecaster.train_model(df, target_column="price")

    # Предскажем цену на новых данных
    new_data = pd.DataFrame({
        "price": [120],
        "count": [9],
        "add_cost": [5500],
        "company": ["A"],
        "product": ["X"]
    })

    predicted = forecaster.predict(new_data)
    assert len(predicted) == 1
    assert predicted[0] > 0  # Мы ожидаем, что модель не выдает отрицательное значение
