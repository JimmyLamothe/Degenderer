from degenderer import add_foo, check_out, create_epub, create_soup, get_book_items
from degenderer import get_paragraph_list, item_to_soup, soup_to_book

book = check_out('Jane Eyre')

book_soup = create_soup(book)

paragraph_list = get_paragraph_list(book_soup)

for paragraph in paragraph_list:
    try:
        add_foo(paragraph)
    except AttributeError:
        pass

soup_to_book(book_soup, book)
    
create_epub(book, 'test.epub')
