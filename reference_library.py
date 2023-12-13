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
