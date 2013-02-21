'''analyze text to find mistakes'''


import sys

from goldwaage import parser


def countwords(text):
    '''return count of each word in text'''
    wordcount = {}
    for word in text.split():
        if word in wordcount:
            wordcount[word] += 1
        else:
            wordcount[word] = 1

    return wordcount


def get_weighted_frequencies(freqs_per_word, windowwidth):
    '''compute total weight per word

    by its overall frequency and per-window-frequency in text

    '''
    wweight = {}

    print('adding weights...')
    for word, freq_per_window in freqs_per_word.items():
        freqsum = sum(freq_per_window)
        wweight[word] = []

        for freq in freq_per_window:
            weight = float(windowwidth) / freqsum * 0.4 + 0.8
            wweight[word].append((freq - 1) * pow(weight, 5))

    return wweight


def get_frequencies_per_word(text, windowlen, steplen):
    '''computes the count of each word per window'''
    print('analyzing...')

    splittext = text.lower().split()
    word_and_frequencies = {
        word: [] for word in parser.collectwords(text.lower())}

    for i in xrange(0, windowlen+len(splittext), steplen):
        window = splittext[max(i - windowlen, 0): i]
        print "\r{p}%".format(
            p=int(float(i) / (windowlen + len(splittext)) * 100)),
        sys.stdout.flush()
        for word, frequencies in word_and_frequencies.items():
            frequencies.append(window.count(word))
    print
    return word_and_frequencies


def analyzetext(cleantext, wlength, steplen):
    '''calls functions to get frequencies per word, and compute the weights'''
    freqs_per_word = get_frequencies_per_word(
        cleantext,
        wlength,
        steplen)

    return get_weighted_frequencies(freqs_per_word, wlength)
