'''output of results into html files'''

import codecs

from jinja2 import Environment, PackageLoader


class SnippetGenerator(object):
    def __init__(self):
        self._text = ''

    def handle_event(self, end_of_file_event):
        self._text = end_of_file_event.rawtext

    def get_snippet(self, startindex, endindex):
        return self._text[startindex:endindex]


def __annihilate_zero_weights(words_and_weights):
    '''delete words with weight < 0'''
    return {
        word: weight_and_snippet
        for word, weight_and_snippet
        in words_and_weights.items()
        if weight_and_snippet[0] > 0}


def __generate_wordlist_html(
        words_and_weighted_frequencies, env, snippet_generator):
    '''write html file with words and weights'''
    get_weight = lambda x: x[0]
    template = env.get_template('wordlist.html')

    bad_occurrences_per_word = {}
    for word, weights in words_and_weighted_frequencies.items():
        worst_occ = max(weights, key=get_weight)
        bad_occurrences_per_word[word] = (
            worst_occ[0],
            snippet_generator.get_snippet(worst_occ[1], worst_occ[2])
        )

    with codecs.open('wordlist.html', mode='w', encoding='utf-8') as htmlfile:
        htmlfile.write(template.render(
            words_and_frequencies=bad_occurrences_per_word,
        ))


def generatehtml(words_and_weighted_frequencies, snippet_generator):
    '''output results as html'''
    env = Environment(loader=PackageLoader('goldwaage', 'templates'))
    env.filters['drop_boring_entries'] = __annihilate_zero_weights
    __generate_wordlist_html(
        words_and_weighted_frequencies, env, snippet_generator)
