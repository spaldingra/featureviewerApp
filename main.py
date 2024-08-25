## main python for featureviewer app
## Author: Reid Spalding
## Ver. 0.0
## Updated: Aug. 25, 2024

## imports
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired


## flask app creation
app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

## upload file 
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

## main page
@app.route('/', methods=('GET', 'POST'))
def index():
    form = UploadFileForm()
    if form.validate_on_submit():
        #get file, save file, return comf.
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        return redirect(url_for('featureviewer'))
    return render_template('index.html', form=form)

@app.route('/featureviewer', methods=('GET', 'POST'))
def featureviewer():
    return render_template('featureviewer.html')

## call main
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')