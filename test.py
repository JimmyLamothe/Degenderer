from process_epub import process_epub
import sys

filename = sys.argv[1]
male = sys.argv[2]
female = sys.argv[3]

parameters = {'male': male, 'female': female}

process_epub(filename, parameters)
