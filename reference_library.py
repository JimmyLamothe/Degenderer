import json
from collections import OrderedDict

with open('reference/all_names.json', 'r') as filename:
    ALL_NAMES = json.load(filename) #List
    
with open('reference/all_names_by_decade.json', 'r') as filename:
    ALL_NAMES_BY_DECADE = json.load(filename) #Dict

with open('reference/COMMON_WORDS.json', 'r') as filename:
    COMMON_WORDS = json.load(filename) #List

with open('reference/WARNING_WORDS.json', 'r') as filename:
    WARNING_WORDS = json.load(filename) #List
    
with open('reference/nb_names.json', 'r') as filename:
    NB_NAMES = json.load(filename) #List
    
with open('reference/nb_names_by_decade.json', 'r') as filename:
    NB_NAMES_BY_DECADE = json.load(filename) #Dict

with open('reference/gendered_names.json', 'r') as filename:
    GENDERED_NAMES = json.load(filename) #List

with open('reference/gendered_names_by_decade.json', 'r') as filename:
    GENDERED_NAMES_BY_DECADE = json.load(filename) #Dict

with open('reference/boy_names.json', 'r') as filename:
    BOY_NAMES = json.load(filename) #List

with open('reference/boy_names_by_decade.json', 'r') as filename:
    BOY_NAMES_BY_DECADE = json.load(filename) #Dict

with open('reference/girl_names.json', 'r') as filename:
    GIRL_NAMES = json.load(filename) #List

with open('reference/girl_names_by_decade.json', 'r') as filename:
    GIRL_NAMES_BY_DECADE = json.load(filename) #Dict    
    
with open('reference/nb_names_modern.json', 'r') as filename:
    invalid = NB_NAMES + ['Infant', 'Baby', 'Unknown','Lorenza','Elisha','Kalani']
    NB_NAMES_MODERN = [name for name in json.load(filename) if not name in invalid]

with open('reference/PRONOUN_DICTIONARY.json', 'r') as filename:
    PRONOUN_DICTIONARY = OrderedDict(json.load(filename)) #Dict

with open('reference/NB_PRONOUN_DICT.json', 'r') as filename:
    NB_PRONOUN_DICT = OrderedDict(json.load(filename)) #Dict

with open('reference/MALE_PRONOUN_DICT.json', 'r') as filename:
    MALE_PRONOUN_DICT = OrderedDict(json.load(filename)) #Dict

with open('reference/FEMALE_PRONOUN_DICT.json', 'r') as filename:
    FEMALE_PRONOUN_DICT = OrderedDict(json.load(filename)) #Dict

ALL_PRONOUNS = [key for key in MALE_PRONOUN_DICT] + [key for key in FEMALE_PRONOUN_DICT]
