from degenderer import degender_text, get_text_names, get_text_dict

def process_text(text, parameters):
    new_text = degender_text(text, parameters)
    print(f'new text: {new_text}')
    return new_text

def get_known_names(text):
    name_dict = get_text_dict(text)
    name_list = []
    for key, value in sorted(name_dict.items(), key = lambda x: x[1], reverse=True):
        name_list.append(key)
    return name_list

def get_potential_names(text):
    name_dict = get_text_names(text)
    short_name_dict = {key: value for key, value in name_dict.items() if value >= 5}
    name_list = []
    for key, value in sorted(short_name_dict.items(), key = lambda x: x[1], reverse=True):
        name_list.append(key)    
    return name_list



