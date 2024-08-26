## main python for featureviewer app
## Author: Reid Spalding
## Ver. 0.2
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
ALLOWED_EXTENSIONS = {'fasta', 'bam'}

## check file upload extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

## init home page
@app.route('/')
def index():
    reset_results()
    return render_template('index.html')


## file upload
@app.route('/upload', methods=['POST'])
def upload_file():

    ##check inputs
    if 'file1' not in request.files or 'file2' not in request.files:
        flash('Both files must be uploaded!')
        return redirect(request.url)
    
    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        flash('Both files must be selected!')
        return redirect(request.url)

    ## check extentions
    if allowed_file(file1.filename) and allowed_file(file2.filename):
        filename1 = file1.filename
        filename2 = file2.filename

        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)

        file1.save(filepath1)
        file2.save(filepath2)

        ## run code on files
        result = process_files(filepath1, filepath2)

        if result:
            return redirect(url_for('results'))

    flash('File not allowed or error in processing!')
    return redirect(request.url)

@app.route('/results')
def results():
    return render_template('results.html')

## viewer test
@app.route('/viewer')
def viewer():
    return render_template('viewer.html')


## file process def
def process_files(bam, fasta):

    outfile = 'output.vcf.gz'
    get_vcf(bam, fasta, outfile)
    result = get_feats(outfile)
    return result
    

## convert bam script
def get_vcf(bam, fasta, outfile):

    try:
        result = subprocess.run(
            ['python', 'bam2vcf.py', bam, fasta, outfile],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()

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