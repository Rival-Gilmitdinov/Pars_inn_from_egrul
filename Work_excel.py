import openpyxl
from openpyxl import load_workbook
import glob
import os
import os




class Work_excel():
    # def find_file(self):
    #     direct = os.path.dirname(__file__)
    #     way_html = os.path.join(direct, 'uploads')
    #     file = glob.glob(os.path.join(way_html, '*'))
    #     new_file = max(file, key=os.path.getmtime)
    #     return new_file


    def read_excel(self, file):
        '''Функия по парсингу таблицы excel
        Return: dannie - список с данными инн
        error_type - словарь с неверными значениями и текстом ошибки
        error_data - словарь с неверными значениями и текстом ошибки'''
        wb = load_workbook(file, read_only=True)
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


# table = Work_excel()
# sp = table.read_excel()
# print(sp[0])
# print(sp[1])
# print(sp[2])


class Write_data():
    def write_in_excel(self, spisok, inn, error_type, error_data):
        book = openpyxl.Workbook()
        sheet = book.active
        sheet['A1'] = 'ИНН'
        sheet['B1'] = 'Полное наименование на русском языке'
        sheet['C1'] = 'Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде'
        sheet['D1'] = 'Сведения об основном виде деятельности'
        n = 1
        for value in spisok:
            sheet[n][0].value = inn[n - 1]
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


# move = Write_data()

# move.write_in_excel(data_value, sp[0], sp[1], sp[2])















