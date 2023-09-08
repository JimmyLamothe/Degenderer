import sys
import json
import uuid
from pathlib import Path

from librarian import check_out, create_soup, read_epub, soup_to_book, write_epub

from degenderer import degender_book, get_book_names

WORKING_DIR = Path('temp')

def get_book_info(book_file):
    filepath = WORKING_DIR.joinpath(str(uuid.uuid4()) + '.epub')
    book = read_epub(book_file)
    book_soup = create_soup(book)
    name_dict = get_book_names(book_soup)
    name_list = []
    for key, value in sorted(name_dict.items(), key = lambda x: x[1], reverse=True):
        name_list.append(key)
    return name_list
        
def process_epub(book_file, parameters):
    filepath = WORKING_DIR.joinpath(str(uuid.uuid4()) + '.epub')
    if not type(parameters) is dict:
        with open(parameters, 'r') as file:
            parameters = json.load(file)
    book = read_epub(book_file)
    book_soup = create_soup(book)
    name_dict = get_book_names(book_soup)
    name_list = []
    for key, value in sorted(name_dict.items(), key = lambda x: x[1], reverse=True):
        name_list.append(key)
    #print(name_list)
    degender_book(book_soup, parameters)
    soup_to_book(book_soup, book)
    write_epub(book, filepath)
    print(filepath)
    return filepath
