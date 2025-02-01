from price_forecasting.data.database import insert_data, fetch_all_data, create_tables


def test_insert_and_fetch_data():
    # Перед началом тестов можно пересоздать таблицы (если боитесь перезаписи).
    create_tables()

    data_list = [
        {"price": "100", "count": "10", "add_cost": "5000", "company": "TestCompany", "product": "TestProduct"},
        {"price": "200", "count": "5", "add_cost": "3000", "company": "TestCompany2", "product": "TestProduct2"}
    ]

    insert_data(data_list)
    records = fetch_all_data()
    assert len(records) >= 2  # Проверяем, что они добавились
    # Можно проверять конкретные значения
