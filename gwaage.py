#!/usr/bin/python
'''analyzes a given unicode text from a file to find wrong usage
of multiple words by approximity'''

import argparse


from goldwaage import analyze, output, parser, events


def parsearguments():
    '''parse, validate and return arguments'''
    argparser = argparse.ArgumentParser(
        description='zaehlt vorkomnisse des wortes')
    argparser.add_argument('textfile')
    argparser.add_argument('-l', '--wlength', default=30, type=int)
    args = argparser.parse_args()

    return args


class ObjectFactory(object):
    def __init__(self, windowlength):
        self._event_dispatcher = None
        self._word_occ_collector = None
        self._windowlength = windowlength

    def get_event_dispatcher(self):
        if not self._event_dispatcher:
            self._event_dispatcher = events.EventDispatcher()
        return self._event_dispatcher

    def get_word_occ_collector(self):
        if not self._word_occ_collector:
            self._word_occ_collector = analyze.WordOccurrenceCollector()
            self._event_dispatcher.register_listener(
                parser.WordFound, self._word_occ_collector)
        return self._word_occ_collector

    def get_char_to_word_collector(self):
        char_to_word_collector = parser.CharToWordCollector(
            self.get_event_dispatcher())
        self.get_event_dispatcher().register_listener(
            parser.CharFound, char_to_word_collector)
        self.get_event_dispatcher().register_listener(
            parser.EndOfFile, char_to_word_collector)
        return char_to_word_collector

    def get_snippet_generator(self):
        snippet_generator = output.SnippetGenerator()
        self.get_event_dispatcher().register_listener(
            parser.EndOfFile, snippet_generator)
        return snippet_generator

    def get_weighted_frequencies_calculator(self):
        frequency_calculator = analyze.WeightedFrequenciesCalculator(
            self.get_word_occ_collector(), self._windowlength)
        self.get_event_dispatcher().register_listener(
            parser.ParsingFinished, frequency_calculator)
        return frequency_calculator


def setup_system(windowlength):
    object_factory = ObjectFactory(windowlength)
    event_dispatcher = object_factory.get_event_dispatcher()
    object_factory.get_char_to_word_collector()
    snippet_generator = object_factory.get_snippet_generator()
    frequency_calculator = object_factory.get_weighted_frequencies_calculator()
    return event_dispatcher, frequency_calculator, snippet_generator


def _main():
    '''main function for direct execution'''

    args = parsearguments()
    (event_dispatcher, frequency_calculator,
        snippet_generator) = setup_system(args.wlength)
    parser.parsetext(args, event_dispatcher)
    output.generatehtml(
        frequency_calculator.words_and_weights, snippet_generator)


if __name__ == '__main__':
    _main()
