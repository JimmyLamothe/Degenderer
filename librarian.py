import ebooklib
import bs4

from ebooklib import epub
from bs4 import BeautifulSoup

BOOK_PATH = 'books/'

BOOK_LIBRARY = {
    'Jane Eyre' : 'pg1260.epub'
    }

def pause():
    input('Press enter to continue')

def get_book_items(book):
    book_items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    return book_items

def check_out(book_title):
    book = epub.read_epub(BOOK_PATH + BOOK_LIBRARY[book_title])
    return book

def item_to_soup(book_item):
    return BeautifulSoup(book_item.get_content(), 'html.parser')

def create_soup(book):
    book_items = get_book_items(book)
    return [item_to_soup(item) for item in book_items]

def get_paragraph_list(book_soup):
    paragraph_list = []
    for soup in book_soup:
        paragraph_list.extend(soup.find_all('p'))
    return paragraph_list

def add_foo(paragraph):
    paragraph.append(': FOO!')

def soup_to_book(book_soup, book):
    book_items = get_book_items(book)
    for soup, item in zip(book_soup, book_items):
        #print('soup:\n', str(soup))
        if soup.find('p'):
            print('pre-item:\n', item.get_content())
            pause
            #item.set_content(''.join([str(paragraph) for paragraph in soup.find_all('p')]))
            item.set_content(str(soup.body))
            print('post-item:\n', item.get_content())
            pause
    
def create_epub(book, filename):
    epub.write_epub(BOOK_PATH + filename, book)


"""
for paragraph in paragraph_list:
    try:

    except AttributeError:
"""
