"""
This is where the degendering takes place.
"""
import regex
import sys
import random
import json
from timeit import default_timer as timer
from librarian import get_book_text, is_string
from reference_library import NB_NAMES, NB_NAMES_MODERN, NB_NAMES_BY_DECADE, ALL_NAMES
from reference_library import AMBIGUOUS_NAMES, BOY_NAMES, GIRL_NAMES
from reference_library import COMMON_WORDS, MALE_PRONOUN_DICT, FEMALE_PRONOUN_DICT
from utilities import lazy_shuffle, sorted_by_values, get_min_diff, lazy_shuffle_keys, drop_low

DEFAULT_PARAMETERS = {
    'male' : 'nb',
    'female' : 'nb',
    'year' : 1960,
    'name matches' : {},
    'name choices' : 20
    }

#Temporary values used to debug an optimization issue
book_timer = 0
soup_timer = 0

def get_pronoun_list():
    male_pronouns = [key for key in MALE_PRONOUN_DICT]
    female_pronouns = [key for key in FEMALE_PRONOUN_DICT]
    pronoun_list = male_pronouns + female_pronouns
    return pronoun_list

def get_suggestion(name_list, names_used):
    #print(f'Used names: {names_used}')
    available_names = [name for name in name_list if not name in names_used]
    #print(f'Available names: {available_names}')
    if available_names:
        selection = random.choice(available_names)
        #print(f'Selected name: {selection}')
        return selection
    else:
        selection = random.choice(name_list)
        #print(f'Selected name: {selection}')
        return selection
    
def suggest_name(gender, names_used):
    if gender == 'nb':
        return get_suggestion(NB_NAMES, names_used)
    elif gender == 'f':
        return get_suggestion(GIRL_NAMES, names_used)
    elif gender == 'm':
        return get_suggestion(BOY_NAMES, names_used)
    else:
        return ''
    
def fill_defaults(parameters):
    for key in DEFAULT_PARAMETERS:
        if key not in parameters:
            parameters[key] = DEFAULT_PARAMETERS[key]
    return parameters

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
        
def degender_text(text, parameters):
    start = timer()
    original_text = text
    match_dict = parameters['match dict']
    for key in match_dict:
        key_dict = match_dict[key]
        text = regex.sub(key_dict['pattern'], key_dict['replacement'], text)
    end = timer()
    global book_timer
    book_timer += (end-start)
    global soup_timer
    soup_timer += (end-start)
    return fix_text(text)

def degender_all(item, parameters):
    if is_string(item):
        new_string = degender_text(item, parameters)
        if new_string:
            item.replace_with(new_string)
    else:        
        try:
            for child in item.contents:
                degender_all(child, parameters)
        except AttributeError:
            pass

def create_pronoun_dict(parameters):
    pronoun_dict = {}
    if parameters['male'] == 'nb':
        male_index = 0
    elif parameters['male'] == 'f':
        male_index = 1
    else:
        male_index = -1
    if parameters['female'] == 'nb':
        female_index = 0
    elif parameters['female'] == 'm':
        female_index = 1
    else:
        female_index = -1
    for tup in [(MALE_PRONOUN_DICT,male_index),(FEMALE_PRONOUN_DICT,female_index)]:
      index = tup[1]
      reference_dict = tup[0]
      if index >= 0:
        for pronoun in reference_dict:
            match = reference_dict[pronoun][index]
            pronoun_dict[pronoun] = {'match':match,
                                  'pattern':regex.compile(r'\b' + pronoun + r'\b'),
                                  'replacement': match + 'àéà'}
            pronoun_dict[pronoun.title()] = {'match':match.title(),
                                             'pattern':regex.compile(r'\b' + pronoun.title()
                                                                     + r'\b'),
                                             'replacement': match.title() + 'àéà'}
            pronoun_dict[pronoun.upper()] = {'match':match.upper(),
                                          'pattern':regex.compile(r'\b' + pronoun.upper()
                                                                  + r'\b'),
                                          'replacement': match.upper() + 'àéà'}
    return pronoun_dict

def create_name_dict(parameters):
    name_matches = parameters['name matches']
    name_dict = {}
    for name in name_matches:
        match = name_matches[name]
        name_dict[name] = {'match':match,
                           'pattern':regex.compile(r'\b' + name + r'\b'),
                           'replacement': match + 'àéà'}
        name_dict[name.upper()] = {'match':match.upper(),
                                   'pattern':regex.compile(r'\b' + name.upper() + r'\b'),
                                   'replacement': match.upper() + 'àéà'}
    return name_dict
        
def degender_book(book_soup, parameters = DEFAULT_PARAMETERS):
    parameters = fill_defaults(parameters)
    pronoun_dict = create_pronoun_dict(parameters)
    name_dict = create_name_dict(parameters)
    match_dict = {**pronoun_dict, **name_dict}
    #print(f'match_dict: {match_dict}')
    parameters['match dict'] = match_dict
    with open('reference/test_match_dict.json', 'w') as json_file:
        json_dict = {}
        for key in match_dict:
            json_dict[key] = match_dict[key]['match']
        json.dump(json_dict, json_file)
    for soup in book_soup:
        global soup_timer
        degender_all(soup, parameters)
        print(f'Degendering times for soup: {soup_timer} seconds')
        soup_timer = 0
    print(f'Degendering times for book {book_timer} seconds:')
        
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

def get_potential_names_dict(book_soup):
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

def get_known_names_dict(book_soup):
    #Gets the best known first names used in the book
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

