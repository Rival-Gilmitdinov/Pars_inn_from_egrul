import openpyxl
from openpyxl import load_workbook
import glob
import os


class Work_excel():
    def read_excel(self, file) -> list:
        '''Функия по парсингу таблицы excel
        file : файл, который загружает пользователь
        Return: list_data_inn - list
            список с данными инн
        error_type - dict
            словарь с неверными значениями и текстом ошибки
        error_data - dict
            словарь с неверными значениями и текстом ошибки'''
        wb = load_workbook(file, read_only=True)
        ws = wb.active
        list_data_inn = []
        error_type = {}
        error_data = {}
        # Проходим циклом по значениям таблицы
        for row in ws.iter_rows(values_only=True):
            for value in range(len(row)):
                if type(row[value]) == int:
                    if 10 ** 11 <= row[value] < 10 ** 12 or 10 ** 9 <= row[value] < 10 ** 10:
                        list_data_inn.append(row[value])
                    else:
                        error_data.setdefault(row[value], 'Неверное количество цифр инн')
                else:
                    error_type.setdefault(row[value], 'Неверный тип данных')
        return list_data_inn, error_type, error_data


class Write_data():
    def write_in_excel(self, data_value, error_type, error_data) -> None:
        """Функция по записи данных в новую эксель таблицу
        Parameters:
            spisok: list
                Список со словарями, в которых записаны спарсенные данные
            inn: list
                Список с необходимыми инн
            error_type: dict
                Словарь с неверным типом данных:
                    key - данные, которые передал пользователь
                    value - сообщение о неверном данном
            error_data: dict
                Словарь с неверными данными
                    key - данные, которые передал пользователь
                    value - сообщение о неверном данном
        """
        book = openpyxl.Workbook()
        sheet = book.active
        sheet['A1'] = 'ИНН'
        sheet['B1'] = 'Полное наименование на русском языке'
        sheet['C1'] = 'Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде'
        sheet['D1'] = 'Сведения об основном виде деятельности'
        n = 1
        for value in data_value:
            sheet[n][0].value = value['инн']
            sheet[n][1].value = value['Полное наименование на русском языке']
            sheet[n][2].value = value['Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде']
            sheet[n][3].value = value['Сведения об основном виде деятельности']
            n += 1
        if error_type:
            for key_error_type, value_error_type in error_type.items():
                sheet[n][0].value = key_error_type
                sheet[n][1].value = value_error_type
                n += 1
        if error_data:
            for key_error_data, value_error_data in error_data.items():
                sheet[n][0].value = key_error_data
                sheet[n][1].value = value_error_data
                n += 1
        book.save('result_data.xlsx')
        book.close()


















