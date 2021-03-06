'''parse text for analyzis'''

import codecs

from goldwaage import events


class CharToWordCollector(object):
    def __init__(self, event_dispatcher):
        self.charlist = []
        self.event_dispatcher = event_dispatcher
        self.end_of_word = 0

    def handle_word_char(self, char, position):
        self.charlist.append(char)
        self.end_of_word = position

    def handle_non_word_char(self):
        if self.charlist:
            self.event_dispatcher.fire_event(
                WordFound(
                    u''.join(self.charlist),
                    self.end_of_word - len(self.charlist) + 1))
            self.charlist = []

    def handle_event(self, event):
        if isinstance(event, CharFound) and event.char.isalnum():
            self.handle_word_char(event.char, event.position)
        else:
            self.handle_non_word_char()


class CharFound(events.Event):
    def __init__(self, char, position):
        self.char = char
        self.position = position


class EndOfFile(events.Event):
    def __init__(self, rawtext):
        self.rawtext = rawtext


class ParsingFinished(events.Event):
    '''signals end of parsing process'''
    pass


class WordFound(events.Event):
    '''event: found a word'''
    def __init__(self, word, start_position):
        self.word = word
        self.start_position = start_position


def _generate_parse_events(text, event_dispatcher):
    for index, char in enumerate(text):
        event_dispatcher.fire_event(CharFound(char, index))
    event_dispatcher.fire_event(EndOfFile(text))


def parsetext(args, event_dispatcher):
    '''read text from file and start parsing'''
    text = codecs.open(args.textfile, encoding='utf-8').read()
    _generate_parse_events(text, event_dispatcher)
    event_dispatcher.fire_event(ParsingFinished())


def collectwords(text):
    '''convert single string to one-string-per-word-list'''
    return set(text.split())
