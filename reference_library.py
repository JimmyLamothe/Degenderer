import json
import pandas as pd
from collections import OrderedDict

FEMALE_PRONOUNS = pd.read_excel('reference/reference.xlsx', sheet_name='Female pronouns')
MALE_PRONOUNS = pd.read_excel('reference/reference.xlsx', sheet_name='Male pronouns')
ALL_PRONOUNS = FEMALE_PRONOUNS['Original'].values.tolist() + MALE_PRONOUNS['Original'].values.tolist()
names = pd.read_excel('reference/reference.xlsx', sheet_name='Names')
NB_NAMES = names['NB'].dropna().tolist()
GIRL_NAMES = names['Female'].dropna().tolist()
BOY_NAMES = names['Male'].dropna().tolist()
exclusions = pd.read_excel('reference/reference.xlsx', sheet_name='Exclusions')
COMMON_WORDS = exclusions['Common'].dropna().tolist()
WARNING_WORDS = exclusions['Warning'].dropna().tolist()
ALL_NAMES = [name for name in NB_NAMES + GIRL_NAMES + BOY_NAMES
             if not name in COMMON_WORDS + WARNING_WORDS]

"""
#ALL BELOW IS FORMER JSON DATA - not used anymore

#Excludes names that are common words, countries, etc.
with open('reference/all_names.json', 'r') as filename:
    ALL_NAMES = json.load(filename) #List

#Not used currently
with open('reference/all_names_by_decade.json', 'r') as filename:
    ALL_NAMES_BY_DECADE = json.load(filename) #Dict

with open('reference/COMMON_WORDS.json', 'r') as filename:
    COMMON_WORDS = json.load(filename) #List

with open('reference/WARNING_WORDS.json', 'r') as filename:
    WARNING_WORDS = json.load(filename) #List
    
with open('reference/nb_names.json', 'r') as filename:
    NB_NAMES = json.load(filename) #List

#Not used currently
with open('reference/nb_names_by_decade.json', 'r') as filename:
    NB_NAMES_BY_DECADE = json.load(filename) #Dict

#Not used currently
with open('reference/gendered_names.json', 'r') as filename:
    GENDERED_NAMES = json.load(filename) #List

#Not used currently
with open('reference/gendered_names_by_decade.json', 'r') as filename:
    GENDERED_NAMES_BY_DECADE = json.load(filename) #Dict

with open('reference/boy_names.json', 'r') as filename:
    BOY_NAMES = json.load(filename) #List

#Not used currently
with open('reference/boy_names_by_decade.json', 'r') as filename:
    BOY_NAMES_BY_DECADE = json.load(filename) #Dict

with open('reference/girl_names.json', 'r') as filename:
    GIRL_NAMES = json.load(filename) #List

#Not used currently
with open('reference/girl_names_by_decade.json', 'r') as filename:
    GIRL_NAMES_BY_DECADE = json.load(filename) #Dict    

#Not used currently
with open('reference/nb_names_modern.json', 'r') as filename:
    invalid = NB_NAMES + ['Infant', 'Baby', 'Unknown','Lorenza','Elisha','Kalani']
    NB_NAMES_MODERN = [name for name in json.load(filename) if not name in invalid]

#Not used currently
with open('reference/PRONOUN_DICTIONARY.json', 'r') as filename:
    PRONOUN_DICTIONARY = OrderedDict(json.load(filename)) #Dict
    
#Not used currently
with open('reference/NB_PRONOUN_DICT.json', 'r') as filename:
    NB_PRONOUN_DICT = OrderedDict(json.load(filename)) #Dict

with open('reference/MALE_PRONOUN_DICT.json', 'r') as filename:
    MALE_PRONOUN_DICT = OrderedDict(json.load(filename)) #Dict

with open('reference/FEMALE_PRONOUN_DICT.json', 'r') as filename:
    FEMALE_PRONOUN_DICT = OrderedDict(json.load(filename)) #Dict

ALL_PRONOUNS = [key for key in MALE_PRONOUN_DICT] + [key for key in FEMALE_PRONOUN_DICT]
"""
