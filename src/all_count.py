import json
import pandas as pd

from constants import file_name

try:
    # Открываем файл и загружаем данные в формате JSON
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Инициализация словарей для хранения количества ОКС по кураторам
    curator_oks_count_problems = {}
    curator_oks_count_risks = {}

    # Получение общего количества проблем и рисков из блоков кураторов
    total_problems = {
        curator['curator_id']: int(curator['total_problems'])
        for curator in data['oks_with_problems'][0]['curators']
    }
    total_risks = {
        curator['curator_id']: int(curator['total_risks'])
        for curator in data['oks_with_risks'][0]['curators']
    }

    # Функция для подсчета количества ОКС из заданного блока
    def count_oks_from_block(block_name, curator_oks_count):
        for block in data[block_name]:
            for curator in block['curators']:
                curator_id = curator['curator_id']
                oks_count = len(curator['curator_records'])  # Количество записей ОКС

                if curator_id not in curator_oks_count:
                    curator_oks_count[curator_id] = 0

                curator_oks_count[curator_id] += oks_count

    # Подсчет ОКС из обоих блоков
    count_oks_from_block('table_oks_with_problems', curator_oks_count_problems)
    count_oks_from_block('table_oks_with_risks', curator_oks_count_risks)

    # Вывод результатов для блока проблем
    print('Количество ОКС по кураторам в блоке table_oks_with_problems:')
    for curator_id, oks_count in curator_oks_count_problems.items():
        print(f'Куратор ID: {curator_id}, Количество ОКС: {oks_count}')

    # Вывод результатов для блока рисков
    print('\nКоличество ОКС по кураторам в блоке table_oks_with_risks:')
    for curator_id, oks_count in curator_oks_count_risks.items():
        print(f'Куратор ID: {curator_id}, Количество ОКС: {oks_count}')

    # Сравнение значений по кураторам с total_problems и total_risks
    print(
        '\nСравнение количества ОКС по кураторам с '
        'total_problems и total_risks:'
    )
    all_curators = set(
        curator_oks_count_problems.keys()).union(curator_oks_count_risks.keys()
    )

    for curator_id in all_curators:
        count_problems = curator_oks_count_problems.get(curator_id, 0)
        count_risks = curator_oks_count_risks.get(curator_id, 0)

        # Сравнение с total_problems из блока oks_with_problems
        expected_problems = total_problems.get(curator_id, 0)
        if count_problems == expected_problems:
            print(
                f'Куратор ID: {curator_id} - совпадает с '
                f'total_problems: {count_problems} ОКС.'
            )
        else:
            print(
                f'Куратор ID: {curator_id} - не совпадает с total_problems: '
                f'{count_problems} ОКС (ожидалось {expected_problems}).'
            )

        # Сравнение с total_risks из блока oks_with_risks
        expected_risks = total_risks.get(curator_id, 0)
        if count_risks == expected_risks:
            print(
                f'Куратор ID: {curator_id} - совпадает с '
                f'total_risks: {count_risks} ОКС.'
            )
        else:
            print(
                f'Куратор ID: {curator_id} - не совпадает с total_risks: '
                f'{count_risks} ОКС (ожидалось {expected_risks}).'
            )

    # Проверка совпадений по oks_all
    oks_all_value = data['oks_with_risks_and_problems'][0]['oks_all']
    for key in ['oks_with_problems', 'oks_with_risks']:
        if data[key][0]['oks_all'] != oks_all_value:
            print(
                f'Несоответствие в {key}: ожидалось {oks_all_value}, '
                f'но найдено {data[key][0]["oks_all"]}.'
            )
        else:
            print('\nКоличество всех ОКС по всем кураторам совпадает\n')

    # Проверка совпадений по кураторам
    curators_with_risks_and_problems = {
        curator['curator_id']: curator
        for curator in data['oks_with_risks_and_problems'][0]['curators']
    }
    curators_with_problems = {
        curator['curator_id']: curator
        for curator in data['oks_with_problems'][0]['curators']
    }
    curators_with_risks = {
        curator['curator_id']: curator
        for curator in data['oks_with_risks'][0]['curators']
    }

    # Объединяем всех кураторов для проверки
    all_curators = set(curators_with_risks_and_problems.keys()).union(
        curators_with_problems.keys(), curators_with_risks.keys()
    )

    for curator_id in all_curators:
        oks_all_rp = curators_with_risks_and_problems.get(
            curator_id, {}
        ).get('oks_all', None)
        oks_all_p = curators_with_problems.get(
            curator_id, {}
        ).get('oks_all', None)
        oks_all_r = curators_with_risks.get(
            curator_id, {}
        ).get('oks_all', None)

        # Проверка на совпадение значений oks_all
        if oks_all_rp != oks_all_p or oks_all_rp != oks_all_r or oks_all_p != oks_all_r:
            print(f'Несоответствие для куратора {curator_id}:')
            if oks_all_rp is not None:
                print(f'  oks_all в рисках и проблемах: {oks_all_rp}')
            if oks_all_p is not None:
                print(f'  oks_all в проблемах: {oks_all_p}')
            if oks_all_r is not None:
                print(f'  oks_all в рисках: {oks_all_r}')
        else:
            print(
                f'Не выявлено расхождений по количеству всех ОКС у '
                f'куратора {curator_id}'
            )

    # Извлечение данных из блока table_oks_with_problems и table_oks_with_risks
    records_problems = data['table_oks_with_problems'][0]['records']
    records_risks = data['table_oks_with_risks'][0]['records']

    # Создание DataFrame из записей
    df_problems = pd.DataFrame(records_problems)
    df_risks = pd.DataFrame(records_risks)

    print(
        '\nРасчет количества всех ОКС в таблицах и сравнение с '
        'верхними виджетами'
    )

    # Подсчет уникальных значений по oks_code
    unique_oks_count_problems = df_problems['oks_code'].nunique()
    unique_oks_count_risks = df_risks['oks_code'].nunique()
    print(
        f'Количество уникальных ОКС по oks_code в '
        f'проблемах: {unique_oks_count_problems}'
    )
    print(
        f'Количество уникальных ОКС по oks_code в '
        f'рисках: {unique_oks_count_risks}'
    )

    # Сравнение с total_problems в oks_with_problems
    total_problems = int(data['oks_with_problems'][0]['total_problems'])
    if unique_oks_count_problems == total_problems:
        print(
            'Количество уникальных ОКС в проблемах совпадает с total_problems.'
        )
    else:
        print(
            f'Несоответствие: уникальные ОКС в проблемах = '
            f'{unique_oks_count_problems}, total_problems = {total_problems}.'
        )

    # Сравнение с total_risks в oks_with_risks
    total_risks = int(data['oks_with_risks'][0]['total_risks'])
    if unique_oks_count_risks == total_risks:
        print('Количество уникальных ОКС в рисках совпадает с total_risks.')
    else:
        print(
            f'Несоответствие: уникальные ОКС в рисках = '
            f'{unique_oks_count_risks}, total_risks = {total_risks}.'
        )

except FileNotFoundError:
    print(f'Файл "{file_name}" не найден. Проверьте имя файла и путь к нему.')
