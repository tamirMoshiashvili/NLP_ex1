from collections import Counter


def get_counter(filename):
    counter = Counter()
    f = open(filename, 'r')
    lines = f.read().splitlines()
    f.close()
    for line in lines:
        words, num = line.split('\t')
        words = words.split(' ')
        if len(words) == 1:
            words = (words[0],)
        else:
            words = tuple(words)
        counter[words] = num
    return counter


class DataHandler:
    def __init__(self, q_filename, e_filename, lamdas=None):
        # assign members
        self._q_counter = get_counter(q_filename)
        self._e_counter = get_counter(e_filename)
        if lamdas:
            self._lamdas = lamdas
        else:
            self._lamdas = [0.8, 0.15, 0.05]

        # more data manipulation
        self._count_special()
        self._prefixes = ['anti', 'de', 'dis', 'en', 'em', 'fore', 'in', 'im', 'il', 'ir', 'mid', 'mis', 'non', 'over',
                          'pre', 're', 'semi', 'sub', 'super', 'trans', 'un']
        self._suffixes = ['ble', 'al', 'ed', 'en', 'er', 'est', 'ful', 'ic', 'ing', 'ion', 'ty', 'ive', 'less', 'ly',
                          'ment', 'ness', 'ous', 'es']
        self._prefix_counter = Counter()
        self._suffix_counter = Counter()

    def _count_special(self):
        """
        Go over e_counter and check for:
        - unknown words
        - prefixes
        - suffixes
        """
        for (word, tag), num in self._e_counter:
            # check for unknown word
            if num == 1:
                self._e_counter.update([('_UNK_', tag)])
            # check for prefix
            for prefix in self._prefixes:
                if word.startswith(prefix):
                    self._prefix_counter.update([(prefix, tag)])
                    break
            # check for suffix
            for suffix in self._suffixes:
                if word.endswith(suffix):
                    self._suffix_counter.update([(suffix, tag)])
                    break

    def _get_q(self, t1, t2, t3):
        """
        return q(t3 | t1, t2)
        """
        first = self._q_counter[(t1, t2, t3)] / float(self._q_counter[(t1, t2)])
        second = self._q_counter[(t2, t3)] / float(self._q_counter[(t2,)])
        third = self._q_counter[(t3,)] / float(sum(self._e_counter.values()))
        return self._lamdas[0] * first + self._lamdas[1] * second + self._lamdas[2] * third

    def _get_e(self, word, tag):
        """
        return e(word | tag)
        """
        first = self._e_counter[(word, tag)]
        if first == 0:  # the given word is uknown
            # unk counting
            unk_c = self._e_counter[('_UNK_', tag)]

            # prefix counting
            prefix_c = 0
            for (prefix, pre_tag), num in self._prefix_counter:
                if pre_tag == tag and word.startswith(prefix):
                    prefix_c = num
                    break

            # suffix counting
            suffix_c = 0
            for (suffix, suff_tag), num in self._suffix_counter:
                if suff_tag == tag and word.endswith(suffix):
                    suffix_c = num
                    break

            # get the max of them
            # TODO: maybe set 'first' as the average of three of them
            first = max([unk_c, prefix_c, suffix_c])

        second = self._q_counter[(tag,)]
        p = float(first) / second
        return p


if __name__ == '__main__':
    dh = DataHandler('q.mle', 'e.mle')
    pass
