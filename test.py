import sys

from librarian import add_foo, check_out, create_epub, create_soup, get_book_items
from librarian import get_paragraph_list, item_to_soup, soup_to_book

book = check_out('Jane Eyre')

book_soup = create_soup(book)

paragraph_list = get_paragraph_list(book_soup)

if not paragraph_list:
    print('Failed to get paragraph list')
    sys.exit(0)

for paragraph in paragraph_list:
    try:
        add_foo(paragraph)
    except AttributeError:
        input('Attribute Error. Press enter to continue')
        pass

soup_to_book(book_soup, book)
    
create_epub(book, 'test.epub')
