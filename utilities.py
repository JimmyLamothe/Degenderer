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

#Compare two dicts and get four dicts by category of change
def compare_dicts(dict1, dict2):
    matching_keys = {} #key in both dicts, same value
    modified_keys_old = {} #key in both dicts, different value - old key-value pair from dict1
    modified_keys_new = {} #key in both dicts, different value - new key-value pair from dict1
    new_keys = {} #key only in dict2
    removed_keys = {} #key only in dict1
    print(f'dict1: {dict1}')
    print(f'dict2: {dict2}')
    for key, value in dict1.items():
        if key in dict2:
            if dict2[key] == value:
                matching_keys[key] = value
            else:
                print(f'dict1[key]: {dict1[key]}')
                print(f'dict2[key]: {dict2[key]}')
                modified_keys_old[key] = dict1[key]
                modified_keys_new[key] = dict2[key]
        else:
            removed_keys[key] = value
    for key, value in dict2.items():
        if not key in dict1:
            new_keys[key] = value
    return matching_keys, modified_keys_old, modified_keys_new, new_keys, removed_keys
