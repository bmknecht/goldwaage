'''output of results into html files'''

import codecs
import StringIO

from jinja2 import Environment, PackageLoader


class SnippetGenerator(object):
    def __init__(self):
        self._text = ''

    def handle_event(self, end_of_file_event):
        self._text = end_of_file_event.rawtext

    def get_snippet(self, startindex, endindex):
        return self._text[startindex:endindex]


def _annihilate_zero_weights(words_and_weights):
    '''delete words with weight < 0'''
    return {
        word: weight_and_snippet
        for word, weight_and_snippet
        in words_and_weights.items()
        if weight_and_snippet[0] > 0}


def _highlight_word_of_interest(text_snippet, word):
    def _get_highlighted_word(index):
        return u'<b>' + text_snippet[index:index+len(word)] + u'</b>'

    def _find_word():
        def _is_word():
            return ((index_found == 0 or
                    not text_snippet[index_found-1].isalnum()) and
                    (index_found+len(word) >= len(text_snippet) or
                    not text_snippet[index_found+len(word)].isalnum()))

        index_found_before = 0
        index_found = text_snippet.lower().find(word)
        while index_found != -1:
            if _is_word():
                yield index_found_before, index_found
                index_found_before = index_found+len(word)
            index_found = text_snippet.lower().find(
                word, index_found+len(word))

    html_string = StringIO.StringIO()
    for prev_index, index in _find_word():
        html_string.write(text_snippet[prev_index:index])
        html_string.write(_get_highlighted_word(index))
    return html_string.getvalue()


def _check_spelling(word, text_with_word):
    index = text_with_word.lower().find(word)
    return text_with_word[index:index+len(word)]


def _generate_wordlist_html(
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
    env.filters['drop_boring_entries'] = _annihilate_zero_weights
    env.filters['highlight_word_of_interest'] = _highlight_word_of_interest
    env.filters['check_spelling'] = _check_spelling
    _generate_wordlist_html(
        words_and_weighted_frequencies, env, snippet_generator)
