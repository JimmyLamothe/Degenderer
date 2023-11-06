"""
submitted book format:
{
    'book_name': request.form['book_name'],
    'author': request.form['author'],
    'webpage': request.form['webpage'],
    'tags': request.form['tags'],
    'excerpt': request.form['excerpt'],
    'male pronouns': session['male_pronoun'],
    'female pronouns': session['female_pronoun'],
    'name matches': session['name_matches'],
    'reviewed': False,
    'approved': False
}
"""

import json
import sqlite3


def initialize_sample_database():
    conn = sqlite3.connect('sample_library.db')
    cursor = conn.cursor()

    # Create a table to store sample library data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sample_library (
            id INTEGER PRIMARY KEY,
            book_name TEXT NOT NULL,
            author TEXT NOT NULL,
            webpage TEXT NOT NULL,
            tags TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            male_pronouns TEXT NOT NULL,
            female_pronouns TEXT NOT NULL,
            name_matches JSON NOT NULL,
            reviewed BOOLEAN NOT NULL,
            approved BOOLEAN NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Add a sample to the database
def add_sample(submission, reviewed=False, approved=False):
    book_name = submission['book_name']
    author = submission['author']
    webpage = submission['webpage']
    tags = submission['tags']
    excerpt = submission['excerpt']
    male_pronouns = submission['male pronouns']
    female_pronouns = submission['female pronouns']
    name_matches = json.dumps(submission['name matches'])
    if not reviewed:
        reviewed = submission['reviewed'] #if not specified, use submission data
    if not approved:
        approved = submission['approved'] #if not specified, use submission data
    conn = sqlite3.connect('sample_library.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sample_library (book_name, author, webpage, tags, excerpt, male_pronouns, "
        "female_pronouns, name_matches, reviewed, approved) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (book_name, author, webpage, tags, excerpt, male_pronouns, female_pronouns,
         name_matches, reviewed, approved))
    conn.commit()
    conn.close()

# Get list of samples from the database    
def get_samples(reviewed=True, approved=True):
    conn = sqlite3.connect('sample_library.db')
    cursor = conn.cursor()
    if reviewed and approved:
        query = "SELECT * FROM sample_library WHERE reviewed = 1 AND approved = 1"
    elif reviewed:
        query = "SELECT * FROM sample_library WHERE reviewed = 1"
    elif approved:
        query = "SELECT * FROM sample_library WHERE approved = 1"
    else:
        query = "SELECT * FROM sample_library"
    cursor.execute(query)
    samples = cursor.fetchall()
    print(samples)
    conn.close()
    sample_dicts = []
    abbreviations = {
        'm' : 'Male',
        'f' : 'Female',
        'nb' : 'Non-binary'
        }
    for sample in samples:
        sample_dict = {
            'book_name': sample[1],
            'author': sample[2], 
            'webpage': sample[3],
            'tags': sample[4],
            'excerpt': sample[5],
            'male pronouns': abbreviations[sample[6]],
            'female pronouns': abbreviations[sample[7]],
            'name matches': sample[8],
            'reviewed': sample[9],
            'approved': sample[10]
        }
        sample_dicts.append(sample_dict)
    return sample_dicts

#TESTING ONLY - Reset sample_library
def clear_sample_library():
    if input('Deleting sample library - Are you sure?\n'
             'Type y to confirm, anything else to exit\n').lower() == 'y':
        print('Deleting samples')
        conn = sqlite3.connect('sample_library.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sample_library")
        conn.commit()
        conn.close()
    else:
        print('Cancelling operation')

#TESTING ONLY - Approve all samples        
def approve_all():
    conn = sqlite3.connect('sample_library.db')
    cursor = conn.cursor()
    update_query = "UPDATE sample_library SET approved = 1, reviewed = 1"
    cursor.execute(update_query)
    conn.commit()
