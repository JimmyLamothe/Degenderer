# -*- coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
import sys
import random
from pathlib import Path
import requests
from flask import Flask, jsonify, request, redirect, render_template, send_file, session
from markupsafe import escape
import config
from degenderer import suggest_name
from utilities import remove_dupes
from samples import add_sample, get_sample_by_id, get_samples
import process_book
import process_text

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

SAMPLE_DIR = Path('sample_books') #eBooks submitted by users and downloaded at least once
WORKING_DIR = Path('temp') #Used to temporarily store downloaded eBooks
UPLOAD_DIR = Path('uploads') #Used to temporarily store uploaded eBooks - Combine with WORKING_DIR?

EMPTY_PARAMETERS = 'empty_dict.json'

def clear_session():
    session['text'] = '' #Text input by user for degendering
    session['filepath'] = '' #Filepath of book uploaded by user
    session['known_name_list'] = [] #Known names detected in user submission
    session['potential_name_list'] = [] #Potential names detected in user submission
    session['pronoun_matches'] = {} #Current pronoun matches
    session['known_matches'] = {} #Current known name matches
    session['potential_matches'] = {} #Current potential name matches
    session['unknown_matches'] = {} #Current matches for words submitted by user
    session['all_matches'] = {} #Final matches submitted for degendering
    session['male_pronoun'] = '' #Gender to make male pronouns
    session['female_pronoun'] = '' #Gender to make female pronouns
    try:
        if not session['samples']:
            session['samples'] = [] #We do not want to clear the samples when clearing the session
    except KeyError:
        session['samples'] = [] #Samples not yet displayed to user
    session.modified=True

#Update all matches with current user choices
def update_matches(user_matches=None):
    session['all_matches'] = {}
    session['all_matches'].update(session['pronoun_matches'])
    session['all_matches'].update(session['known_matches'])
    session['all_matches'].update(session['potential_matches'])
    if user_matches:
        session['all_matches'].update(user_matches)
    else: #Just for safety, normally this updates with an empty dict
        session['all_matches'].update(session['unknown_matches'])
    session.modified=True
    
@app.route('/')
@app.route('/home')
@app.route('/welcome')
def welcome():
    clear_session()
    return render_template('welcome.html')
  
@app.route('/samples')
def samples():
    clear_session()
    samples = get_samples()
    number = 10
    if len(samples) > number:
        selection = random.sample(samples, number)
    else:
        selection = samples
    session['samples'] = [item for item in samples if not item in selection]
    session.modified=True
    return render_template('samples.html', selection=selection)

@app.route('/download-sample/<sample_id>')
def download_sample(sample_id):
    sample = get_sample_by_id(sample_id)
    url = sample['webpage']
    book_filename = url.split("/")[-1]
    degendered_filepath = SAMPLE_DIR / book_filename
    if not degendered_filepath.exists():
        temp_filepath = WORKING_DIR / book_filename
        # Download the book using requests if it doesn't exist
        response = requests.get(url)
        with open(temp_filepath, 'wb') as f:
            f.write(response.content)
        parameters = {
            'male' : sample['male pronouns'],
            'female': sample['female pronouns'],
            'name matches': sample['name matches'],
        }
        epub_filepath = process_book.process_epub(temp_filepath, parameters)
        epub_filepath.rename(degendered_filepath)
        temp_filepath.unlink()
    return send_file(degendered_filepath)

@app.route('/upload-book')
def upload_book():
    clear_session()
    return render_template('upload-book.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filepath = UPLOAD_DIR.joinpath(file.filename)
        file.save(filepath)
        session['filepath'] = str(filepath)
        all_names = process_book.get_all_names(filepath)
        known_names = all_names[0]
        potential_names = all_names[1]
        session['known_name_list'] = known_names
        session['potential_name_list'] = potential_names[:50] #Top 50 potential names
        return redirect('/pronouns')
    return redirect('/') #To reroute if someone enters the address directly

@app.route('/text-upload', methods=['GET', 'POST'])
def text_upload():
    if request.method == 'POST':
        session['text'] = escape(request.form.get('text'))
        all_names = process_text.get_all_names(session['text'])
        print(f'all_names: {all_names}')
        known_names = all_names[0]
        potential_names = all_names[1]
        session['known_name_list'] = known_names
        session['potential_name_list'] = potential_names[:30]
        return redirect('/pronouns')
    #If GET
    clear_session()
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
    #If GET
    clear_session()
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
        if session['male_pronoun'] == 'nb':
            session['pronoun_matches']['he'] = request.form['he'].lower()
            session['pronoun_matches']['him'] = request.form['him'].lower()
            session['pronoun_matches']['his'] = request.form['his'].lower()
            session['pronoun_matches']['himself'] = request.form['himself'].lower()
        if session['female_pronoun'] == 'nb':
            session['pronoun_matches']['she'] = request.form['she'].lower()
            session['pronoun_matches']['her'] = request.form['her'].lower()
            session['pronoun_matches']['hers'] = request.form['hers'].lower()
            session['pronoun_matches']['herself'] = request.form['herself'].lower()
        update_matches()
        return redirect('/known-names') #If file upload
    #If GET
    if session['filepath']: #If file upload
        return render_template('pronouns.html')
    if session['text']: #If text input
        return render_template('pronouns.html')
    else: #If URL accessed improperly
        return redirect('/')

@app.route('/known-names', methods=['GET', 'POST'])
def known_names():
    if request.method == 'POST':
        submit_type = request.form.get('submit_type', 'submit')
        print(submit_type)
        new_name_list = request.form.getlist('new_names[]')
        for item in zip(session['known_name_list'], new_name_list):
            if item[1]:
                session['known_matches'][item[0]] = item[1]
        session.modified=True
        if submit_type == 'back': #If user clicked back button
            return redirect('/pronouns')
        #If user clicked submit button
        return redirect('/potential-names')
    #If GET
    if not session['male_pronoun'] and session['female_pronoun']: #If user typed url directly
        return redirect('/')
    if session['known_name_list']:
        return render_template('known-names.html')
    else:
        return redirect('/potential-names')
        
@app.route('/potential-names', methods=['GET', 'POST'])
def potential_names():
    if request.method == 'POST':
        submit_type = request.form.get('submit_type', 'submit')
        new_name_list = request.form.getlist('new_names[]')
        for item in zip(session['potential_name_list'], new_name_list):
            if item[1]:
                session['potential_matches'][item[0]] = item[1]
        session.modified=True
        if submit_type == 'back': #If user clicked back button
            if session['known_name_list']:
                return redirect('/known-names')
            else:
                return redirect('/pronouns')
        #If user clicked submit button
        return redirect('/unknown-names')
    else:
        if not session['male_pronoun'] and session['female_pronoun']: #If user typed url directly
            return redirect('/')
        if session['potential_name_list']:
            return render_template('potential-names.html')
        else:
            return redirect('/unknown-names')

@app.route('/unknown-names', methods=['GET', 'POST'])
def unknown_names():
    if request.method == 'POST':
        submit_type = request.form.get('submit_type', 'submit')
        unknown_name_list = request.form.getlist('existing_names[]')
        new_name_list = request.form.getlist('new_names[]')
        for item in zip(unknown_name_list, new_name_list):
            if item[0] and item[1]:
                session['unknown_matches'][item[0]] = item[1]
        session.modified=True
        if submit_type == 'back': #If user clicked back button
            if session['potential_name_list']:
                return redirect('/potential-names')
            elif session['known_name_list']:
                return redirect('/known-names')
            else:
                return redirect('/pronouns')
        #If user clicked submit button
        lower_dict = {(key.lower(), value.lower())
                      for (key, value) in session['unknown_matches'].items()}
        title_dict = {(key.title(), value.title())
                      for (key, value) in session['unknown_matches'].items()}
        upper_dict = {(key.upper(), value.upper())
                      for (key, value) in session['unknown_matches'].items()}
        user_matches = {}
        user_matches.update(lower_dict)
        user_matches.update(title_dict)
        user_matches.update(upper_dict)
        update_matches(user_matches=user_matches) #Updating session['all_matches'] with final values 
        parameters = {
            'male' : session['male_pronoun'],
            'female': session['female_pronoun'],
            'all matches': session['all_matches'],
            }
        try:
            if session['text']: #If we got here via text box input
                print(session['text'])
                #We escape a second time in case the session cookie was hacked
                session['text'] = process_text.process_text(escape(session['text']),
                                                            parameters)
                #print(f'session text: {session["text"]}')
                return redirect('/text-display')
        except KeyError: #If we got here via file upload
            pass
        try:
            epub_filepath = process_book.process_epub(session['filepath'], parameters)
        except Exception as e:
            #raise e #Uncomment to diagnose exception
            return redirect('/processing-error')
        return send_file(epub_filepath, as_attachment=True)
    else:
        print(session['unknown_matches'])
        num_entries = (max(10, len(session['unknown_matches'])))
        try:
            if session['male_pronoun'] and session['female_pronoun']:
                return render_template('unknown-names.html', num_entries=num_entries)
            else:
                return redirect('/')
        except KeyError:
            return redirect('/')

@app.route('/submission-form', methods=['GET', 'POST'])
def submission_form():
    if request.method == 'POST':
        book_name = request.form['book_name']
        author = request.form['author']
        webpage = request.form['webpage']
        tags = request.form['tags']
        excerpt = request.form['excerpt']

        # Save the submitted data (you can store it in a database or file)
        submitted_book = {
            'book_name': book_name,
            'author': author,
            'webpage': webpage,
            'tags': tags,
            'excerpt': excerpt,
            'male pronouns': session['male_pronoun'],
            'female pronouns': session['female_pronoun'],
            'name matches': session['all_matches'],
            'reviewed': False,
            'approved': False
        }
        add_sample(submitted_book)
        print(get_samples(reviewed=False, approved=False))
        return redirect('/thank-you')

    return render_template('submission-form.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')
        
@app.route('/text-display', methods=['GET'])
def text_display():
    try:
        if session['text']:
            #print(f'session text in text_display: {session["text"]}')
            return render_template('text-display.html')
    except KeyError:
        pass
    return redirect('/') #If we don't have text to display, go to home page

def get_suggestion(gender):
    #print(f'Working on row {request.json.get("row")}')
    page_suggestions = request.json.get('pageSuggestions')
    saved_suggestions = list(session['all_matches'].values())
    names_used = list(set(page_suggestions + saved_suggestions))
    suggestion = suggest_name(gender, names_used)
    return jsonify({'suggested_name': suggestion})

@app.route('/suggest-nb', methods=['POST'])
def suggest_nb():
    return get_suggestion('nb')

@app.route('/suggest-female', methods=['POST'])
def suggest_female():
    return get_suggestion('f')

@app.route('/suggest-male', methods=['POST'])
def suggest_male():
    return get_suggestion('m')

@app.route('/processing-error')
def processing_error():
    return render_template('processing-error.html')

@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400

@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(503)
def unavailable(e):
    return render_template('503.html'), 503

@app.route('/test-error/<error>')
def test_error(error):
    return render_template(f'{error}.html')

app.run(host='0.0.0.0', port=5001)
