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


class WordOccurrenceCollector(object):
    '''receives call at "found word event"'''
    def __init__(self):
        self.indices_per_word = {}
        self.word_counter = 0

    def handle_event(self, event):
        '''saves index of given word'''
        self.indices_per_word.setdefault(event.word.lower(), []).append(
            self.word_counter)
        self.word_counter += 1


class WeightedFrequenciesCalculator(object):
    '''assigns each word occurrence a frequency value'''
    def __init__(self, collector, windowlength):
        self._collector = collector
        self._windowlength = windowlength
        self.words_and_weights = {}

    def _move_window_over_list(self, occurrences):
        def _fit_in_window(begin, end):
            return occurrences[end] - occurrences[begin] < self._windowlength

        def _is_still_in_text(index):
            return index < len(occurrences)

        startindex = 0
        endindex = 0
        while startindex < len(occurrences):
            if (_is_still_in_text(endindex) and
                    _fit_in_window(startindex, endindex)):
                #Fenster kann wachsen
                endindex += 1
            elif (_is_still_in_text(endindex) and
                    _fit_in_window(startindex+1, endindex)):
                #Fenster kann sich bewegen
                startindex += 1
                endindex += 1
            else:
                #Fenster kann nur noch schrumpfen
                startindex += 1
            if endindex != startindex:
                yield endindex-startindex

    def _get_weighted_frequencies(self):
        for word, indices in self._collector.indices_per_word.items():
            freqsum = sum(self._move_window_over_list(indices))

            self.words_and_weights[word] = []
            for freq in self._move_window_over_list(indices):
                weight = float(self._windowlength) / freqsum * 0.4 + 0.8
                self.words_and_weights[word].append(
                    (freq - 1) * pow(weight, 5))

    def handle_event(self, _):
        '''reacts to finished-parsing event'''
        self._get_weighted_frequencies()


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
