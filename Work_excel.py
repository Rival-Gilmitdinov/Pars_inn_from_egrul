import openpyxl
from openpyxl import load_workbook
import glob
import os


class Work_excel():
    def read_excel(self, file) -> tuple:
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
        error_data = {}
        # Проходим циклом по значениям таблицы
        for row in ws.iter_rows(values_only=True):
            for value in range(len(row)):
                if type(row[value]) == int or (type(row[value]) == str and row[value].isdigit()):
                    if len(str(row[value])) == 10 or len(str(row[value])) == 12:
                        list_data_inn.append(int(row[value]))
                    else:
                        error_data.setdefault(row[value], 'Неверное количество цифр инн')
                elif row[value] == None:
                    continue
                else:
                    error_data.setdefault(row[value], 'Неверный тип данных')
        name_split = file.filename.rsplit('.')[0]
        path_dir = f'C:\Python\pythonProject\\2025\work_inn\saving_pdf\\{name_split}'
        if name_split not in os.listdir('C:\Python\pythonProject\\2025\work_inn\saving_pdf'):
            os.mkdir(path_dir)
        return list_data_inn, error_data, path_dir, name_split


class Write_data():
    def write_in_excel(self, data_value, error_data, name_split, error_response) -> None:
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
        if error_data:
            for key_error_data, value_error_data in error_data.items():
                sheet[n][0].value = key_error_data
                sheet[n][1].value = value_error_data
                n += 1
        elif error_response:
            for key, value in error_response.items():
                sheet[n][0].value = key
                sheet[n][1].value = value
        book.save(f'C:\Python\pythonProject\\2025\work_inn\saving_pdf\\{name_split}\\result_data_{name_split}.xlsx')
        book.close()



















