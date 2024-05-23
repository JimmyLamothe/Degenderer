"""
This module creates dataframes from all our reference files of pronouns and names
"""

import pandas as pd

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

def get_number_of_pronouns(male, female):
    """ Gets the number of pronouns that will need to be processed for deregendering """
    number_of_pronouns = 0
    if not male == 'm':
        number_of_pronouns += len(MALE_PRONOUNS)
    if not female == 'f':
        number_of_pronouns += len(FEMALE_PRONOUNS)
    return number_of_pronouns
