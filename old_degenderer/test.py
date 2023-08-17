import sys

from librarian import check_out, create_epub, create_soup, get_book_items
from librarian import get_paragraph_list, get_paragraph_text, item_to_soup, pause
from librarian import soup_to_book, get_book_text
from degenderer import degender_book

if len(sys.argv) > 1:
    gender = sys.argv[1]
    if gender not in ['m','f','nb']:
        print('Invalid gender, exiting')
        sys.exit(0)
else:
    gender = 'nb'

book = check_out('Jane Eyre')

book_soup = create_soup(book)

parameters = {'verbose':False, 'year':1847, 'gender':gender}

degender_book(book_soup, parameters)

soup_to_book(book_soup, book)
    
create_epub(book, 'test.epub')

print(get_book_text(book_soup))

sys.exit(0)
