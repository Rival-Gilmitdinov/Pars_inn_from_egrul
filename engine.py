from Work_excel import Work_excel
from Find_file_pdf import Find_pdf_file
from Parser_pdf import Parser_pdf
from Work_postgre import Append_table_postrge
from Work_excel import Write_data


class Engine():
    def __init__(self, file):
        self.table = Work_excel()
        self.sp = self.table.read_excel(file)
        self.move = Write_data()
        self.pdf_files = Find_pdf_file()
        self.pars = Parser_pdf(file)
        self.app = Append_table_postrge()


    def engine(self):
        """Метод по запуску приложения"""
        self.pdf_files.query(self.sp[0])
        data_value = self.pars.find_value(self.sp[0])
        print(self.sp)
        self.move.write_in_excel(data_value, self.sp[0], self.sp[1], self.sp[2])
        self.app.app(data_value, self.sp[0], self.sp[1], self.sp[2])

