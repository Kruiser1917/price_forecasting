import argparse
import pandas as pd

# Импорт из нашего проекта:
from price_forecasting.data.loader import load_csv_data
from price_forecasting.data.database import create_tables, insert_data
from price_forecasting.models.forecasting import PriceForecaster


def main():
    parser = argparse.ArgumentParser(description="Price Forecasting CLI")
    parser.add_argument("--load_csv", type=str,
                        help="Путь к CSV-файлу, из которого нужно загрузить данные в БД.")
    parser.add_argument("--train", action="store_true",
                        help="Запустить обучение модели на данных из БД.")
    parser.add_argument("--predict", nargs=5,
                        help="Сделать прогноз. Нужно передать 5 аргументов: price count add_cost company product")

    args = parser.parse_args()

    # 1. Загрузка CSV -> в БД
    if args.load_csv:
        create_tables()  # Создаёт таблицы, если их ещё нет
        data = load_csv_data(args.load_csv)
        insert_data(data)
        print(f"[INFO] Загрузили {len(data)} записей из {args.load_csv} в БД.")

    # 2. Обучение модели
    if args.train:
        forecaster = PriceForecaster()
        df = forecaster.load_data_from_db()

        if df.empty:
            print("[ERROR] В БД нет данных для обучения.")
        else:
            forecaster.train_model(df, target_column="price")
            print("[INFO] Модель успешно обучена!")

    # 3. Прогноз
    if args.predict:
        if len(args.predict) != 5:
            print("[ERROR] Для --predict нужно 5 аргументов: price count add_cost company product")
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

        # Создаём forecaster, снова грузим данные из БД и обучаем (упрощённый вариант).
        forecaster = PriceForecaster()
        df = forecaster.load_data_from_db()

        if df.empty:
            print("[ERROR] В БД нет данных для обучения.")
        else:
            forecaster.train_model(df, target_column="price")
            prediction = forecaster.predict(new_data)
            print(f"[INFO] Прогнозируемая цена: {prediction[0]:.2f}")


if __name__ == "__main__":
    main()
