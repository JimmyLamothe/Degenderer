"""
This module handles ePub processing with Beautiful Soup
"""

import ebooklib
import bs4

from ebooklib import epub
from bs4 import BeautifulSoup

BOOK_PATH = '../books/'

def read_epub(filepath):
    """ Reads an ePub file using ebooklib """
    book = epub.read_epub(filepath)
    return book

def write_epub(book, filepath):
    """ Writes an ePub file using ebooklib """
    epub.write_epub(filepath, book)

def get_book_items(book):
    """ Gets all items from an ebooklib book """
    book_items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    return book_items

def item_to_soup(book_item):
    """ Converts an ebooklib item to a BeautifulSoup soup """
    return BeautifulSoup(book_item.get_content(), 'html.parser')

def create_soup(book):
    """ Converts an ebooklib book to a list of BeautifulSoup soups """
    book_items = get_book_items(book)
    return [item_to_soup(item) for item in book_items]

def is_string(soup_item):
    """ Checks if an item in a soup is a navigable string """
    return isinstance(soup_item, bs4.element.NavigableString)

def set_text(navigable_string, text):
    """ Changes the text of a navigable string """
    navigable_string.replace_with(text)

def get_paragraphs(soup):
    """ Gets all the paragraphs in a soup """
    paragraphs = soup.find_all('p')
    return paragraphs

def get_divs(soup):
    """ Gets all the divs in a soup """
    divs = []
    for div in soup.find_all('div'):
        if not div.find('p') and not div.find('div'):
            if div.get_text():
                divs.append(div)
    return divs

def get_paragraphs_and_divs(soup):
    """ Gets all the paragraphs and divs in a soup """
    paragraphs = get_paragraphs(soup)
    divs = get_divs(soup)
    return paragraphs + divs

def get_paragraph_list(book_soup):
    """ Convers list of soups into list of lists of paragraphs and divs """
    paragraph_list = []
    for soup in book_soup:
        paragraph_list.extend(get_paragraphs_and_divs(soup))
    return paragraph_list

def get_paragraph_text(paragraph):
    """ Gets the text of a paragraph or div """
    return paragraph.get_text()

def get_book_text(book_soup):
    """ Combines all strings in a book soup into one and returns it """
    paragraph_list = get_paragraph_list(book_soup)
    book_text = ''
    for paragraph in paragraph_list:
        book_text += get_paragraph_text(paragraph)
    return book_text

def soup_to_book(book_soup, book):
    """ Converts modified book_soup back into ebooklib format """
    book_items = get_book_items(book)
    for soup, item in zip(book_soup, book_items):
        if soup.find('p') or soup.find('div'):
            item.set_content(str(soup.body))

def create_epub(book, filename):
    """ Create ePub file from ebooklib book """
    epub.write_epub(BOOK_PATH + filename, book)
