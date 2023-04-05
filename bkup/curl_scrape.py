import os
import subprocess
import time
import random

def random_time():
    base = random.randint(1,4)
    fraction = random.random()
    return base + fraction

def curl_get(link, destination=None, output=True, random_sleep=False, nva=None, token=None):
    cwd = os.getcwd()
    if destination:
        os.chdir(destination)
    if nva or token:
        link += '?'
    if nva:
        link += 'nva='
        link += nva
    if token:
        if nva:
            link += '&'
        link += 'token='
        link += token
    if output:
        subprocess.run(['curl', '-O', '-J', link])
    else:
        subprocess.run(['curl', link])
    if destination:
        os.chdir(cwd)
    if random_sleep:
        time.sleep(random_time())
