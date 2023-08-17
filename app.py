# -*- coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
import sys
from pathlib import Path
from flask import Flask, jsonify, request, redirect, render_template, send_file, session
from markupsafe import escape
import config
from degenderer import suggest_name
from process_book import process_epub, process_text, get_known_names, get_potential_names

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

@app.route('/upload-book')
def upload_book():
    return render_template('upload-book.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        session['text'] = '' #Clear any text in memory from text box
        file = request.files['file']
        filepath = UPLOAD_DIR.joinpath(file.filename)
        file.save(filepath)
        session['filepath'] = str(filepath)
        known_names = get_known_names(filepath)
        print('known_names:', known_names)
        potential_names = get_potential_names(filepath)
        potential_names = [name for name in potential_names if not name in known_names]
        session['known_name_list'] = known_names
        print(session['known_name_list'])
        session['potential_name_list'] = potential_names[:30]
        print(session['potential_name_list'])
        session['name_matches'] = {}
        return redirect('/pronouns')
    return redirect('/') #To reroute if someone enters the address directly

@app.route('/text-upload', methods=['GET', 'POST'])
def text_upload():
    if request.method == 'POST':
        session['text'] = escape(request.form.get('text'))
        print(f'session text in text_upload: {session["text"]}')
        return redirect('/pronouns')
    return render_template('text-upload.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        modified_query = query.replace(' ', '+')
        start_url = 'https://www.gutenberg.org/ebooks/search/?query=>'
        end_url = '&submit_search=Go%21'
        search_url = start_url + modified_query + end_url
        return redirect(search_url)
    return render_template('search.html')

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
        try:
            if session['text']: #If we got here via text box input
                print(f'session text in pronouns: {session["text"]}')
                return redirect('/unknown-names')
        except KeyError:
            pass
        return redirect('/known-names') #If we got here via file upload
    else:
        try:
            if session['filepath'] or session['text']:
                return render_template('pronouns.html')
            else:
                return redirect('/')
        except KeyError:
            return redirect('/')

@app.route('/known-names', methods=['GET', 'POST'])
def known_names():
    if request.method == 'POST':
        print('known names POST - session name matches:', session['name_matches'])
        new_name_list = request.form.getlist('new_names[]')
        print('known names - new names:', new_name_list)
        for item in zip(session['known_name_list'], new_name_list):
            if item[1]:
                session['name_matches'][item[0]] = item[1]
        session.modified = True
        print('known names - name matches', session['name_matches'])
        return redirect('/potential-names')
    else:
        try:
            print('known names GET - session name matches:', session['name_matches'])
            if session['male_pronoun'] and session['female_pronoun']:
                return render_template('known-names.html')
            else:
                return redirect('/')
        except KeyError:
            return redirect('/')
        
@app.route('/potential-names', methods=['GET', 'POST'])
def potential_names():
    if request.method == 'POST':
        print('potential names POST - session name matches:', session['name_matches'])
        new_name_list = request.form.getlist('new_names[]')
        for item in zip(session['potential_name_list'], new_name_list):
            if item[1]:
                session['name_matches'][item[0]] = item[1]
        session.modified = True
        return redirect('/unknown-names')
    else:
        try:
            print('potential names GET - session name matches:', session['name_matches'])
            if session['male_pronoun'] and session['female_pronoun']:
                return render_template('potential-names.html')
            else:
                return redirect('/')
        except KeyError:
            return redirect('/')

@app.route('/unknown-names', methods=['GET', 'POST'])
def unknown_names():
    if request.method == 'POST':
        print('unknown names POST - session name matches:', session['name_matches'])
        unknown_name_list = request.form.getlist('existing_names[]')
        new_name_list = request.form.getlist('new_names[]')
        for item in zip(unknown_name_list, new_name_list):
            if item[0] and item[1]:
                session['name_matches'][item[0]] = item[1]
        session.modified = True
        parameters = {
            'male' : session['male_pronoun'],
            'female': session['female_pronoun'],
            'name matches': session['name_matches'],
            'verbose': True
            }
        try:
            if session['text']: #If we got here via text box input
                session['text'] = process_text(escape(session['text']))
                #We escape a second time in case the session cookie was hacked
                return redirect('/text-display')
        except KeyError: #If we got here via file upload
            pass
        epub_filepath = process_epub(session['filepath'], parameters)        
        return send_file(epub_filepath)
    else:
        try:
            print('unknown names GET - session name matches:', session['name_matches'])
            if session['male_pronoun'] and session['female_pronoun']:
                return render_template('unknown-names.html')
            else:
                return redirect('/')
        except KeyError:
            return redirect('/')

@app.route('/text-display', methods=['GET'])
def text_display():
    try:
        if session['text']:
            return render_template('text-display.html')
    except KeyError:
        pass
    return redirect('/') #If we don't have text to display, go to home page
        
@app.route('/suggest-nb', methods=['POST'])
def suggest_nb():
    suggestion = suggest_name('nb')
    return jsonify({'suggested_name': suggestion})

@app.route('/suggest-female', methods=['POST'])
def suggest_female():
    suggestion = suggest_name('f')
    return jsonify({'suggested_name': suggestion})

@app.route('/suggest-male', methods=['POST'])
def suggest_male():
    suggestion = suggest_name('m')
    return jsonify({'suggested_name': suggestion})

app.run(host='0.0.0.0', port=5001)
