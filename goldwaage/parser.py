'''parse text for analyzis'''

import codecs
import re


def readtext(args):
    '''returns parseable text

    reads unicode text from file and returns it and a second version of it
    which is stripped of all special characters, numbers,...

    '''
    text = codecs.open(args.textfile, encoding='utf-8').read()
    print('cleaning...')
    cleantext = re.sub(u'[^a-zA-Z\xdc\xfc\xe4\xc4\xf6\xd6\xdf\n ]', u' ', text)

    return cleantext, text


def collectwords(text):
    '''convert single string to one-string-per-word-list'''
    return set(text.split())
