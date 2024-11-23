import os
import pandas as pd
from flask import Flask, request, redirect, url_for, render_template, session, send_file
from werkzeug.utils import secure_filename
from utils import *
from config import *

app = Flask(__name__)
app.secret_key = 'secretary'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            df = preprocess_data(file_path)

            session['file_path'] = df

            return redirect(url_for('show_result'))

    return render_template('index.html')


@app.route('/result')
def show_result():
    if 'file_path' in session:
        file_path = session['file_path']
        df = pd.read_csv(file_path)
        return render_template('result.html',
                               table=df.to_html(index=False),
                               filename=file_path)
    else:
        return redirect(url_for('upload_file'))


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=False, port=PORT, host=HOST)