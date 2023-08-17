import sys
import json
import uuid
from pathlib import Path

from librarian import check_out, create_epub, create_soup, soup_to_book

from degenderer import degender_book

WORKING_DIR = 'temp'

def process_epub(book_file, json_parameters):
    filepath = WORKING_DIR.joinpath(str(uuid.uuid4(),'.epub'))
    with open(json_parameters, 'r') as file:
        parameters = json.load(json_parameters)
    book = check_out(book_file)
    book_soup = create_soup(book)
    degender_book(book_soup, parameters)
    soup_to_book(book_soup, book)
    create_epub(book, filepath)
    #print(get_book_text(book_soup))
    return filepath
