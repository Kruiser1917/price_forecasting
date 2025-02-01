from price_forecasting.data.loader import load_csv_data


def test_load_csv_data(tmp_path):
    # Создаем временный csv-файл
    d = tmp_path / "sub"
    d.mkdir()
    file_path = d / "test.csv"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("price,count,add_cost,company,product\n")
        f.write("100,10,5000,CompanyA,ProductA\n")
        f.write("200,5,3000,CompanyB,ProductB\n")

    data = load_csv_data(str(file_path))
    assert len(data) == 2
    assert data[0]["price"] == "100"
    assert data[0]["company"] == "CompanyA"
