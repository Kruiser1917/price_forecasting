import argparse

import pandas as pd

from price_forecasting.data.database import create_tables, insert_data
# Импорты собственных модулей
from price_forecasting.data.loader import load_csv_data
from price_forecasting.models.forecasting import PriceForecaster


def main():
    parser = argparse.ArgumentParser(description="Price Forecasting CLI")
    parser.add_argument("--load_csv", type=str,
                        help="Путь к CSV-файлу, из которого будут загружены данные.")
    parser.add_argument("--train", action="store_true",
                        help="Запустить обучение модели на данных, находящихся в БД.")
    parser.add_argument("--predict", nargs="+",
                        help="Сделать прогноз. Нужно передать 5 аргументов: price, count, add_cost, company, product")
    args = parser.parse_args()

    # 1. Загрузка данных из CSV в БД
    if args.load_csv:
        create_tables()  # Создаём таблицы (если ещё не созданы)
        data = load_csv_data(args.load_csv)
        insert_data(data)
        print(f"[INFO] Загрузили {len(data)} записей в БД из файла {args.load_csv}")

    # 2. Обучение модели
    if args.train:
        forecaster = PriceForecaster()
        df = load_data_from_db()  # Загружаем данные из БД в pandas
        forecaster.train_model(df, target_column="price")  # Обучаем модель
        print("[INFO] Модель успешно обучена!")

    # 3. Прогноз для новых данных
    if args.predict:
        # Ожидаем 5 аргументов: price, count, add_cost, company, product
        if len(args.predict) != 5:
            print("[ERROR] Для --predict нужно передать ровно 5 аргументов:")
            print("        price count add_cost company product")
            return

        price, count, add_cost, company, product = args.predict

        # Формируем DataFrame с новыми данными
        new_data = pd.DataFrame({
            "price": [float(price)],
            "count": [int(count)],
            "add_cost": [float(add_cost)],
            "company": [company],
            "product": [product]
        })

        # Чтобы сделать предсказание, модель должна быть обучена.
        # Можно быстро (пере)обучить модель на тех же данных из БД:
        forecaster = PriceForecaster()
        df = load_data_from_db()
        forecaster.train_model(df, target_column="price")

        prediction = forecaster.predict(new_data)
        print(f"[INFO] Прогнозируемая цена для введённых данных: {prediction[0]:.2f}")


if __name__ == "__main__":
    main()
