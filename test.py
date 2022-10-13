import sys

from librarian import check_out, create_epub, create_soup, get_book_items
from librarian import get_paragraph_list, get_paragraph_text, item_to_soup, pause
from librarian import soup_to_book
from degenderer import degender_book

if len(sys.argv) > 1:
    verbose=True
else:
    verbose=False
    
book = check_out('Jane Eyre')

book_soup = create_soup(book)

degender_book(book_soup, verbose=verbose)

soup_to_book(book_soup, book)
    
create_epub(book, 'test.epub')

sys.exit(0)

paragraph_list = get_paragraph_list(book_soup)

for paragraph in paragraph_list:
    print(get_paragraph_text(paragraph))

if not paragraph_list:
    print('Failed to get paragraph list')
    sys.exit(0)

def add_foo(paragraph):
    paragraph.append(': FOO!')
    
for paragraph in paragraph_list:
    try:
        add_foo(paragraph)
    except AttributeError:
        input('Attribute Error. Press enter to continue')
        pass

soup_to_book(book_soup, book)
    
create_epub(book, 'test.epub')
B
