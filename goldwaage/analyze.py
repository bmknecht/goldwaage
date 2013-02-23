'''analyze text to find mistakes'''


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
        self.index_of_current_word = 0

    def _add_word_occurrence(self, word, word_start_position):
        if word not in self.indices_per_word:
            self.indices_per_word[word] = []
        self.indices_per_word[word].append(
            (self.index_of_current_word, word_start_position))

    def handle_event(self, event):
        '''saves index of given word'''
        self._add_word_occurrence(event.word.lower(), event.start_position)
        self.index_of_current_word += 1


class WeightedFrequenciesCalculator(object):
    '''assigns each word occurrence a frequency value'''
    def __init__(self, collector, windowlength):
        self._collector = collector
        self._windowlength = windowlength
        self.words_and_weights = {}

    def _move_window_over_occ(self, occurrences, yield_func):
        def _fit_in_window(begin, end):
            return (occurrences[end][0] - occurrences[begin][0] <
                    self._windowlength)

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
                yield yield_func(startindex, endindex)

    def _get_sum_of_word_in_all_windows(self, occurrences):
        return_word_count_in_window = lambda start, end: end - start
        return sum(
            self._move_window_over_occ(
                occurrences, return_word_count_in_window))

    def _get_weights_per_window(self, wordlen, occurrences, weight):
        return_start_and_end = lambda start, end: (start, end)

        def _get_minimal_distance():
            distances = []
            for index in xrange(start, end-1):
                distances.append(occurrences[index+1][0]-occurrences[index][0])
            return min(distances) if distances else 0

        weights = []
        for start, end in self._move_window_over_occ(
                occurrences, return_start_and_end):
            freq = end - start
            weights.append((
                (freq * pow(weight, 1) *
                    pow(float(
                        _get_minimal_distance()) / self._windowlength, 0.5)),
                occurrences[start][1],
                occurrences[end-1][1] + wordlen
            ))
        return weights

    def _calculate_wordweight(self, occurrences):
        return (float(self._windowlength) /
                self._get_sum_of_word_in_all_windows(occurrences) * 0.4 + 0.8)

    def _get_weighted_frequencies(self):
        for word, occurrences in self._collector.indices_per_word.items():
            word_weight = self._calculate_wordweight(occurrences)
            self.words_and_weights[word] = self._get_weights_per_window(
                len(word), occurrences, word_weight)

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
