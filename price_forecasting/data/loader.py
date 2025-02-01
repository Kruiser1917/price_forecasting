import csv


def load_csv_data(file_path: str) -> list[str]:
    """
    Функция для загрузки CSV данных.
    Возвращает список словарей, где ключи - названия столбцов.
    """
    data = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data
