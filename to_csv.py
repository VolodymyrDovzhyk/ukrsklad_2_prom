import csv
import math


file_input = 'export_from_ukrSklad.csv'
file_to_prom = 'import_to_PROM.csv'
id_main_group = '101290945'  # str(int) -> ID main group at PROM.ua

with open(file_to_prom, 'w+', newline="") as file2prom:
    fieldnames = ['Название_позиции', 'Поисковые_запросы', 'Описание', 'Тип_товара', 'Цена', 'Валюта',
                  'Единица_измерения', 'Оптовая_цена', 'Минимальный_заказ_опт', 'Ссылка_изображения', 'Наличие',
                  'Идентификатор_товара', 'Идентификатор_группы', 'Личные_заметки']
    writer = csv.DictWriter(file2prom, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    with open(file_input) as f:
        reader = csv.DictReader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        counter = 0
        for row in reader:
            prod_name = row['"Повна назва товару"'].replace('"', '').replace(',', ' ')
            # Формуємо ключові слова зі слів в назві товару
            req_keys = [i for i in prod_name.split()]
            req_keys.append(prod_name)
            # Округлена роздрібна ціна в УкрСклад
            price = math.ceil(float(row['"Розд. ціна"'].strip().replace(',', '.').replace('"', '')))
            # Ціни для імопрту в Пром.юа
            price_opt = round(1.05 * price)  # Множитель оптовой цены  * "Розд. ціна"
            price_roz = round(1.12 * price)  # Множитель рознечной цены  * "Розд. ціна"
            position = dict(Название_позиции=prod_name, Поисковые_запросы=','.join(req_keys),
                            Описание=','.join(req_keys), Тип_товара='u', Цена=price_roz, Валюта='UAH',
                            Единица_измерения='шт.', Оптовая_цена=price_opt, Минимальный_заказ_опт='6.000',
                            Наличие='+', Идентификатор_товара=row['"ID"'].replace('"', ''),
                            Идентификатор_группы=id_main_group, Личные_заметки='Imported')
            writer.writerow(position)
            counter += 1
        print(f"Обработано {counter} позиций")
