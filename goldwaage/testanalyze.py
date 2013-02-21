'''tests text analysis module'''
import unittest

from goldwaage import analyze


class TestWeightedFrequencyCollector_Window(unittest.TestCase):
    '''test window movement'''
    def test_emptylist(self):
        collector = analyze.WeightedFrequenciesCalculator(None, 30)
        result = list(collector._move_window_over_list([]))
        self.assertEquals([], result)

    def test_1_occ_at_beginning(self):
        collector = analyze.WeightedFrequenciesCalculator(None, 30)
        result = list(collector._move_window_over_list([0]))
        self.assertEquals([1], result)

    def test_1_occ_in_middle(self):
        collector = analyze.WeightedFrequenciesCalculator(None, 30)
        result = list(collector._move_window_over_list([50]))
        self.assertEquals([1], result)

    def test_2_occ_in_seperate_windows(self):
        collector = analyze.WeightedFrequenciesCalculator(None, 30)
        result = list(collector._move_window_over_list([10, 50]))
        self.assertEquals([1, 1], result)

    def test_3_occ_in_seperate_windows(self):
        collector = analyze.WeightedFrequenciesCalculator(None, 30)
        result = list(collector._move_window_over_list([10, 50, 100]))
        self.assertEquals([1, 1, 1], result)

    def test_2_occ_in_same_window(self):
        collector = analyze.WeightedFrequenciesCalculator(None, 30)
        result = list(collector._move_window_over_list([10, 20]))
        self.assertEquals([1, 2, 1], result)

    def test_3_occ_in_same_window(self):
        collector = analyze.WeightedFrequenciesCalculator(None, 30)
        result = list(collector._move_window_over_list([10, 15, 20]))
        self.assertEquals([1, 2, 3, 2, 1], result)

    def test_4_occ_in_pairs(self):
        collector = analyze.WeightedFrequenciesCalculator(None, 30)
        result = list(collector._move_window_over_list([10, 15, 110, 115]))
        self.assertEquals([1, 2, 1, 1, 2, 1], result)


if __name__ == '__main__':
    unittest.main()
