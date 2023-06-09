"""
This is where the degendering takes place.
"""
import regex

from librarian import get_paragraph_text, pause, set_paragraph_text, get_book_text
from reference_library import NB_NAMES, NB_NAMES_MODERN, NB_NAMES_BY_DECADE, ALL_NAMES
from reference_library import GENDERED_NAMES, GENDERED_NAMES_BY_DECADE, AMBIGUOUS_NAMES
from reference_library import BOY_NAMES, BOY_NAMES_BY_DECADE, GIRL_NAMES, GIRL_NAMES_BY_DECADE
from reference_library import PRONOUN_DICTIONARY, ALL_NAMES_BY_DECADE
from reference_library import NB_PRONOUN_DICT, MALE_PRONOUN_DICT, FEMALE_PRONOUN_DICT
from utilities import lazy_shuffle, sorted_by_values, get_min_diff, lazy_shuffle_keys, drop_low

DEFAULT_PARAMETERS = {
    'gender' : 'nb',
    'verbose' : False,
    'year' : 1960,
    'name matches' : {},
    'name choices' : 10
    }

def fill_defaults(parameters):
    for key in DEFAULT_PARAMETERS:
        if key not in parameters:
            parameters[key] = DEFAULT_PARAMETERS[key]
    return parameters

def change_pronoun(pronoun, pronoun_dict, text, gender, verbose=False):
    if gender == 'nb':
        replacement = pronoun_dict[pronoun][0]
    else:
        replacement = pronoun_dict[pronoun][1]
    if verbose:
        print('Matching for : ' + pronoun)
        if regex.search(r'\b' + pronoun + r'\b', text):
            print('Pronoun found!')
            print(pronoun + ' will be changed to ' + replacement)
    text = regex.sub(r'\b' + pronoun + r'\b', replacement, text)
    return text

def change_pronouns(text, gender, verbose=False):
    if gender == 'nb':
        pronoun_dict = NB_PRONOUN_DICT
    elif gender == 'f':
        pronoun_dict = MALE_PRONOUN_DICT
    elif gender == 'm':
        pronoun_dict = FEMALE_PRONOUN_DICT
    else:
        print('Unexepected gender input in change_pronouns function, defaulting to non-binary')
    if verbose:
        for pronoun in pronoun_dict:
            text = change_pronoun(pronoun, pronoun_dict, text, gender, verbose=True)
    for pronoun in pronoun_dict:
        text = change_pronoun(pronoun, pronoun_dict, text, gender)
    return text

def get_name_dict(book_soup, verbose=False):
    book_text = get_book_text(book_soup)
    word_list = regex.sub(r'[^\p{Latin}]',' ',book_text).split()
    name_list = [word for word in word_list if (word in ALL_NAMES
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
    
def get_period_names(year, gender, verbose=False): #NOTE: Only NB implemented for now, gender ignored
    if gender == 'm':
        print('m')
        name_list = BOY_NAMES_BY_DECADE
    elif gender == 'f':
        print('f')
        name_list = GIRL_NAMES_BY_DECADE
    else:
        if not gender == 'nb':
            print('WARNING: Unknown gender in parameters, defaulting to non-binary')
        else:
            print('nb')
        name_list = NB_NAMES_BY_DECADE
    target_decade = year + 30
    name_diff_dict = {item : get_min_diff(year, value)
                         for (item, value)in name_list.items()}
    period_names = lazy_shuffle_keys(name_diff_dict, reverse=False)
    if gender == 'nb':
        period_names.extend(NB_NAMES_MODERN)
    return period_names

def change_name(name, match, text, verbose=False):
    if verbose:
        print('Matching for : ' + name)
        if regex.search(r"(?<![a-zA-Z'’-])" + name + r"(?![a-zA-Z'’-])", text):
            print('Name found!')
            print(name + ' will be changed to ' + match)
    text = regex.sub(r"(?<![a-zA-Z'’-])" + name + r"(?![a-zA-Z'’-])", match, text)
    return text

def change_names(text, parameters):
    name_matches = parameters['name matches']
    if parameters['verbose']:
        for name in name_matches:
            text = change_name(name, name_matches[name], text, verbose=True)
    for name in name_matches:
        text = change_name(name, name_matches[name], text)
    return text
        
def degender_text(text, parameters):
    original_text = text
    if parameters['verbose']:
        text = change_pronouns(text, parameters['gender'], verbose=True)
    else:
        text = change_pronouns(text, parameters['gender'])
    if parameters['verbose']:
        text = change_names(text, parameters)
    else:
        text = change_names(text, parameters)
    if parameters['verbose']:
        if text != original_text:
            print('Changed pronouns and/or names')
            print('New text:')
            print(text)
    return text

def degender_paragraph(paragraph, parameters):
    text = get_paragraph_text(paragraph)
    if parameters['verbose']:
        print('Pre-text:')
        print(text)
        text = degender_text(text, parameters)
    else:
        text = degender_text(text, parameters)
    if parameters['verbose']:
        set_paragraph_text(paragraph, text, verbose=True)
    else:
        set_paragraph_text(paragraph, text)
              
def degender_soup(soup, parameters):
    if parameters['verbose']:
        for paragraph in soup.find_all('p'):
            degender_paragraph(paragraph, parameters)
    for paragraph in soup.find_all('p'):
        degender_paragraph(paragraph, parameters)

def get_all_name_matches(name_list, parameters):
    period_names = get_period_names(parameters['year'], parameters['gender'])
    return list(zip(name_list, period_names))
    
def get_name_matches(name_list, parameters):
    name_matches = {}
    name_match_list = get_all_name_matches(name_list, parameters)
    import sys
    print('Enter a name for each main character or press ENTER to accept suggestion')
    for name, suggestion in name_match_list[0:parameters['name choices']]:
        new_name = input(f'Name (suggestion: {suggestion}): ')
        if not new_name:
            name_matches[name] = suggestion
        else:
            name_matches[name] = new_name
    return name_matches
    
def degender_book(book_soup, parameters = DEFAULT_PARAMETERS):
    parameters = fill_defaults(parameters)
    name_dict = get_name_dict(book_soup)
    name_list = get_sorted_name_list(drop_low(name_dict)) #Removing names with few occurrences
    parameters['name matches'] = get_name_matches(name_list, parameters)
    if parameters['verbose']:
        for soup in book_soup:
            degender_soup(soup, parameters)
    for soup in book_soup:
        degender_soup(soup, parameters)
