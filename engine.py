from Work_excel import Work_excel
from Find_file_pdf import Find_pdf_file
from Parser_pdf import Parser_pdf
from Work_postgre import Append_table_postrge, cheсk
from Work_excel import Write_data


class Engine():
    def __init__(self, file):
        self.table = Work_excel()
        self.list_from_user_file = self.table.read_excel(file)
        self.move = Write_data()
        self.pdf_files = Find_pdf_file()
        self.pars = Parser_pdf()
        self.app = Append_table_postrge()
        # self.all_results_from_database = cheсk.chek_data_from_postgre()[0]
        self.list_inn_from_postgre = cheсk.check_data_from_postgre()


    def engine(self):
        """Метод по запуску приложения"""
        self.pdf_files.query(self.list_from_user_file[0], self.list_from_user_file[3], self.list_inn_from_postgre)
        data_value = self.pars.find_value(self.list_from_user_file[0], self.list_from_user_file[3], self.list_inn_from_postgre)
        print(self.list_from_user_file)
        self.move.write_in_excel(data_value, self.list_from_user_file[1], self.list_from_user_file[2], self.list_from_user_file[4])
        self.app.app(data_value, self.list_from_user_file[1], self.list_from_user_file[2], self.list_inn_from_postgre)

