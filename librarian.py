import ebooklib
import bs4

from ebooklib import epub
from bs4 import BeautifulSoup

BOOK_PATH = '../books/'

BOOK_LIBRARY = {
    'Jane Eyre' : 'pg1260.epub',
    'Segreti' : 'Harry Potter e la Camera dei Segreti.epub'
    }

def pause():
    input('Press enter to continue')

def read_epub(filepath):
    book = epub.read_epub(filepath)
    return book

def write_epub(book, filepath):
    epub.write_epub(filepath, book)
    
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

def get_paragraphs(soup):
    paragraphs = soup.find_all('p')
    divs = soup.find_all('div')
    return paragraphs + divs

def get_paragraph_list(book_soup):
    paragraph_list = []
    for soup in book_soup:
        paragraph_list.extend(get_paragraphs(soup))
    return paragraph_list

def get_paragraph_text(paragraph):
    return paragraph.get_text()

def set_paragraph_text(paragraph, text, verbose=False):
    if verbose:
        print('Paragraph pre-text:')
        print(paragraph.text)
        print('Changing to:')
        print(text)
    paragraph.clear()
    paragraph.append(text)
    if verbose:
        print('Paragraph post-text:')
        print(paragraph.text)
        pause()

def get_book_names(book_soup, verbose=False):
    book_text = get_book_text(book_soup)
    name_list = regex.sub(r'[^\p{Latin}]',' ',book_text).split()
    name_dict = {}
    for name in name_list:
        if name in name_dict:
            name_dict[name] += 1
        else:
            name_dict[name] = 1
    return name_dict
        
def get_book_text(book_soup):
    paragraph_list = get_paragraph_list(book_soup)
    book_text = ''
    for paragraph in paragraph_list:
        book_text += get_paragraph_text(paragraph)
    return book_text

def soup_to_book(book_soup, book):
    book_items = get_book_items(book)
    for soup, item in zip(book_soup, book_items):
        #print('soup:\n', str(soup))
        if soup.find('p'):
            #print('pre-item:\n', item.get_content())
            #pause()
            #item.set_content(''.join([str(paragraph) for paragraph in soup.find_all('p')]))
            item.set_content(str(soup.body))
            #print('post-item:\n', item.get_content())
            #pause()
    
def create_epub(book, filename):
    epub.write_epub(BOOK_PATH + filename, book)


"""
for paragraph in paragraph_list:
    try:

    except AttributeError:
"""
