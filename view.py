from flask import Flask, render_template, request, flash
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'abracadabra'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)      # обозначаем директорию, для дальнейшего подбора настроек(конфигурации)
allowed_types = ['xlsx']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def validation_file(filename):
    if '.' in filename:
        if filename.rsplit(sep='.')[1].lower() in allowed_types:
            return True
        else:
            return False
    else:
        return False


def create_unique_name(filename):
    new_filename = filename
    root, format = os.path.splitext(filename)
    counter = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], new_filename)):
        counter += 1
        new_filename = f'{root}_{counter}{format}'
    return new_filename



@app.route('/', methods=['GET', 'POST'])
def start():
    upload_succees = False
    if request.method == 'POST':
        doc = request.files['file']
        print(request.files)
        if 'file' not in request.files:
            flash('файл не выбран, выберите файл', 'error')
        elif validation_file(doc.filename) == False:
            flash('Неверный тип данных, доступен только эксель', 'error')
        else:
            name = secure_filename(doc.filename)
            print(name)
            new_name = create_unique_name(name)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
            doc.save(file_path)
            upload_succees = True
    # elif request.method == 'GET':
        # from engine import Engine
        # go = Engine()
        # go.engine()
    return render_template('index.html', upload_succees=upload_succees)




if __name__ == '__main__':
    app.run(debug=True)


