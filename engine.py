from Work_excel import Work_excel
from Find_file_pdf import Find_pdf_file
from Parser_pdf import Parser_pdf
from Work_postgre import Append_table_postrge
from Work_excel import Write_data


class Engine():
    def __init__(self, file):
        self.table = Work_excel()
        self.list_from_user_file = self.table.read_excel(file)
        self.move = Write_data()
        self.pdf_files = Find_pdf_file()
        self.pars = Parser_pdf(file)
        self.app = Append_table_postrge()


    def engine(self):
        """Метод по запуску приложения"""
        self.pdf_files.query(self.list_from_user_file[0], self.list_from_user_file[3])
        data_value = self.pars.find_value(self.list_from_user_file[0], self.list_from_user_file[3])
        print(self.list_from_user_file)
        self.move.write_in_excel(data_value, self.list_from_user_file[1], self.list_from_user_file[2])
        self.app.app(data_value, self.list_from_user_file[1], self.list_from_user_file[2])

