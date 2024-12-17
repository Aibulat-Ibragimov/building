import json

from constants import file_name

try:
    # Открываем файл и загружаем данные в формате JSON
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Уникальные ОКС без привязки к куратору
    unique_oks_set = set()

    # Извлечение ОКС из блока table_oks_with_problems
    for record in data['table_oks_with_problems'][0]['records']:
        unique_oks_set.add(record['oks_code'])

    # Извлечение ОКС из блока table_oks_with_risks
    for record in data['table_oks_with_risks'][0]['records']:
        unique_oks_set.add(record['oks_code'])

    # Подсчет уникальных ОКС без привязки к куратору
    total_unique_oks = len(unique_oks_set)
    print(
        f'Количество уникальных ОКС без привязки к куратору: {total_unique_oks}'
    )

    # Уникальные ОКС с привязкой к кураторам
    curator_unique_oks = {}

    # Извлечение ОКС с привязкой к кураторам из блока table_oks_with_problems
    for curator in data['table_oks_with_problems'][0]['curators']:
        curator_id = curator['curator_id']
        curator_unique_oks[curator_id] = set()  # Инициализация множества для уникальных ОКС куратора
        for record in curator['curator_records']:
            curator_unique_oks[curator_id].add(record['oks_code'])

    # Извлечение ОКС с привязкой к кураторам из блока table_oks_with_risks
    for curator in data['table_oks_with_risks'][0]['curators']:
        curator_id = curator['curator_id']
        if curator_id not in curator_unique_oks:
            curator_unique_oks[curator_id] = set()  # Инициализация, если куратора еще нет
        for record in curator['curator_records']:
            curator_unique_oks[curator_id].add(record['oks_code'])

    # Подсчет уникальных ОКС с привязкой к куратору и проверка
    for curator_id, oks_set in curator_unique_oks.items():
        unique_count = len(oks_set)  # Подсчет уникальных ОКС для текущего куратора
        print(
            f'Куратор ID: {curator_id}, Количество уникальных ОКС: {unique_count}'
        )

        # Получение total_problems и total_risks для каждого куратора
        total_problems_and_risks = 0

        for curator in data['oks_with_risks_and_problems'][0]['curators']:
            if curator['curator_id'] == curator_id:
                total_problems_and_risks = curator.get(
                    'total_risks_and_problems', 0
                )
                break

        # Приведение типов к целым числам для сравнения
        if isinstance(total_problems_and_risks, str):
            total_problems_and_risks = int(total_problems_and_risks)

        # Сравнение уникального количества ОКС с ожидаемым значением
        if unique_count == total_problems_and_risks:
            print(
                f'Количество уникальных ОКС у куратора {curator_id} '
                f'совпадает со значением верхнего виджета.'
            )
        else:
            print(
                f'Несоответствие для куратора {curator_id}: уникальные '
                f'ОКС = {unique_count}, верхнем виджете = {total_problems_and_risks}.'
            )

    # Сравнение общего количества рисков и проблем с верхним виджетом
    total_risks_and_problems = int(
        data['oks_with_risks_and_problems'][0]['total_risks_and_problems']
    )
    print(f'Значение верхнего виджета: {total_risks_and_problems}')

    # Проверка совпадения количества уникальных ОКС с верхним виджетом
    if total_unique_oks == total_risks_and_problems:
        print('Количество уникальных ОКС совпадает со значением верхнего виджета.')
    else:
        print(
            f'Несоответствие: уникальные ОКС = {total_unique_oks}, '
            f'верхний виджет = {total_risks_and_problems}.'
        )

except FileNotFoundError:
    print(f'Файл "{file_name}" не найден. Проверьте имя файла и путь к нему.')
except KeyError as e:
    print(f'Ошибка: отсутствует ключ {e} в данных.')
except ValueError as e:
    print(f'Ошибка преобразования значения: {e}')
