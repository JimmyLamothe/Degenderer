"""
This module manages user-submitted de/regendered book samples

submitted book format:
{
    'title': request.form['title'],
    'author': request.form['author'],
    'webpage': request.form['webpage'],
    'tags': request.form['tags'],
    'excerpt': request.form['excerpt'],
    'male pronouns': session['male_pronouns'],
    'female pronouns': session['female_pronouns'],
    'all matches': session['all_matches'],
    'reviewed': False,
    'approved': False
}
"""

import os
import json
import sqlite3
import random
from pathlib import Path

DB_FOLDER = Path(os.environ.get('DATABASE_PATH', 'databases'))

def get_db_conn(db_name):
    """ Connect to a database """
    db_path = DB_FOLDER / db_name
    conn = sqlite3.connect(db_path)
    return conn

def initialize_books_database():
    """ Used once to initialize the database of processed books
    
    filename is the degendered filename, including pronoun extension
    address is the user ip address
    words is the total number of words in the book
    matches is the number of words to degender
    time is the time it took to do the degendering
    """
    conn = get_db_conn('processed_books.db')
    cursor = conn.cursor()

    # Create a table to store processed books data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_books (
            id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL,
            address TEXT NOT NULL,
            words INTEGER NOT NULL,
            matches INTEGER NOT NULL,
            time INTEGER NOT NULL,
            UNIQUE(filename, address)
        )
    ''')

    conn.commit()
    conn.close()

if not (DB_FOLDER/'processed_books.db').exists():
    initialize_books_database()

def initialize_sample_database():
    """ Used once to initialize the database of book samples """
    conn = get_db_conn('sample_library.db')
    cursor = conn.cursor()

    # Create a table to store sample library data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sample_library (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            webpage TEXT NOT NULL,
            tags TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            male_pronouns TEXT NOT NULL,
            female_pronouns TEXT NOT NULL,
            all_matches JSON NOT NULL,
            reviewed BOOLEAN NOT NULL,
            approved BOOLEAN NOT NULL,
            download_count INTEGER NOT NULL DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

if not (DB_FOLDER/'sample_library.db').exists():
    initialize_books_database()
    
def add_sample(submission, reviewed=False, approved=False):
    """ Add a sample to the samples database """
    title = submission['title']
    author = submission['author']
    webpage = submission['webpage']
    tagline = submission['tagline']
    excerpt = submission['excerpt']
    male_pronouns = submission['male pronouns']
    female_pronouns = submission['female pronouns']
    all_matches = json.dumps(submission['all matches'])
    if not reviewed:
        reviewed = submission['reviewed'] #if not specified, use submission data
    if not approved:
        approved = submission['approved'] #if not specified, use submission data
    conn = get_db_conn('sample_library.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sample_library (title, author, webpage, tagline, excerpt, male_pronouns, "
        "female_pronouns, all_matches, reviewed, approved, download_count)"
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (title, author, webpage, tagline, excerpt, male_pronouns, female_pronouns,
         all_matches, reviewed, approved, 0)
    )
    conn.commit()
    conn.close()

def add_book(filename, address, words, matches, time):
    """ Add a book - ip combination to the processed books database """
    conn = get_db_conn('processed_books.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO processed_books (filename, address, words, matches, time) VALUES (?, ?, ?, ?, ?)",
        (filename, address, words, matches, time)
    )
    conn.commit()
    conn.close()

def get_book_count():
    """ Get total number of books that have been degendered """
    conn = get_db_conn('processed_books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(id) FROM processed_books')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_sample_dict(sample, keep_abbreviations=True):
    """ Create a dictionary from a sample in the database """
    abbreviations = {
        'm' : 'Male',
        'f' : 'Female',
        'nb' : 'Non-binary'
        }
    sample_dict = {
            'id': sample[0],
            'title': sample[1],
            'author': sample[2], 
            'webpage': sample[3],
            'tagline': sample[4],
            'excerpt': sample[5],
            'male pronouns': sample[6],
            'female pronouns': sample[7],
            'all matches': json.loads(sample[8]),
            'reviewed': sample[9],
            'approved': sample[10]
        }
    if not keep_abbreviations:
        sample_dict['male pronouns'] = abbreviations[sample_dict['male pronouns']]
        sample_dict['female pronouns'] = abbreviations[sample_dict['female pronouns']]
    return sample_dict

def get_sample_by_id(sample_id, keep_abbreviations=True):
    """ Get a specific sample dictionary using its ID """
    conn = get_db_conn('sample_library.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM sample_library WHERE id = {sample_id};"
    cursor.execute(query)
    sample = cursor.fetchall()[0]
    conn.close()
    sample_dict = get_sample_dict(sample, keep_abbreviations=keep_abbreviations)
    return sample_dict

def get_sample_ids(reviewed=True, approved=True, order='random'):
    """ Get list of approved samples ids from the database """
    conn = get_db_conn('sample_library.db')
    cursor = conn.cursor()
    if reviewed and approved:
        query = "SELECT id FROM sample_library WHERE reviewed = 1 AND approved = 1"
    elif reviewed:
        query = "SELECT id FROM sample_library WHERE reviewed = 1"
    elif approved:
        query = "SELECT id FROM sample_library WHERE approved = 1"
    else:
        query = "SELECT id FROM sample_library"
    cursor.execute(query)
    sample_ids = cursor.fetchall()
    sample_ids = [item[0] for item in sample_ids]
    conn.close()
    if order == 'random': #Other sort orders could be implemented - popularity?
        random.shuffle(sample_ids)
    return sample_ids

def increment_download_count(sample_id):
    """ Increment download count for a sample """
    conn = get_db_conn('sample_library.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE sample_library
        SET download_count = download_count + 1
        WHERE id = ?;
    ''', (sample_id,))
    conn.commit()
    conn.close()

def clear_sample_library():
    """ TESTING ONLY - Reset sample_library """
    print('Not allowed') #Comment out this line to use this function - for safety
    return #Comment our this line to use this function - for safety
    if input('Deleting sample library - Are you sure?\n'
             'Type y to confirm, anything else to exit\n').lower() == 'y':
        print('Deleting samples')
        conn = get_db_conn('sample_library.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sample_library")
        conn.commit()
        conn.close()
    else:
        print('Cancelling operation')

def approve_all():
    """ TESTING ONLY - Approve all samples """
    print('Not allowed') #Comment out this line to use this function - for safety
    return #Comment out this line to use this function - for safety
    conn = get_db_conn('sample_library.db')
    cursor = conn.cursor()
    update_query = "UPDATE sample_library SET approved = 1, reviewed = 1"
    cursor.execute(update_query)
    conn.commit()
