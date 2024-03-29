import random

def drop_low(dictionary, floor = 3):
    return {key : value for (key, value) in dictionary.items() if value > floor}  

def sorted_by_values(dictionary, reverse=False):
    return [item[0] for item in sorted(dictionary.items(), key=lambda x:x[1], reverse=reverse)]

def lazy_shuffle(lst):
    shuffle_dict = {item:index for (index, item) in enumerate(lst)}
    for item in shuffle_dict:
        shuffle_dict[item] += random.randint(1,int(len(lst)/5))
    shuffled_list = sorted_by_values(shuffle_dict)
    return shuffled_list

def lazy_shuffle_keys(dictionary, reverse=False):
    item_list = sorted_by_values(dictionary, reverse=reverse)
    return lazy_shuffle(item_list)

def get_min_diff(integer, lst):
    minimum = 2000
    for value in lst:
        minimum = min(minimum, abs(value-integer))
        if minimum == 0:
            return 0
    return minimum

def remove_dupes(lst):
    new_list = []
    for value in lst:
        if value in new_list:
            pass
        else:
            new_list.append(value)
    return new_list

#Take an url string and return a filename ending in epub
def url_to_epub(url):
    filename = url.split("/")[-1]
    stem = filename.split('.')[0]
    return stem + '.epub'

#Compare two dicts and return two dicts of matching values and unmatched values
def compare_dicts(dict1, dict2):
    unchanged_matches = {}
    changed_matches = {}
    for key, value in dict1.items():
        if key in dict2 and dict2[key] == value:
            unchanged_matches[key] = value
        else:
            changed_matches[key] = value
    return unchanged_matches, changed_matches
