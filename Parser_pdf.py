import os
import pdfplumber
from Work_excel import Work_excel


class Parser_pdf():
    def __init__(self, doc):
        self.doc = doc


    def find_file(self):
        list_file = []
        dir = 'C:\Python\pythonProject\\2025\work_inn\saving_pdf'
        for file in os.listdir(dir):
            if self.chek_files(file) == True:
                abs_path = os.path.join(dir, file)
                list_file.append(abs_path)
        return list_file


    def find_value(self):
        list_file = self.find_file()
        parsing_data = {'Полное наименование на русском языке': None,
                        'Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде': None,
                        'Сведения об основном виде деятельности': None}
        list_data = []
        # пробегаемся циклом по файлам из папки
        for file in list_file:
            Flag = False
            with pdfplumber.open(file) as file:
                # узнаем количество страниц
                count_pages = len(file.pages)
                # пробегаемся циклом по страницам файла
                for i in range(count_pages):
                    # парсим таблицу по строкам
                    tables = file.pages[i].extract_table()
                    # пробегаемся по строкам в поисках необходимых значений
                    try:
                        for value in tables:
                            if 'Полное наименование на русском языке' in value:
                                new_value = self.change_value(value[2])
                                parsing_data['Полное наименование на русском языке'] = new_value
                            elif 'Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде' in value:
                                new_value = self.change_value(tables[tables.index(value) + 2][2])
                                parsing_data['Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде']  = new_value
                            elif 'Сведения об основном виде деятельности' in value:
                                new_value = self.change_value(tables[tables.index(value) + 2][2])
                                parsing_data['Сведения об основном виде деятельности'] = new_value
                            if None not in parsing_data.values():
                                safe_data = parsing_data
                                list_data.append(safe_data.copy())
                                for key in parsing_data.keys():
                                    parsing_data[key] = None
                                Flag = True
                                break
                    except:
                        list_data.append('Данные в ЕГРЮЛ не найдены')
                    if None in parsing_data:
                        if i == count_pages:
                            safe_data = parsing_data
                            list_data.append(safe_data.copy())
                            for key in parsing_data.keys():
                                parsing_data[key] = None
                            Flag = True
                            break
                    if Flag == True:
                        break
        return list_data

    def change_value(self, value):
        if isinstance(value, str) and '\n' in value:
            new_value = value.replace('\n', ' ')
        else:
            new_value = value
        return new_value

    def chek_files(self, file):
        table = Work_excel()
        sp = table.read_excel(self.doc)
        flag = False
        for i in sp[0]:
            if str(i) in file:
                flag = True
        return flag


# pars = Parser_pdf()
# data_value = pars.find_value()