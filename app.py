import sys
from pathlib import Path
from flask import Flask, request, redirect, render_template, send_file

from process_epub import process_epub

app = Flask(__name__)

SAMPLE_DIR = Path('samples') 

UPLOAD_DIR = Path('uploads')

EMPTY_PARAMETERS = 'empty_dict.json'

@app.route('/')
@app.route('/home')
def home():
  return render_template('welcome.html')

@app.route('/samples')
def samples():
  return render_template('samples.html')

@app.route('/download/<filename>')
def download(filename):
  filename = filename + '.epub'
  return send_file(SAMPLE_DIR.joinpath(filename), as_attachment=True)

@app.route('/select')
def select_book():
  return render_template('select_js.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
  if request.method == 'POST':
    file = request.files['file']
    filepath = UPLOAD_DIR.joinpath(file.filename)
    file.save(filepath)
    epub_filepath = process_epub(filepath, EMPTY_PARAMETERS)
    return send_file(epub_filepath)
  return redirect('/')

app.run(host='0.0.0.0', port=5001)
