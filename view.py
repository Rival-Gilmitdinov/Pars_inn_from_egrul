from flask import Flask, render_template, request, flash, send_file, session
import os
# from engine import Engine
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = 'abracadabra'

allowed_types = ['xlsx']


def validation_file(filename):
    if '.' in filename:
        if filename.rsplit(sep='.')[1].lower() in allowed_types:
            return True
        else:
            return False
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def start():
    succes = False
    if request.method == 'POST':
        doc = request.files['file']
        session['name_file'] = doc.filename.rsplit('.')[0]
        if 'file' not in request.files:
            flash('файл не выбран, выберите файл', 'error')
        elif validation_file(doc.filename) == False:
            flash('Неверный тип данных, доступен только эксель', 'error')
        else:
            from engine import Engine
            go = Engine(doc)
            go.engine()
            succes = True
    return render_template('index.html', succes=succes)


@app.route('/result', methods=['GET', 'POST'])
def result():
    name_user_file = session['name_file']
    list_files = os.listdir(f'saving_pdf\\{name_user_file}')
    for file in list_files:
        if 'xlsx' in file:
            file_path = f'saving_pdf\\{name_user_file}\\result_data_{name_user_file}.xlsx'
            filename = f'result_data_{name_user_file}.xlsx'
            return send_file(
                    file_path,
                    as_attachment=True,
                    download_name=filename,
                    mimetype='application/octet-stream'
                )


if __name__ == '__main__':
    app.run(debug=True)


