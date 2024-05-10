"""
Utility functions used in various modules

Some functions are not used at the moment, but have been left in the module
in case they are needed in the future.
"""

import random

def drop_low(dictionary, floor = 3):
    """ Drop all items with counts below floor in a count dictionary """
    return {key : value for (key, value) in dictionary.items() if value > floor}

def sorted_by_values(dictionary, reverse=False):
    """ Get list of keys in count dict from most common to least """
    return [item[0] for item in sorted(dictionary.items(), key=lambda x:x[1], reverse=reverse)]

def lazy_shuffle(lst):
    """ Shuffle the order of a list, but not too much """
    shuffle_dict = {item:index for (index, item) in enumerate(lst)}
    for item in shuffle_dict:
        shuffle_dict[item] += random.randint(1,int(len(lst)/5))
    shuffled_list = sorted_by_values(shuffle_dict)
    return shuffled_list

def lazy_shuffle_keys(dictionary, reverse=False):
    """ Get list of keys in count dict in not quite descending order """
    item_list = sorted_by_values(dictionary, reverse=reverse)
    return lazy_shuffle(item_list)

def get_min_diff(integer, lst):
    """ Get the smallest gap between values in a list of integers """
    minimum = 2000
    for value in lst:
        minimum = min(minimum, abs(value-integer))
        if minimum == 0:
            return 0
    return minimum

def remove_dupes(lst):
    """ Remove duplicate items from a list """
    new_list = []
    for value in lst:
        if value in new_list:
            pass
        else:
            new_list.append(value)
    return new_list

def url_to_epub(url):
    """ Take an url string and return a filename ending in epub """
    filename = url.split("/")[-1]
    stem = filename.split('.')[0]
    return stem + '.epub'

def compare_dicts(dict1, dict2):
    """ Compare two dicts and get five dicts by category of change

    This is used to modify a book that was already degendered.
    dict1 contains the user-submitted matches for the previous version.
    dict2 contains the matches for the new version.
    We create five dicts according to the changes between versions:

    matching_keys - Keys in both dicts that have the same value
    modified_keys_old - Keys in both dicts that have different values - kv pair from dict1
    modified_keys_new - Keys in both dicts that have different values - kv pair from dict2
    new_keys - Keys that are only in dict2
    removed_keys - Keys that are only in dict1
    """
    matching_keys = {}
    modified_keys_old = {}
    modified_keys_new = {}
    new_keys = {}
    removed_keys = {}
    for key, value in dict1.items():
        if key in dict2:
            if dict2[key] == value:
                matching_keys[key] = value
            else:
                modified_keys_old[key] = dict1[key]
                modified_keys_new[key] = dict2[key]
        else:
            removed_keys[key] = value
    for key, value in dict2.items():
        if not key in dict1:
            new_keys[key] = value
    return matching_keys, modified_keys_old, modified_keys_new, new_keys, removed_keys
