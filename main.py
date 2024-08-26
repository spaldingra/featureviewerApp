## main python for featureviewer app
## Author: Reid Spalding
## Ver. 0.1
## Updated: Aug. 25, 2024

## imports
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

## set upload path
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

## file extension checking
ALLOWED_EXTENSIONS = {'gz', 'vcf'}

## check file upload extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

## init home page
@app.route('/')
def index():
    reset_results()
    return render_template('index.html')

## init upload page
@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        ## run feature viewer
        result = get_feats(filepath)

        if result:

            return redirect(url_for('results'))

        else:
            return render_template('index.html', result=result)

    flash('File not allowed')
    return redirect(request.url)

@app.route('/results')
def results():
    return render_template('results.html')

## convert bam script
def get_vcf(bam, fasta):

    try:
        result = 0

    except Exception as e:
        return f"An error occurred: {e}"

## feature viewer script
def get_feats(filepath):
    ## run featureviewer.py
    try:
        result = subprocess.run(
            ['python', 'featureviewer.py', filepath],  # Pass the file path to the script
            capture_output=True, 
            text=True
        )
        return result.stdout.strip()  # Return the output of the script
    except Exception as e:
        return f"An error occurred: {e}"
    
## reset results page
def reset_results():
    f = open('templates/results.html', 'w')
    init = open('templates/init.txt', 'r')

    data = init.read()
    init.close()

    f.write(data)
    f.close()

## call main
if __name__ == '__main__':

    reset_results()
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0')