import sys
import json
import uuid
from pathlib import Path

from librarian import check_out, create_soup, read_epub, soup_to_book, write_epub

from degenderer import degender_book, get_book_names

WORKING_DIR = Path('temp')
UPLOAD_DIR = Path('uploads')

def get_names(book_file):
    book = read_epub(book_file)
    book_soup = create_soup(book)
    name_dict = get_book_names(book_soup)
    name_list = []
    for key, value in sorted(name_dict.items(), key = lambda x: x[1], reverse=True):
        name_list.append(key)
    return name_list
        
def process_epub(filepath, parameters):
    input_filepath = Path(filepath)
    if not input_filepath.suffix == '.epub':
        output_filepath = WORKING_DIR.joinpath(str(uuid.uuid4()) + '.epub')
    else:
        output_filename = input_filepath.stem
        output_filename += '_'
        output_filename += parameters['male']
        output_filename += parameters['female']
        output_filename += input_filepath.suffix
        output_filepath = WORKING_DIR.joinpath(output_filename)
    if not type(parameters) is dict:
        with open(parameters, 'r') as file:
            parameters = json.load(file)
    book = read_epub(input_filepath)
    book_soup = create_soup(book)
    name_dict = get_book_names(book_soup)
    """
    name_list = []
    for key, value in sorted(name_dict.items(), key = lambda x: x[1], reverse=True):
        name_list.append(key)
    print(name_list)
    """
    degender_book(book_soup, parameters)
    soup_to_book(book_soup, book)
    write_epub(book, output_filepath)
    print(output_filepath)
    return output_filepath
