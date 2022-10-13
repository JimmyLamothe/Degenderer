"""
This is where the degendering takes place.
"""
import re

from librarian import get_paragraph_text, pause, set_paragraph_text
from reference_library import PRONOUN_DICTIONARY

def degender_pronoun(pronoun, text, verbose=False):
    if verbose:
        print('Matching for : ' + pronoun)
        if re.search(r'\b' + pronoun + r'\b', text):
            print('Pronoun found!')
            print(pronoun + ' will be changed to ' + PRONOUN_DICTIONARY[pronoun])
    text = re.sub(r'\b' + pronoun + r'\b', PRONOUN_DICTIONARY[pronoun], text)
    return text

def degender_pronouns(text, verbose=False):
    if verbose:
        for pronoun in PRONOUN_DICTIONARY:
            degender_pronoun(pronoun, text, verbose=True)
    for pronoun in PRONOUN_DICTIONARY:
        text = degender_pronoun(pronoun, text)
    return text

def degender_names(text, verbose=False):
    """ NOT IMPLEMENTED """
    return text
        
def degender_text(text, verbose=False):
    original_text = text
    if verbose:
        text = degender_pronouns(text, verbose=True)
    else:
        text = degender_pronouns(text)
    if verbose:
        text = degender_names(text, verbose=True)
    else:
        text = degender_names(text)
    if verbose:
        if text != original_text:
            print('Changed pronouns')
            print('New text:')
            print(text)
    return text

def degender_paragraph(paragraph, verbose=False):
    text = get_paragraph_text(paragraph)
    if verbose:
        print('Pre-text:')
        print(text)
        text = degender_text(text, verbose=True)
    else:
        text = degender_text(text)
    if verbose:
        set_paragraph_text(paragraph, text, verbose=True)
    else:
        set_paragraph_text(paragraph, text)
              
def degender_soup(soup, verbose=False):
    if verbose:
        for paragraph in soup.find_all('p'):
            degender_paragraph(paragraph, verbose=True)
    for paragraph in soup.find_all('p'):
        degender_paragraph(paragraph)
        
def degender_book(book_soup, verbose=False):
    if verbose:
        for soup in book_soup:
            degender_soup(soup, verbose=True)
    for soup in book_soup:
        degender_soup(soup)
