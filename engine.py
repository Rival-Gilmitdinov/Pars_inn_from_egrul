from Work_excel import Work_excel
from Find_file_pdf import Find_pdf_file
from Parser_pdf import Parser_pdf
from Work_postgre import Append_table_postrge, cheсk
from Work_excel import Write_data
import time


class Engine():
    def __init__(self, file):
        self.table = Work_excel(file)
        self.path_dir = self.table.path_dir()
        self.name_split = self.table.file_name()
        self.list_from_user_file = self.table.read_excel()[0]
        self.error_data = self.table.read_excel()[1]
        self.move = Write_data()
        self.pdf_files = Find_pdf_file()
        self.pars = Parser_pdf()
        self.app = Append_table_postrge()
        # self.all_results_from_database = cheсk.chek_data_from_postgre()[0]
        self.list_inn_from_postgre = cheсk.check_data_from_postgre(self.list_from_user_file)
        self.error_response = self.pdf_files.error_response
        self.errors_from_postgre = cheсk.pars_erros_from_postgre()


    def engine(self):
        """Метод по запуску приложения"""
        time_1 = time.time()
        self.pdf_files.query(self.list_from_user_file, self.path_dir, self.list_inn_from_postgre[1])
        data_value = self.pars.find_value(self.list_from_user_file, self.path_dir, self.list_inn_from_postgre)
        print(self.list_from_user_file)
        self.move.write_in_excel(data_value, self.error_data, self.name_split, self.error_response)
        self.app.app(data_value, self.error_data, self.list_inn_from_postgre, self.error_response, self.errors_from_postgre)
        self.pdf_files.delete_old_files(self.path_dir)
        print(self.error_response)
        time_2 = time.time()
        print(f'время выполения программы составляет {time_2 - time_1}')


