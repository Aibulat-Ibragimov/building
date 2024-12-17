import pandas as pd
import json
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from constants import file_name, date_now


try:
    # Открываем файл и загружаем данные в формате JSON
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Создаем словари для сопоставления кодов и названий различных проектов и статусов
    national_projects = {
        item['code']: item['name'] for item in data['national_projects']
    }
    federal_projects = {
        item['code']: item['name'] for item in data['federal_projects']
    }
    regions = {
        item['code']: item['name'] for item in data['regions']
    }
    oks_statuses = {
        item['code']: item['name'] for item in data['oks_statuses']
    }
    grbses = {
        item['code']: item['name'] for item in data['grbses']
    }
    risks = {
        item['code']: item['name'] for item in data['risks']
    }

    # Извлекаем записи из блока с рисками
    records = data['table_oks_with_risks'][0]['records']

    rows = []

    # Формируем список строк для DataFrame
    for record in records:
        for risk in record['risks']:
            row = {
                "oks_name": record['oks_name'],
                "oks_code": record['oks_code'],
                "national_project_code": record['national_project_code'],
                "federal_project_code": record['federal_project_code'],
                "region_code": record['region_code'],
                "oks_address": record['oks_address'],
                "grbs_code": record['grbs_code'],
                "cost_oks": record['cost_oks'],
                "oks_status_code": record['oks_status_code'],
                "risk_code": risk['risk_code'],
                "date_detected_risk": risk['date_detected_risk']
            }
            rows.append(row)

    # Создаем DataFrame из собранных строк
    df = pd.DataFrame(rows)

    # Добавляем названия проектов и статусов на основе кодов
    df['national_project_name'] = df['national_project_code'].map(national_projects)
    df['federal_project_name'] = df['federal_project_code'].map(federal_projects)
    df['region_name'] = df['region_code'].map(regions)
    df['oks_status_name'] = df['oks_status_code'].map(oks_statuses)
    df['grbs_name'] = df['grbs_code'].map(grbses)
    df['risk_name'] = df['risk_code'].map(risks)

    # Удаляем коды, оставляя только названия
    df.drop(
        columns=[
            'national_project_code', 'federal_project_code',
            'region_code', 'oks_status_code',
            'grbs_code', 'risk_code'
        ], inplace=True
    )

    # Создание нового Excel файла
    wb = Workbook()
    ws = wb.active

    # Запись заголовков столбцов в Excel
    ws.append(df.columns.tolist())

    # Запись данных из DataFrame в Excel
    for row in dataframe_to_rows(df, index=False, header=False):
        row[1] = str(row[1])  # Преобразование oks_code в строку для корректной записи
        ws.append(row)

    # Сохраняем файл в указанном пути
    wb.save(f"C:\\Users\\Aibulat\\work\\building\\output\\oks_with_risks_{date_now}.xlsx")

    print(f"Данные успешно сохранены в файл oks_with_risks_{date_now}.xlsx")

except FileNotFoundError:
    print(f"Файл '{file_name}' не найден. Проверьте имя файла и путь к нему.")
except KeyError as e:
    print(f"Ошибка: отсутствует ключ {e} в данных.")
