"""
Main module for the web app.

Functions:
    clear_session: Clear session memory when needed
    

"""
import gevent.monkey
gevent.monkey.patch_all()
import os
from pathlib import Path
import gevent
import requests
from flask import Flask, jsonify, request, redirect, render_template, send_file, session, url_for
from flask import copy_current_request_context
from flask_session import Session
from flask_sse import sse
from markupsafe import escape
import config
from degenderer import suggest_name
from reference_library import get_number_of_pronouns
from samples import add_book, add_sample, get_book_count, get_sample_by_id, get_sample_ids
from samples import increment_download_count
from utilities import url_to_epub, compare_dicts
import process_book
import process_text

app = Flask(__name__)

app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SESSION_TYPE'] = config.SESSION_TYPE
app.config['SESSION_PERMANENT'] = config.SESSION_PERMANENT
app.config['SESSION_USE_SIGNER'] = config.SESSION_USE_SIGNER
app.config['SESSION_REDIS'] = config.SESSION_REDIS
app.config["REDIS_URL"] = config.REDIS_URL

Session(app)

app.register_blueprint(sse, url_prefix='/stream')

SAMPLE_DIR = Path(os.environ.get('SAMPLE_DIR', 'sample_books'))
WORKING_DIR = Path(os.environ.get('WORKING_DIR', 'temp'))
for item in WORKING_DIR.iterdir():
    item.unlink()

PER_PAGE = 5 #Samples to load per page

def clear_session(clear_samples=False, same_book=False):
    """ Clear user session info when needed. """
    session['text'] = '' #Text input by user for degendering
    session['new_text'] = '' #Text output
    if not same_book: #If working on a new book (versus modifying)
        session['filepath'] = '' #Filepath of book uploaded by user
        session['output_filepath'] = '' #Filepath of degendered book
        session['known_name_list'] = [] #Known names detected in user submission
        session['potential_name_list'] = [] #Potential names detected in user submission
    session['pronoun_matches'] = {} #Current pronoun matches
    session['known_matches'] = {} #Current known name matches
    session['potential_matches'] = {} #Current potential name matches
    session['unknown_matches'] = {} #Current matches for words submitted by user
    session['all_matches'] = {} #Final matches submitted for degendering
    session['male_pronouns'] = '' #Gender to make male pronouns
    session['female_pronouns'] = '' #Gender to make female pronouns
    session['latest_filepath'] = '' #Filepath of latest user-modified book version
    session['latest_all_matches'] = {} #All matches for latest user-modified book version
    session['latest_female_pronouns'] = '' #Female pronouns for latest user-modified book version
    session['latest_male_pronouns'] = '' #Male pronouns for latest user-modified book version
    try:
        if clear_samples: #Reset samples to be displayed
            session['sample_ids'] = get_sample_ids()
            session['sample_index'] = 0
        else: #Leave as is, but check if they have been initialized
            session['sample_ids'] #To trigger KeyError if it hasn't been initialized
            session['sample_index'] #To trigger KeyError if it hasn't been initialized
    except KeyError: #Default values on initialization
        session['sample_ids'] = get_sample_ids()
        session['sample_index'] = 0
    session.modified=True

def update_matches(user_matches=None):
    """ Update all matches with current user choices """
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
    """ Route to web app home page """
    clear_session(clear_samples=True)
    return render_template('welcome.html', books_processed=get_book_count())

@app.route('/samples')
def samples():
    """ Route to samples page with book examples """
    clear_session()
    sample_ids = session['sample_ids']
    start = session['sample_index']
    if (start + PER_PAGE) < len(sample_ids): #If there are more samples to load
        end = start + PER_PAGE
        more = True
    else:
        end = len(sample_ids)
        more = False
    selected_ids = sample_ids[start:end]
    previous = bool(start - PER_PAGE >= 0)
    session.modified=True #For safety only in case of future code changes
    selection = []
    for sample_id in selected_ids:
        selection.append(get_sample_by_id(sample_id, keep_abbreviations=False))
    return render_template('samples.html', selection=selection, more=more, previous=previous)

@app.route('/samples/more')
def more_samples():
    """ Route to load more book examples """
    session['sample_index'] = session['sample_index'] + PER_PAGE
    return redirect('/samples')

@app.route('/samples/previous')
def previous_samples():
    """ Route to navigate to previous page of book examples """
    session['sample_index'] = session['sample_index'] - PER_PAGE
    return redirect('/samples')

@app.route('/download-sample/<sample_id>')
def download_sample(sample_id):
    """ Route to download the eBook related to a sample """
    sample = get_sample_by_id(sample_id)
    url = sample['webpage']
    parameters = {
        'male' : sample['male pronouns'],
        'female': sample['female pronouns'],
        'all matches': sample['all matches'],
    }
    book_filename = url_to_epub(url)
    degendered_filepath = process_book.get_output_filepath(SAMPLE_DIR / book_filename,
                                                            parameters,
                                                            destination=SAMPLE_DIR)
    print(f'degendered_filepath: {degendered_filepath}')
    if not degendered_filepath.exists():
        temp_filepath = WORKING_DIR / book_filename
        session['output_filepath'] = degendered_filepath
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.Timeout:
            return render_template('504.html')
        except requests.RequestException as e:
            app.logger.error(e)
            return render_template('504.html')
        with open(temp_filepath, 'wb') as f:
            f.write(response.content)
        @copy_current_request_context
        def task(temp_filepath, parameters, session_id=None):
            try:
                epub_filepath = process_book.process_epub(temp_filepath, parameters, session_id=session_id)
                epub_filepath.rename(degendered_filepath)
                temp_filepath.unlink()
            except Exception as e: # pylint: disable=broad-except
                app.logger.error(e)
                #raise e #Uncomment to diagnose exception
                if session_id:
                    sse.publish({'message':'processing error'}, type='processing_error', channel=session_id)
            if session_id:
                sse.publish({'message':'book_processed'}, type='book_processed', channel=session_id)
        gevent.spawn(task, temp_filepath, parameters, session_id=session.sid)
        return redirect(url_for('processing', is_sample=True))
    increment_download_count(sample_id)
    return send_file(degendered_filepath)

@app.route('/upload-book')
def upload_book():
    """ Route to upload a book for de/regendering - GET """
    clear_session()
    return render_template('upload-book.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    """ Route to upload a book for de/regendering - POST """
    if request.method == 'POST':
        file = request.files['file']
        filepath = WORKING_DIR.joinpath(file.filename)
        file.save(filepath)
        session['filepath'] = str(filepath)
        all_names = process_book.get_all_names(filepath)
        session['known_name_list'] = all_names[0] #All known names
        session['potential_name_list'] = all_names[1][:50] #Top 50 potential names
        return redirect('/pronouns')
    return redirect('/') #To reroute if someone enters the address directly

@app.route('/text-upload', methods=['GET', 'POST'])
def text_upload():
    """ Route to submit text for de/regendering """
    if request.method == 'POST':
        session['text'] = escape(request.form.get('text'))
        all_names = process_text.get_all_names(session['text'])
        session['known_name_list'] = all_names[0] #All known names
        session['potential_name_list'] = all_names[1][:30] #Top 30 potential names
        return redirect('/pronouns')
    #If GET
    clear_session()
    return render_template('text-upload.html')

@app.route('/search')
def search():
    """ Route to search for a book on Project Gutenberg """
    clear_session()
    return render_template('search.html')

@app.route('/start-over')
def start_over():
    """ Route to keep working on the same book but starting from scratch """
    clear_session(same_book=True)
    return redirect('pronouns')

@app.route('/pronouns', methods=['GET', 'POST'])
def pronouns():
    """ Route to define pronouns matches for the book or text """
    def abbreviate(pronoun):
        if pronoun.lower() == 'non-binary':
            return 'nb'
        if pronoun.lower() == 'female':
            return 'f'
        if pronoun.lower() == 'male':
            return 'm'
        raise ValueError
    if request.method == 'POST':
        session['male_pronouns'] = abbreviate(request.form['male'])
        session['female_pronouns'] = abbreviate(request.form['female'])
        if session['male_pronouns'] == 'nb':
            session['pronoun_matches']['he'] = request.form['he'].lower()
            session['pronoun_matches']['him'] = request.form['him'].lower()
            session['pronoun_matches']['his'] = request.form['his'].lower()
            session['pronoun_matches']['himself'] = request.form['himself'].lower()
        if session['female_pronouns'] == 'nb':
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
    return redirect('/') #If URL accessed improperly

@app.route('/known-names', methods=['GET', 'POST'])
def known_names():
    """ Route to define matches for names in our list of common names """
    if request.method == 'POST':
        submit_type = request.form.get('submit_type', 'submit')
        new_name_list = request.form.getlist('new_names[]')
        for item in zip(session['known_name_list'], new_name_list):
            if item[1]: #If user gave a match for a name, add it to dict
                session['known_matches'][item[0]] = item[1]
            else:
                try: #If user came back and deleted a match, remove it from dict
                    del session['known_matches'][item[0]]
                except KeyError: #If user never gave a match, do nothing
                    pass
        session.modified=True
        if submit_type == 'back': #If user clicked back button
            return redirect('/pronouns')
        #If user clicked submit button
        return redirect('/potential-names')
    #If GET
    if not session['male_pronouns'] and session['female_pronouns']: #If user typed url directly
        return redirect('/')
    if session['known_name_list']:
        return render_template('known-names.html')
    return redirect('/potential-names')

@app.route('/potential-names', methods=['GET', 'POST'])
def potential_names():
    """ Route to define matches for common capital words that could be names """
    if request.method == 'POST':
        submit_type = request.form.get('submit_type', 'submit')
        new_name_list = request.form.getlist('new_names[]')
        for item in zip(session['potential_name_list'], new_name_list):
            if item[1]: #If user gave a match for a name, add it to dict
                session['potential_matches'][item[0]] = item[1]
            else:
                try: #If user came back and deleted a match, remove it from dict
                    del session['potential_matches'][item[0]]
                except KeyError: #If user never gave a match, do nothing
                    pass
        session.modified=True
        if submit_type == 'back': #If user clicked back button
            if session['known_name_list']:
                return redirect('/known-names')
            return redirect('/pronouns')
        #If user clicked submit button
        return redirect('/unknown-names')
    else:
        if not session['male_pronouns'] and session['female_pronouns']: #If user typed url directly
            return redirect('/')
        if session['potential_name_list']:
            return render_template('potential-names.html')
        return redirect('/unknown-names')
    
@app.route('/unknown-names', methods=['GET', 'POST'])
def unknown_names():
    """ Route to define matches for user submitted words """
    if request.method == 'POST':
        submit_type = request.form.get('submit_type', 'submit')
        unknown_name_list = request.form.getlist('existing_names[]')
        new_name_list = request.form.getlist('new_names[]')
        for item in zip(unknown_name_list, new_name_list):
            if item[0] and item[1]: #If user gave a name and match, add them to dict
                session['unknown_matches'][item[0]] = item[1]
            elif item[0]:
                try: #If user came back and deleted a match, remove it from dict
                    del session['unknown_matches'][item[0]]
                except KeyError: #If user never gave a match, do nothing
                    pass
        session.modified=True
        if submit_type == 'back': #If user clicked back button
            if session['potential_name_list']:
                return redirect('/potential-names')
            if session['known_name_list']:
                return redirect('/known-names')
            return redirect('/pronouns')
        #If user clicked submit button
        user_matches = {(key.lower(), value.lower())
                      for (key, value) in session['unknown_matches'].items()}
        update_matches(user_matches=user_matches) #Updating session['all_matches'] with final values
        parameters = {
            'male' : session['male_pronouns'],
            'female': session['female_pronouns'],
            'all matches': session['all_matches'],
            'modifying': False
            }
        try:
            if session['text']: #If we got here via text box input
                #We escape a second time in case the session cookie was hacked
                session['new_text'] = process_text.process_text(escape(session['text']),
                                                            parameters)
                return redirect('/text-display')
        except KeyError: #If we got here via file upload
            pass
        filepath = session['filepath']
        if session['latest_filepath']: #If user is modifying a previous submission
            if (session['latest_female_pronouns'] == session['female_pronouns'] and
                session['latest_male_pronouns'] == session['male_pronouns']):
                #NOTE: There are so many more standard gendered words to replace than user matches
                #that modifying should always be faster. We are just keeping it here in case
                #we later choose to offer a turbo conversion process with a reduced pronoun list
                comparison = compare_dicts(session['latest_all_matches'], session['all_matches'])
                matching_keys, modified_keys_old, modified_keys_new, new_keys, removed_keys = comparison
                changed_values = len(modified_keys_old) + len(new_keys) + len(removed_keys)
                unchanged_values = len(matching_keys)
                number_of_pronouns = get_number_of_pronouns(session['male_pronouns'],
                                                            session['female_pronouns'])
                if changed_values < unchanged_values + number_of_pronouns: #If few modifications
                    parameters['modifying'] = True #To not change pronouns again
                    filepath = session['latest_filepath'] #Start from latest version
                    all_matches = {}
                    for key, value in new_keys.items():
                        all_matches.update(new_keys) #Add new matches
                    for key, value in removed_keys.items():
                        all_matches[value] = key #Revert removed matches
                    for key, value in modified_keys_old.items(): #Adapt modified matches
                        all_matches[modified_keys_old[key]] = modified_keys_new[key]
                    parameters['all matches'] = all_matches #Use latest changes only
        session['output_filepath'] = process_book.get_output_filepath(filepath, parameters)
        session['latest_all_matches'] = dict(session['all_matches'])
        session['latest_female_pronouns'] = session['female_pronouns']
        session['latest_male_pronouns'] = session['male_pronouns']
        @copy_current_request_context
        def task(filepath, parameters, session_id=None):
            print(f'parameters["modifying"] = {parameters.get("modifying", "Key absent")}')
            try:
                epub_filepath = process_book.process_epub(filepath, parameters, session_id=session_id)
            except Exception as e: # pylint: disable=broad-except
                app.logger.error(e)
                #raise e #Uncomment to diagnose exception
                if session_id:
                    sse.publish({'message':'processing error'}, type='processing_error', channel=session_id)
            try:
                filename = epub_filepath.name
                address = request.remote_addr
                add_book(filepath, address) #Add filename / IP combination to processed books database
                #Not important if it fails, so simply log the exception
            except Exception as e: # pylint: disable=broad-except
                app.logger.error(e)
            if session_id:
                sse.publish({'message':'book_processed'}, type='book_processed', channel=session_id)
        gevent.spawn(task, filepath, parameters, session_id=session.sid)
        return redirect('/processing')
    else:
        num_entries = (max(10, len(session['unknown_matches'])))
        #To make sure user didn't get here by typing the url directly
        try:
            if session['male_pronouns'] and session['female_pronouns']:
                return render_template('unknown-names.html', num_entries=num_entries)
            return redirect('/')
        except KeyError:
            return redirect('/')

@app.route('/processing')
def processing():
    """ Route for communicating degendering progress to user """
    is_sample = request.args.get('is_sample', False)
    return render_template('processing.html', is_sample=is_sample)

@app.route('/send-book')
def send_book():
    """ Route to send degendered book to user """
    if not session['output_filepath']:
        return redirect('/')
    if os.path.exists(str(session['output_filepath'])):
        session['latest_filepath'] = session['output_filepath']
        session['output_filepath'] = ''
        print(f'latest_filepath: {session["latest_filepath"]}')
        print(f'latest_all_matches: {session["latest_all_matches"]}')
        print(f'latest_male_pronouns: {session["latest_male_pronouns"]}')
        print(f'latest_female_pronouns: {session["latest_female_pronouns"]}')
        return send_file(session['latest_filepath'])
    return redirect('/500')

@app.route('/submission-form', methods=['GET', 'POST'])
def submission_form():
    """ Route for user to submit a sample """
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        webpage = request.form['webpage']
        tagline = request.form['tagline']
        excerpt = request.form['excerpt']
        # Save the submitted data (you can store it in a database or file)
        submitted_book = {
            'title': title,
            'author': author,
            'webpage': webpage,
            'tagline': tagline,
            'excerpt': excerpt,
            'male pronouns': session['male_pronouns'],
            'female pronouns': session['female_pronouns'],
            'all matches': session['all_matches'],
            'reviewed': False,
            'approved': False
        }
        add_sample(submitted_book)
        return redirect('/thank-you')
    return render_template('submission-form.html')

@app.route('/thank-you')
def thank_you():
    """ Route to thank a user for their submission """
    return render_template('thank-you.html')

@app.route('/text-display', methods=['GET'])
def text_display():
    """ Route to display de/regendered text """
    if session['new_text']:
        return render_template('text-display.html')
    return redirect('/') #If we don't have text to display, go to home page

def get_suggestion(gender):
    """ Route to get a name suggestion for a given gender """
    page_suggestions = request.json.get('pageSuggestions')
    saved_suggestions = list(session['all_matches'].values())
    names_used = list(set(page_suggestions + saved_suggestions))
    suggestion = suggest_name(gender, names_used)
    return jsonify({'suggested_name': suggestion})

@app.route('/suggest-nb', methods=['POST'])
def suggest_nb():
    """ Route to suggest a non-binary name """
    return get_suggestion('nb')

@app.route('/suggest-female', methods=['POST'])
def suggest_female():
    """ Route to suggest a female name """
    return get_suggestion('f')

@app.route('/suggest-male', methods=['POST'])
def suggest_male():
    """ Route to suggest a male name """
    return get_suggestion('m')

@app.route('/processing-error')
def processing_error():
    """ Route to let the user know book processing failed """
    return render_template('processing-error.html')

@app.errorhandler(400)
def bad_request(_e):
    """ Route for 400 bad request errors """
    return render_template('400.html'), 400

@app.errorhandler(401)
def unauthorized(_e):
    """ Route for 401 unauthorized errors """
    return render_template('401.html'), 401

@app.errorhandler(403)
def forbidden(_e):
    """ Route for 403 forbidden errors """
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(_e):
    """ Route for 404 page not found errors """
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """ Route for 500 server error errors """
    app.logger.error(e)
    return render_template('500.html'), 500

@app.errorhandler(503)
def unavailable(e):
    """ Route for 503 unavailable errors """
    app.logger.error(e)
    return render_template('503.html'), 503

@app.errorhandler(504)
def unavailable(e):
    """ Route for 504 gateway timeout errors """
    app.logger.error(e)
    return render_template('504.html'), 503

@app.route('/test-error/<error>')
def test_error(error):
    """ Route to test display of specific error pages """
    return render_template(f'{error}.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
