'''parse text for analyzis'''

import codecs
import re

from goldwaage import events


class WordFound(events.Event):
    '''event: found a word'''
    def __init__(self, word):
        self.word = word


class ParsingFinished(events.Event):
    '''signals end of parsing process'''
    pass


def _generate_parse_events(text, event_dispatcher):
    cleantext = re.sub(u'[^a-zA-Z\xdc\xfc\xe4\xc4\xf6\xd6\xdf\n ]', u' ', text)
    for word in cleantext.split():
        event_dispatcher.fire_event(WordFound(word))
    event_dispatcher.fire_event(ParsingFinished())


def parsetext(args, event_dispatcher):
    '''read text from file and start parsing'''
    text = codecs.open(args.textfile, encoding='utf-8').read()
    _generate_parse_events(text, event_dispatcher)


def collectwords(text):
    '''convert single string to one-string-per-word-list'''
    return set(text.split())
