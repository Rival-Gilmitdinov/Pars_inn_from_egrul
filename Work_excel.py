from openpyxl import load_workbook
import glob
import os
import os
import requests
from qwe import cookies, headers
import time
import pdfplumber


class Work_excel():
    def find_file(self):
        direct = os.path.dirname(__file__)
        way_html = os.path.join(direct, 'uploads')
        file = glob.glob(os.path.join(way_html, '*'))
        new_file = max(file, key=os.path.getmtime)
        return new_file


    def read_excel(self):
        '''Функия по парсингу таблицы excel
        Return: dannie - список с данными инн
        error_type - словарь с неверными значениями и текстом ошибки
        error_data - словарь с неверными значениями и текстом ошибки'''
        wb = load_workbook(self.find_file(), read_only=True)
        ws = wb.active
        dannie = []
        error_type = {}
        error_data = {}
        # Проходим циклом по значениям таблицы
        for row in ws.iter_rows(values_only=True):
            for value in range(len(row)):
                if type(row[value]) == int:
                    if 10 ** 11 <= row[value] < 10 ** 12 or 10 ** 9 <= row[value] < 10 ** 10:
                        dannie.append(row[value])
                    else:
                        error_data.setdefault(row[value], 'Неверное количество цифр инн')
                else:
                    error_type.setdefault(row[value], 'Неверный тип данных')
        return dannie, error_type, error_data


table = Work_excel()
sp = table.read_excel()
print(sp[0])
print(sp[1])
print(sp[2])

















