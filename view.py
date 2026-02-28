from flask import Flask, render_template, request, flash
import os
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
    if request.method == 'POST':
        doc = request.files['file']
        print(request.files)
        if 'file' not in request.files:
            flash('файл не выбран, выберите файл', 'error')
        elif validation_file(doc.filename) == False:
            flash('Неверный тип данных, доступен только эксель', 'error')
        else:
            from engine import Engine
            go = Engine(doc)
            go.engine()

    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)


