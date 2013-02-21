'''output of results into html files'''

import codecs

from jinja2 import Environment, PackageLoader


def __annihilate_zero_weights(words_and_weights):
    '''delete words with weight < 0'''
    return {
        word: weight
        for word, weight
        in words_and_weights.items()
        if weight > 0}


def __generate_wordlist_html(words_and_weighted_frequencies, env):
    '''write html file with words and weights'''
    template = env.get_template('wordlist.html')

    with codecs.open('wordlist.html', mode='w', encoding='utf-8') as htmlfile:
        htmlfile.write(template.render(words_and_frequencies={
            word: max(weights)
            for word, weights
            in words_and_weighted_frequencies.items()}
        ))


def generatehtml(words_and_weighted_frequencies):
    '''output results as html'''
    env = Environment(loader=PackageLoader('goldwaage', 'templates'))
    env.filters['drop_boring_entries'] = __annihilate_zero_weights
    __generate_wordlist_html(words_and_weighted_frequencies, env)
