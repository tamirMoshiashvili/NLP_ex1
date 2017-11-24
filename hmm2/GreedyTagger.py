import numpy as np

UNK = '_UNK_'


class GreedyTagger:
    def __init__(self, data_handler):
        self.dh = data_handler

    def get_opt_tag(self, word, tag2, tag1):
        opt_tag = None
        max = -np.inf

        if word not in self.dh.e:
            word = UNK

        for tag in self.dh.e[word]:
            eq = self.dh.get_score(word, tag2, tag1, tag)
            if eq > max:
                max = eq
                opt_tag = tag
        return opt_tag
