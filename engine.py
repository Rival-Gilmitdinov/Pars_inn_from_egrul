from Work_excel import sp
from Find_file_pdf import pdf_files
from Parser_pdf import pars
from Work_postgre import app
from Work_excel import move


def engine():
    pdf_files.query(sp[0])
    data_value = pars.find_value()
    print(data_value)
    move.write_in_excel(data_value, sp[0], sp[1], sp[2])
    app.app(data_value, sp[0], sp[1], sp[2])

engine()