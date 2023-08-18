"""
This is where the degendering takes place.
"""
import regex
import sys
import random
from timeit import default_timer as timer
from librarian import get_book_text, is_string
from reference_library import NB_NAMES, NB_NAMES_MODERN, NB_NAMES_BY_DECADE, ALL_NAMES
from reference_library import AMBIGUOUS_NAMES, BOY_NAMES, GIRL_NAMES
from reference_library import COMMON_WORDS, MALE_PRONOUN_DICT, FEMALE_PRONOUN_DICT
from utilities import lazy_shuffle, sorted_by_values, get_min_diff, lazy_shuffle_keys, drop_low

DEFAULT_PARAMETERS = {
    'male' : 'nb',
    'female' : 'nb',
    'verbose' : False,
    'year' : 1960,
    'name matches' : {},
    'name choices' : 20
    }

#Temporary values used to debug an optimization issue
lowercase_timer = 0
titlecase_timer = 0
uppercase_timer = 0
soup_lowercase_timer = 0
soup_titlecase_timer = 0
soup_uppercase_timer = 0

def suggest_name(gender):
    if gender == 'nb':
        return random.choice(NB_NAMES)
    elif gender == 'f':
        return random.choice(GIRL_NAMES)
    elif gender == 'm':
        return random.choice(BOY_NAMES)
    else:
        raise ValueError
    
def fill_defaults(parameters):
    for key in DEFAULT_PARAMETERS:
        if key not in parameters:
            parameters[key] = DEFAULT_PARAMETERS[key]
    return parameters

def change_pronoun(pronoun, replacement, text, verbose=False):
    """Since the regex substitution is done for each pronoun in the whole text,
    we need to add a mark ('àéà') to avoid the pronouns we've just changed being
    changed back later. This mark will be removed in fix_text"""
    text = regex.sub(r'\b' + pronoun + r'\b', replacement + 'àéà', text)
    return text

def fix_text(text):
    """ Various substitutions to fix problems created by the fact
    we check pronouns one at a time """
    text = regex.sub(r'àéà', '', text)
    text = regex.sub(r'His/Him/Hers', 'Her/Hers', text)
    text = regex.sub(r'Their/Them/Hers', 'Her/Hers', text)
    text = regex.sub(r'Their/Hers', 'Her/Hers', text)
    text = regex.sub(r'their/hers', 'her/hers', text)
    text = regex.sub(r'his/him/hers', 'her/hers', text)
    text = regex.sub(r'their/them/hers', 'her/hers', text)
    return text

def change_pronouns(text, pronoun_dict, verbose=False):
    start = timer()
    for pronoun in pronoun_dict:
        text = change_pronoun(pronoun, pronoun_dict[pronoun], text, verbose=verbose)
    end = timer()
    global lowercase_timer
    lowercase_timer += (end-start)
    global soup_lowercase_timer
    soup_lowercase_timer += (end-start)
    start = timer()
    for pronoun in pronoun_dict:
        text = change_pronoun(pronoun.title(), pronoun_dict[pronoun].title(),
                              text, verbose=verbose)
    end = timer()
    global titlecase_timer
    titlecase_timer += (end-start)
    global soup_titlecase_timer
    soup_titlecase_timer += (end-start)
    start = timer()
    for pronoun in pronoun_dict:
        text = change_pronoun(pronoun.upper(), pronoun_dict[pronoun].upper(),
                              text, verbose=verbose)
    end = timer()
    global uppercase_timer
    uppercase_timer += (end-start)
    global soup_uppercase_timer
    soup_uppercase_timer += (end-start)
    return fix_text(text)

def create_pronoun_dict(text, male, female):
    pronoun_dict = {}
    if male == 'nb':
        pronoun_dict.update({item:value[0] for (item,value)
                             in MALE_PRONOUN_DICT.items()})
    elif male == 'f':
        pronoun_dict.update({item:value[1] for (item,value)
                             in MALE_PRONOUN_DICT.items()})
    if female == 'nb':
        pronoun_dict.update({item:value[0] for (item,value)
                             in FEMALE_PRONOUN_DICT.items()})
    elif female == 'm':
        pronoun_dict.update({item:value[1] for (item,value)
                             in FEMALE_PRONOUN_DICT.items()})
    return pronoun_dict

def get_book_names(book_soup, verbose=False):
    #Tries to get all proper names used in the book
    book_text = get_book_text(book_soup)
    pattern = r'(?<!^|[.?!]\s)\b[A-Z][a-z]*\b'
    matches = regex.findall(pattern, book_text)
    names = []
    for match in matches:
        if not match.lower() in [word.lower() for word in COMMON_WORDS]:
            names += [match]
    name_dict = {}
    for name in names:
        if name in name_dict:
            name_dict[name] += 1
        else:
            name_dict[name] = 1
    return name_dict

def get_name_dict(book_soup, verbose=False):
    #ets the best known first names used in the book
    book_text = get_book_text(book_soup)
    word_list = regex.sub(r'[^\p{Latin}]',' ',book_text).split()
    name_list = [word for word in word_list if word in ALL_NAMES]
    name_dict = {}
    for name in name_list:
        if name in name_dict:
            name_dict[name] += 1
        else:
            name_dict[name] = 1
    return name_dict

def get_sorted_name_list(name_dict, verbose=False):
    return lazy_shuffle_keys(name_dict, reverse=True)
    
def change_name(name, match, text, verbose=False):
    text = regex.sub(rf"\b{regex.escape(name)}\b", match, text)
    return text

def change_names(text, parameters):
    name_matches = parameters['name matches']
    for name in name_matches:
        text = change_name(name, name_matches[name], text, verbose=parameters['verbose'])
        text = change_name(name.upper(), name_matches[name].upper(),
                           text, verbose=parameters['verbose'])
    return text
        
def degender_text(text, parameters):
    verbose = parameters['verbose']
    original_text = text
    pronoun_dict = create_pronoun_dict(text, parameters['male'], parameters['female'])
    text = change_pronouns(text, pronoun_dict, verbose=verbose)
    text = change_names(text, parameters)
    if verbose:
        if text != original_text:
            print('Changed pronouns and/or names')
            print('New text:')
            print(text)
    return text

def degender_all(item, parameters):
    if is_string(item):
        new_string = degender_text(item, parameters)
        if new_string:
            item.replace_with(new_string)
    try:
        if item.contents:
            for child in item.contents:
                degender_all(child, parameters)    
    except AttributeError:
        pass
        
def degender_book(book_soup, parameters = DEFAULT_PARAMETERS):
    parameters = fill_defaults(parameters)
    print(parameters)
    for soup in book_soup:
        global soup_lowercase_timer
        global soup_titlecase_timer
        global soup_uppercase_timer
        degender_all(soup, parameters)
        print('Degendering times for soup:')
        print(f'Lowercase: {soup_lowercase_timer} seconds')
        print(f'Titlecase: {soup_titlecase_timer} seconds')
        print(f'Uppercase: {soup_uppercase_timer} seconds')
        soup_lowercase_timer = 0
        soup_titlecase_timer = 0
        soup_uppercase_timer = 0
    print('Degendering times for book:')
    print(f'Lowercase: {lowercase_timer} seconds')
    print(f'Titlecase: {titlecase_timer} seconds')
    print(f'Uppercase: {uppercase_timer} seconds')
        
def get_text_dict(text):
    word_list = regex.sub(r'[^\p{Latin}]',' ',text).split()
    name_list = [word for word in word_list if (word in ALL_NAMES
                                                and word not in AMBIGUOUS_NAMES)]
    name_dict = {}
    for name in name_list:
        if name in name_dict:
            name_dict[name] += 1
        else:
            name_dict[name] = 1
    return name_dict

def get_text_names(text):
    pattern = r'(?<!^|[.?!]\s)\b[A-Z][a-z]*\b'
    matches = regex.findall(pattern, text)
    names = []
    for match in matches:
        if not match.lower() in [word.lower() for word in COMMON_WORDS]:
            names += [match]
    name_dict = {}
    for name in names:
        if name in name_dict:
            name_dict[name] += 1
        else:
            name_dict[name] = 1
    return name_dict
