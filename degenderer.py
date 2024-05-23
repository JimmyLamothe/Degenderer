"""
This is where the de/regendering takes place.
"""
import random
import json
from timeit import default_timer as timer
import regex
from flask_sse import sse
from librarian import get_book_text, is_string
from reference_library import MALE_PRONOUNS, FEMALE_PRONOUNS #DataFrames
from reference_library import NB_NAMES, GIRL_NAMES, BOY_NAMES, ALL_NAMES, ALL_PRONOUNS #Lists
from reference_library import COMMON_WORDS, WARNING_WORDS #Lists

book_timer = 0
#soup_timer = 0 #Uncomment for optimization testing

def get_suggestion(name_list, names_used):
    """ Suggests a name from a list if it's not already in use """
    available_names = [name for name in name_list if not name in names_used]
    if available_names:
        selection = random.choice(available_names)
        return selection
    selection = random.choice(name_list)
    return selection

def suggest_name(gender, names_used):
    """ Suggests a name from the requested gender """
    if gender == 'nb':
        return get_suggestion(NB_NAMES, names_used)
    if gender == 'f':
        return get_suggestion(GIRL_NAMES, names_used)
    if gender == 'm':
        return get_suggestion(BOY_NAMES, names_used)
    return ''

def fix_text(text):
    """ Various fixes needed due to search and replace ordering issues

    Since we check pronouns one at a time, we need to temporarily add a marker (àéà)
    to each changed pronouns to avoid it being changed back later. We also have a few
    fixes for old default choices that caused other problems, since the user might
    ask for the same substitution we used to use ourselves.
    """
    text = regex.sub(r'àéà', '', text)
    text = regex.sub(r'His/Him/Hers', 'Her/Hers', text)
    text = regex.sub(r'Their/Them/Hers', 'Her/Hers', text)
    text = regex.sub(r'Their/Hers', 'Her/Hers', text)
    text = regex.sub(r'their/hers', 'her/hers', text)
    text = regex.sub(r'his/him/hers', 'her/hers', text)
    text = regex.sub(r'their/them/hers', 'her/hers', text)
    return text

def degender_text(text, parameters):
    """ De/regender a string according to the given parameters """
    start = timer()
    match_dict = parameters['match dict']
    for key in match_dict:
        key_dict = match_dict[key]
        text = regex.sub(key_dict['pattern'], key_dict['replacement'], text)
    end = timer()
    global book_timer
    book_timer += (end-start)
    #global soup_timer #Uncomment for optimization testing
    #soup_timer += (end-start) #Uncomment for optimization testing
    return fix_text(text)


def degender_text_box(text, parameters):
    """ De/regender a string from the text box submission page """
    pronoun_dict = create_pronoun_dict(parameters)
    name_dict = create_name_dict(parameters)
    match_dict = {**pronoun_dict, **name_dict}
    parameters['match dict'] = match_dict
    return degender_text(text, parameters)

def degender_all(item, parameters):
    """ De/regender a soup from Beautiful Soup """
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
    """ Creates a dictionary of pronouns and gendered words to replace """
    if parameters.get('modifying', False): #If pronouns have already been modified
        return {} #We return an empty dict to skip pronoun processing
    pronoun_dict = {}
    if parameters['female'] == 'nb':
        female_match = 'NB'
    elif parameters['female'] == 'm':
        female_match = 'Opposite'
    else:
        female_match = None #No change - same gender as original
    if parameters['male'] == 'nb':
        male_match = 'NB'
    elif parameters['male'] == 'f':
        male_match = 'Opposite'
    else:
        male_match = None #No change - same gender as original
    def process_df(gender_match, df):
        if gender_match:
            for _index, row in df.iterrows():
                original = row['Original']
                match = row[gender_match]
                match_case = row['Match case']
                pronoun_dict[original] = {'match':match,
                                          'pattern':regex.compile(r'\b' + original + r'\b'),
                                          'replacement': match + 'àéà'}
                if match_case:
                    pronoun_dict[original.title()] = {'match':match.title(),
                                                      'pattern':regex.compile(r'\b'
                                                                              + original.title()
                                                                              + r'\b'),
                                                      'replacement': match.title() + 'àéà'}
                    pronoun_dict[original.upper()] = {'match':match.upper(),
                                                      'pattern':regex.compile(r'\b'
                                                                              + original.upper()
                                                                              + r'\b'),
                                                      'replacement': match.upper() + 'àéà'}
    process_df(female_match, FEMALE_PRONOUNS)
    process_df(male_match, MALE_PRONOUNS)
    return pronoun_dict

def create_name_dict(parameters):
    """ Creates a dictionary of replacements for user-submitted names and words """
    all_matches = parameters['all matches']
    name_dict = {}
    for word in all_matches:
        match = all_matches[word]
        name_dict[word] = {'match':match,
                           'pattern':regex.compile(r'\b' + word + r'\b'),
                           'replacement': match + 'àéà'}
        name_dict[word.title()] = {'match':match.title(),
                                   'pattern':regex.compile(r'\b' + word.title() + r'\b'),
                                   'replacement': match.title() + 'àéà'}
        name_dict[word.upper()] = {'match':match.upper(),
                                   'pattern':regex.compile(r'\b' + word.upper() + r'\b'),
                                   'replacement': match.upper() + 'àéà'}
    return name_dict

def degender_book(book_soup, parameters, session_id=None):
    """ De/regenders the Beautiful Soup version of an ePub book """
    pronoun_dict = create_pronoun_dict(parameters)
    name_dict = create_name_dict(parameters)
    match_dict = {**pronoun_dict, **name_dict}
    parameters['match dict'] = match_dict
    def save_match_dict():
        with open('reference/test_match_dict.json', 'w') as json_file:
            json_dict = {}
            for key in match_dict:
                json_dict[key] = match_dict[key]['match']
            json.dump(json_dict, json_file)
    #save_match_dict() #Uncomment for testing
    global book_timer
    book_timer = 0
    chapters = len(book_soup)
    for index, soup in enumerate(book_soup):
        #global soup_timer #Uncomment for optimization testing
        if session_id:
            print(f'session.sid = {session_id}')
            sse.publish({"current": index + 1, "total": chapters}, type='progress', channel=session_id)
        degender_all(soup, parameters)
        print(f'Processed chapter {index + 1} of {chapters}') #Uncomment for testing
        #print(f'Degendering times for soup: {soup_timer} seconds') #Uncomment for optimization testing
        #soup_timer = 0 #Uncomment for optimization testing
    #print(f'Degendering times for book {book_timer} seconds:') #Uncomment for optimization testing

    
def get_known_names(text):
    """ Gets list of names in book that are in our list of common names """
    word_list = regex.sub(r'[^\p{Latin}]', ' ', text).split()
    name_list = [word for word in word_list if word in ALL_NAMES]
    name_list = [word for word in name_list if not word in WARNING_WORDS + COMMON_WORDS]
    name_dict = {}
    for name in name_list:
        if name in name_dict:
            name_dict[name] += 1
        else:
            name_dict[name] = 1
    return name_dict

def get_potential_names(text, min_occurrences=5):
    """ Get list of capital words in text that occur more than min_ocurrences """
    pattern = r'(?<!^|[.?!]\s)\b[A-Z][a-z]*\b'
    matches = regex.findall(pattern, text)
    names = []
    for match in matches:
        if not match.lower() in [word.lower() for word in COMMON_WORDS + ALL_PRONOUNS]:
            names += [match]
    name_dict = {}
    for name in names:
        if name in name_dict:
            name_dict[name] += 1
        else:
            name_dict[name] = 1
    short_name_dict = {key: value for key, value in name_dict.items() if value >= min_occurrences}
    return short_name_dict

def split_clean_warning_dict(count_dict):
    """ Splits off names that could also be words from a name count dict """
    warning_dict = {}
    clean_dict = {}
    for key, count in count_dict.items():
        if key in WARNING_WORDS:
            warning_dict[key] = count
        else:
            clean_dict[key] = count
    return (clean_dict, warning_dict)

def combine_dicts(count_dicts):
    """ Combine two count dictionaries where key = name and value = count """
    combined_dict = {}
    for count_dict in count_dicts:
        for key, count in count_dict.items():
            combined_dict[key] = combined_dict.get(key, 0) + count
    return combined_dict

def get_names(text, min_occurrences=5):
    """ Gets all known names and potential names in a text """
    known_name_dict = get_known_names(text)
    potential_name_dict = get_potential_names(text, min_occurrences=min_occurrences)
    temp_tuple = split_clean_warning_dict(known_name_dict)
    known_name_dict = temp_tuple[0]
    warning_name_dict = temp_tuple[1]
    known_names = []
    for key, value in sorted(known_name_dict.items(), key = lambda x: x[1], reverse=True):
        known_names.append(key)
    potential_name_dict = combine_dicts([potential_name_dict, warning_name_dict])
    for key in [key for (key, value) in potential_name_dict.items()]:
        if key in known_names:
            del potential_name_dict[key]
    potential_names = []
    for key, value in sorted(potential_name_dict.items(), key = lambda x: x[1], reverse=True):
        potential_names.append(key)
    return (known_names, potential_names)

def get_book_names(book_soup):
    """ Gets all known and potential names in a Beautiful Soup of an ePub """
    book_text = get_book_text(book_soup)
    name_tuple = get_names(book_text)
    return name_tuple

def get_total_words(book_soup):
    """ Gets total number of words in a Beautiful Soup of an ePub """
    book_text = get_book_text(book_soup)
    total_words = len(book_text.split())
    return total_words
