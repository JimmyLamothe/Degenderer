#Used to retrieve HTML page from internet

import sys
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_html(page_address,
             basepath = 'html/',
             filename = None,
             overwrite = False,
             module = 'requests'):
    print(page_address)
    last_slash_index = page_address.rfind('/')
    if not filename:
        filename = basepath + page_address[last_slash_index + 1:] + '.html'
    else:
        filename = basepath + filename
    if overwrite == False:
        try:
            with open(filename, 'r') as testfile:
                print('File already exists, skipping.')
                return True #Only returns if file skipped, otherwise action taken.
        except FileNotFoundError:
            pass
    print('Currently downloading: ' + filename)
    if module == 'urlopen':
        page = urlopen(page_address)
    else:
        response = requests.get(page_address)
        print(response.status_code)
        page = response.text
        with open(filename, 'w') as html_file:
            html_file.write(page)
        return
    soup = BeautifulSoup(page, 'html.parser')
    with open(filename, 'w') as html_file:
        html_file.write(soup.prettify())

def print_html(page_address): #test function, to be deleted
    page = urlopen(page_address)
    soup = BeautifulSoup(page, 'html.parser')
    print(soup)
    
#Used to run from terminal
try:
    get_html(sys.argv[1])
except IndexError:
    pass
