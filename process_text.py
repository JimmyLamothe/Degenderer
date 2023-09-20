from degenderer import degender_text_box, get_names

def process_text(text, parameters):
    new_text = degender_text_box(text, parameters)
    return new_text

def get_all_names(text):
    return get_names(text)
