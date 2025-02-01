# Модель ценообразования (Price Forecasting)

## Описание
Данный проект реализует алгоритм прогнозирования цены на основе исторических данных:
- Цена товара (`price`)
- Количество продаж (`count`)
- Затраты на продвижение (`add_cost`)
- Компания (`company`)
- Продукт (`product`)
- (Опционально) Цены конкурентов

Цель проекта — спрогнозировать оптимальную/будущую цену, исходя из существующих данных о продажах, продвижении и ценах конкурентов.

## Структура проекта

price_forecasting/ ├── price_forecasting/ │ ├── data/ │ │ ├── database.py # Модуль работы с базой данных (SQLite + SQLAlchemy) │ │ ├── loader.py # Модуль для чтения CSV │ ├── models/ │ │ ├── forecasting.py # Модель (линейная регрессия) и класс PriceForecaster │ ├── main.py # Точка входа в приложение ├── tests/ │ ├── test_database.py │ ├── test_loader.py │ ├── test_forecasting.py ├── csv_data.csv # Входные данные (пример) ├── requirements.txt ├── README.md └── .gitignore


## Установка и запуск

1. Склонировать репозиторий:
   ```bash
   git clone https://github.com/<user>/price_forecasting.git

2. Установить зависимости
   ```bash
   cd price_forecasting
   pip install -r requirements.txt

3. Создать таблицы в базе данных (при первом запуске):
   ```bash  
   python -c "from price_forecasting.data.database import create_tables; create_tables()"
   
4. Загрузить данные из CSV и сохранить в БД (пример сценария в main.py):
   ```bash
   python price_forecasting/main.py --load_csv csv_data.csv

5. Запустить обучение модели (пример, также может быть реализовано в main.py):
   ```bash
   python price_forecasting/main.py --train

6. Сформировать прогноз (пример, также в main.py):
   ```bash
   python price_forecasting/main.py --predict

## Тестирование

Для запуска тестов:

   ```bash
   pytest
   ```
Для проверки покрытия тестами:

   ```bash
   pytest --cov=price_forecasting --cov-report=html
   ```
Отчёт о покрытии появится в папке htmlcov.


## Автор

Рафаэль Аптикеев aptikeev1942@gmail.com 

---








