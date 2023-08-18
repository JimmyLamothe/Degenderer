"""
This is where the degendering takes place.
"""
import regex
import sys
import random
from librarian import get_paragraphs, get_paragraph_text, pause, set_paragraph_text, get_book_text
from librarian import get_divs, get_div_text, set_div_text, is_string
from reference_library import NB_NAMES, NB_NAMES_MODERN, NB_NAMES_BY_DECADE, ALL_NAMES
from reference_library import AMBIGUOUS_NAMES
from reference_library import BOY_NAMES, GIRL_NAMES
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
    if False:#verbose: #this is usually too verbose so is always skipped 
        print('Matching for : ' + pronoun)
        if regex.search(r'\b' + pronoun + r'\b', text):
            print('Pronoun found!')
            print(pronoun + ' will be changed to ' + replacement)
    text = regex.sub(r'\b' + pronoun + r'\b', replacement+'àéà', text)
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

def change_pronouns(text, male, female, verbose=False):
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
    for pronoun in pronoun_dict:
        text = change_pronoun(pronoun, pronoun_dict[pronoun], text, verbose=verbose)    
    return fix_text(text)

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
    
def get_period_names(year, verbose=False):
    """ NOT CURRENTLY USED """
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
    period_names.extend(NB_NAMES_MODERN)
    return period_names

def change_name(name, match, text, verbose=False):
    if False:#verbose:
        print('Matching for : ' + name)
        if regex.search(r"(?<![a-zA-Z'’-])" + name + r"(?![a-zA-Z'’-])", text):
            print('Name found!')
            print(name + ' will be changed to ' + match)
    text = regex.sub(r"(?<![a-zA-Z'’-])" + name + r"(?![a-zA-Z'’-])", match, text)
    return text

def change_names(text, parameters):
    name_matches = parameters['name matches']
    for name in name_matches:
        text = change_name(name, name_matches[name], text, verbose=parameters['verbose'])
    return text
        
def degender_text(text, parameters):
    verbose = parameters['verbose']
    original_text = text
    text = change_pronouns(text, parameters['male'], parameters['female'], verbose=verbose)
    text = change_names(text, parameters)
    if verbose:
        if text != original_text:
            print('Changed pronouns and/or names')
            print('New text:')
            print(text)
    return text

def degender_string(string, parameters):
    if parameters['verbose']:
        print('Pre-text:')
        print(string)
    new_text = degender_text(string, parameters)
    if parameters['verbose']:
        print('Post-text:')
        print(new_text)
    if new_text != string:
        print('returning new text')
        return new_text
    else:
        return False

def degender_tag(tag, tag_type, parameters):
    print(f'pre {tag_type}')
    print(tag)
    new_contents = []
    for (number, child) in enumerate(tag.contents):
        print(number)
        print(child)
        if is_string(child):
            new_string = degender_string(child, parameters)
            if new_string:
                child.replace_with(new_string)
        print(f'post {tag_type}')
        print(tag)
        #pause()
    
def degender_soup(soup, parameters):
    for div in get_divs(soup):
        degender_tag(div, 'div', parameters)
    for p in get_paragraphs(soup):
        degender_tag(p, 'paragraph', parameters)

def degender_all(item, parameters):
    """ Test function to replace degender_soup """
    if is_string(item):
        new_string = degender_string(item, parameters)
        if new_string:
            item.replace_with(new_string)
    try:
        if item.contents:
            for child in item.contents:
                degender_all(child, parameters)    
    except AttributeError:
        pass
    
def get_all_name_matches(name_list, parameters):
    """ NOT CURRENTLY USED """
    period_names = get_period_names(parameters['year'])
    return list(zip(name_list, period_names))
    
def get_name_matches(name_list, parameters):
    """ NOT CURRENTLY USED """
    name_matches = {}
    name_match_list = get_all_name_matches(name_list, parameters)
    import sys
    print('Enter a name for each main character or press ENTER to accept suggestion')
    for name, suggestion in name_match_list[0:parameters['name choices']]:
        #NOTE: functionality removed for web compatibility
        new_name = '' #input(f'Name (suggestion: {suggestion}): ') 
        if not new_name:
            name_matches[name] = suggestion
        else:
            name_matches[name] = new_name
    return name_matches
    
def degender_book(book_soup, parameters = DEFAULT_PARAMETERS):
    parameters = fill_defaults(parameters)
    print(parameters)
    #name_dict = get_name_dict(book_soup)
    #name_list = get_sorted_name_list(drop_low(name_dict)) #Removing names with few occurrences
    #parameters['name matches'] = get_name_matches(name_list, parameters)
    #REMOVED PREVIOUS 2 LINES FOR WEB VERSION
    for soup in book_soup:
        #degender_soup(soup, parameters)
        degender_all(soup, parameters)

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
