"""
This module de/regenders strings submitted by users using a text box
"""

from degenderer import degender_text_box, get_names

def process_text(text, parameters):
    """ De/regenders a string according to user-submitted parameters """
    new_text = degender_text_box(text, parameters)
    return new_text

def get_all_names(text):
    """ Gets all known and potential names in a string """
    return get_names(text, min_occurrences = 3)
