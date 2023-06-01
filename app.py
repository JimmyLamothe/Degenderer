# -*- coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
import sys
from pathlib import Path
from flask import Flask, request, redirect, render_template, send_file, session
import config 
from process_book import process_epub, get_names

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

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
      session['filepath'] = str(filepath)
      session['name_list'] = get_names(filepath)[:20]
      print(session['name_list'])
      return redirect('/pronouns')
    return redirect('/') #To reroute if someone enters the address directly

@app.route('/pronouns', methods=['GET', 'POST'])
def pronouns():
    def abbreviate(pronoun):
        if pronoun.lower() == 'non-binary':
            return 'nb'
        elif pronoun.lower() == 'female':
            return 'f'
        elif pronoun.lower() == 'male':
            return 'm'
        else:
            raise ValueError
    if request.method == 'POST':
        session['male_pronoun'] = abbreviate(request.form['male'])
        session['female_pronoun'] = abbreviate(request.form['female'])
        return redirect('/names')
    else:
        try:
            if session['filepath']:
                return render_template('pronouns.html')
            else:
                return redirect('/')
        except KeyError:
            return redirect('/')

@app.route('/names', methods=['GET', 'POST'])
def names():
    if request.method == 'POST':
        session['new_name_list'] = request.form.getlist('new_names[]')
        session['name_matches'] = {}
        for item in zip(session['name_list'], session['new_name_list']):
            if item[1]:
                session['name_matches'][item[0]] = item[1]
        parameters = {
            'male' : session['male_pronoun'],
            'female': session['female_pronoun'],
            'name matches': session['name_matches']
            }
        epub_filepath = process_epub(session['filepath'], parameters)        
        return send_file(epub_filepath)
    else:
        try:
            if session['male_pronoun'] and session['female_pronoun']:
                return render_template('names.html')
            else:
                return redirect('/')
        except KeyError:
            return redirect('/')

app.run(host='0.0.0.0', port=5001)
