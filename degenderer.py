"""A
This is where the degendering takes place.
"""
import regex

from librarian import get_paragraph_text, pause, set_paragraph_text, get_book_text
from reference_library import NB_NAMES, NB_NAMES_MODERN, NB_NAMES_BY_DECADE
from reference_library import GENDERED_NAMES, GENDERED_NAMES_BY_DECADE, AMBIGUOUS_NAMES
from reference_library import BOY_NAMES, BOY_NAMES_BY_DECADE, GIRL_NAMES, GIRL_NAMES_BY_DECADE
from reference_library import PRONOUN_DICTIONARY
from utilities import lazy_shuffle, sorted_by_values, get_min_diff, lazy_shuffle_keys, drop_low

def degender_pronoun(pronoun, text, verbose=False):
    if verbose:
        print('Matching for : ' + pronoun)
        if regex.search(r'\b' + pronoun + r'\b', text):
            print('Pronoun found!')
            print(pronoun + ' will be changed to ' + PRONOUN_DICTIONARY[pronoun])
    text = regex.sub(r'\b' + pronoun + r'\b', PRONOUN_DICTIONARY[pronoun], text)
    return text

def degender_pronouns(text, verbose=False):
    if verbose:
        for pronoun in PRONOUN_DICTIONARY:
            text = degender_pronoun(pronoun, text, verbose=True)
    for pronoun in PRONOUN_DICTIONARY:
        text = degender_pronoun(pronoun, text)
    return text

def get_name_dict(book_soup, verbose=False):
    book_text = get_book_text(book_soup)
    word_list = regex.sub(r'[^\p{Latin}]',' ',book_text).split()
    name_list = [word for word in word_list if (word in GENDERED_NAMES
                                                and word not in AMBIGUOUS_NAMES)]
    name_dict = {}
    for name in name_list:
        if name in name_dict:
            name_dict[name] += 1
        else:
            name_dict[name] = 1
    return name_dict

def get_sorted_name_list(name_dict, verbose=False):
    return lazy_shuffle_keys(name_dict, reverse=True)
    
def get_period_nb_names(year, verbose=False):
    target_decade = year + 30
    nb_name_diff_dict = {item : get_min_diff(year, value)
                         for (item, value)in NB_NAMES_BY_DECADE.items()} 
    return lazy_shuffle_keys(nb_name_diff_dict, reverse=False)

def degender_name(name, match, text, verbose=False):
    if verbose:
        print('Matching for : ' + name)
        if regex.search(r"(?<![a-zA-Z'’-])" + name + r"(?![a-zA-Z'’-])", text):
            print('Name found!')
            print(name + ' will be changed to ' + match)
    text = regex.sub(r"(?<![a-zA-Z'’-])" + name + r"(?![a-zA-Z'’-])", match, text)
    return text

def degender_names(text, name_matches, year=1960, verbose=False):
    if verbose:
        for name in name_matches:
            text = degender_name(name, name_matches[name], text, verbose=True)
    for name in name_matches:
        text = degender_name(name, name_matches[name], text)
    return text
        
def degender_text(text, name_matches, year=1960, verbose=False):
    original_text = text
    if verbose:
        text = degender_pronouns(text, verbose=True)
    else:
        text = degender_pronouns(text)
    if verbose:
        text = degender_names(text, name_matches, year=year, verbose=True)
    else:
        text = degender_names(text, name_matches, year=year)
    if verbose:
        if text != original_text:
            print('Changed pronouns and/or names')
            print('New text:')
            print(text)
    return text

def degender_paragraph(paragraph, name_matches, year=1960, verbose=False):
    text = get_paragraph_text(paragraph)
    if verbose:
        print('Pre-text:')
        print(text)
        text = degender_text(text, name_matches, year=year, verbose=True)
    else:
        text = degender_text(text, name_matches, year=year)
    if verbose:
        set_paragraph_text(paragraph, text, verbose=True)
    else:
        set_paragraph_text(paragraph, text)
              
def degender_soup(soup, name_matches, year=1960, verbose=False):
    if verbose:
        for paragraph in soup.find_all('p'):
            degender_paragraph(paragraph, name_matches, year=year, verbose=True)
    for paragraph in soup.find_all('p'):
        degender_paragraph(paragraph, name_matches, year=year)
        
def degender_book(book_soup, year=1960, verbose=False):
    name_dict = get_name_dict(book_soup)
    name_list = get_sorted_name_list(drop_low(name_dict)) #Removing names with few occurrences
    nb_name_list = get_period_nb_names(year)
    nb_name_list.extend(NB_NAMES_MODERN)
    name_matches = {item : value for (item, value) in zip(name_list, nb_name_list)}
    if verbose:
        for soup in book_soup:
            degender_soup(soup, name_matches, year=year, verbose=True)
    for soup in book_soup:
        degender_soup(soup, name_matches, year=year)
