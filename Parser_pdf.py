import os
import pdfplumber
from Work_excel import Work_excel
from Work_postgre import Check_data


class Parser_pdf():
    def __init__(self):
        self.check = Check_data()


    def find_file(self, path_dir) -> list:
        """Метод по нахождению файла и создания списка с полным путем к ним"""
        list_file = []
        # dir = 'C:\Python\pythonProject\\2025\work_inn\saving_pdf'
        for file in os.listdir(path_dir):
            if 'pdf' in file:
                abs_path = os.path.join(path_dir, file)
                list_file.append(abs_path)
        return list_file


    def find_value(self, list_from_excel, path_dir, list_inn_from_postgre) -> list:
        """Метод по парсингу пдф файла, сбор этих данных в каждый словарь и добавление этих словарей в один список
        Parameters:
            list_from_excel: list
                Список с перечнем инн, по которым пользователь хочет получить данные"""
        list_file = self.find_file(path_dir)
        print(f'парсер_пдф ---- список полных путей файлов {list_file}')
        parsing_data = {'инн': None,
                        'Полное наименование на русском языке': None,
                        'Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде': None,
                        'Сведения об основном виде деятельности': None}
        list_data = []
        # Пробегаемся циклом по инн, которые были спарсены из экселя, который загрузил пользователь
        for value_inn_from_excel in list_from_excel:
            # Проверка, если такой инн в базе данных
            if str(value_inn_from_excel) in list_inn_from_postgre:
                for value_postgre in self.check.pars_from_postgre(int(value_inn_from_excel)):
                    parsing_data['инн'] = int(value_postgre.inn_company)
                    parsing_data['Полное наименование на русском языке'] = value_postgre.name
                    parsing_data['Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде'] = value_postgre.capital
                    parsing_data['Сведения об основном виде деятельности'] = value_postgre.activity
                copy_dict = parsing_data.copy()
                list_data.append(copy_dict)
                print(f'значение есть в посгре - {list_data}')
                for file_in_dir in list_file:
                    if str(value_inn_from_excel) in file_in_dir:
                        list_file.remove(file_in_dir)
        if None not in parsing_data.values():
            for keys in parsing_data.keys():
                parsing_data[keys] = None
        print(f'после проверки на наличие данных в постгрессе у нас выходит такой списко файлов {list_file}')
        if not list_file:
            return list_data
        # пробегаемся циклом по файлам из папки
        for file in list_file:
            # for name_of_file in file.split('\\'):
            #     if 'result_search_file' in name_of_file:
            #         inn = name_of_file.split('_')[0]
            #         parsing_data['инн'] = inn
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
                            if 'ИНН юридического лица' in value:
                                parsing_data['инн'] = value[2]
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
                                print(f'По итогу в цикле парсер_пдф получается {list_data}')
                                for key in parsing_data.keys():
                                    parsing_data[key] = None
                                Flag = True
                                break
                    except:
                        list_data.append('Данные в ЕГРЮЛ не найдены')
                    if 1 < list(parsing_data.values()).count(None) < 5:
                        if i == count_pages - 1:
                            safe_data = parsing_data
                            list_data.append(safe_data.copy())
                            for key in parsing_data.keys():
                                parsing_data[key] = None
                            Flag = True
                            break
                    if Flag == True:
                        break
        print(f'итоговое значение - {list_data}')
        return list_data

    def change_value(self, value) -> str:
        """Метод по изменению строковых данных, спарсенных из пдф файла
        Parameters:
            value - str
                Данные,спарсенные из пдф файла"""
        if isinstance(value, str) and '\n' in value:
            new_value = value.replace('\n', ' ')
        else:
            new_value = value
        return new_value

    # def chek_files(self, file) -> bool:
    #     """Метод по проверке наличия инн, необходимого для получения данных и того файла, над которым ведется работа"""
    #     table = Work_excel()
    #     sp = table.read_excel(self.doc)
    #     flag = False
    #     for i in sp[0]:
    #         if str(i) in file:
    #             flag = True
    #     return flag

# pars = Parser_pdf()
# print(pars.find_value([3444051154, 6319054636], 'C:\Python\pythonProject\\2025\work_inn\saving_pdf\еще один пробный файл', []))
#
