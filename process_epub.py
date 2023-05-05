import sys
import json
import uuid
from pathlib import Path

from librarian import check_out, create_soup, read_epub, soup_to_book, write_epub

from degenderer import degender_book, get_book_names

WORKING_DIR = Path('temp')

def process_epub(book_file, parameters):
    filepath = WORKING_DIR.joinpath(str(uuid.uuid4()) + '.epub')
    if not type(parameters) is dict:
        with open(parameters, 'r') as file:
            parameters = json.load(file)
    book = read_epub(book_file)
    book_soup = create_soup(book)
    name_dict = get_book_names(book_soup)
    for key, value in sorted(name_dict.items(), key = lambda x: x[1]):
        print(key, value)
    sys.exit(0)
    degender_book(book_soup, parameters)
    soup_to_book(book_soup, book)
    write_epub(book, filepath)
    #print(get_book_text(book_soup))
    print(filepath)
    return filepath
