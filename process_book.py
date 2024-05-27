"""
This module processes an ePub book for de/regendering
"""
import os
from pathlib import Path
from librarian import create_soup, read_epub, soup_to_book, write_epub
from degenderer import degender_book, get_book_names, get_total_words

WORKING_DIR = Path(os.environ.get('WORKING_DIR', 'temp'))

def analyze_book(book_file):
    """ Get a tuple of the known names, potential names and total words in the book """
    book = read_epub(book_file)
    book_soup = create_soup(book)
    known_names, known_name_genders, potential_names = get_book_names(book_soup)
    total_words = get_total_words(book_soup)
    return known_names, known_name_genders, potential_names, total_words

def get_output_filepath(filepath, parameters, destination=WORKING_DIR):
    """ Get the output filepath for a book to be degendered """
    input_filepath = Path(filepath)
    output_filename = input_filepath.stem
    if not parameters.get('modifying', None):
        output_filename += '_'
        output_filename += parameters['male']
        output_filename += parameters['female']
    output_filename += input_filepath.suffix
    output_filepath = WORKING_DIR.joinpath(output_filename)
    return output_filepath

def process_epub(filepath, parameters, session_id=None):
    """ De/regenders an ePub book according to user-submitted parameters """
    input_filepath = Path(filepath)
    output_filepath = get_output_filepath(filepath, parameters)
    book = read_epub(input_filepath)
    book_soup = create_soup(book)
    degender_book(book_soup, parameters, session_id=session_id)
    soup_to_book(book_soup, book)
    write_epub(book, output_filepath)
    print(output_filepath)
    return output_filepath
