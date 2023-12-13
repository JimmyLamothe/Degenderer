"""
Get book from web using curl
"""

from get_html import get_html

def download_search_results(search_string, destination = 'html/'):
    """ Download html search results from Project Gutenberg | str --> None """
    query = f'http://gutenberg.org/ebooks/search/?query={search_string}&submit_search=Go%21'
    get_html(query, filename=search_string, basepath=destination, overwrite=True)

def get_book(source, destination='/books'):
    curl_get(source, destination=destination)

download_search_results(input('Enter search text\n'))
