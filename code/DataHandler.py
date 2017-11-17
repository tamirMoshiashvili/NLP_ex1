from collections import Counter


def smart_div(x, y):
    if y == 0:
        return 0
    return float(x) / y


def add_to_counter(counter, keys):
    for key in keys:
        if key in counter:
            counter[key] += 1
        else:
            counter[key] = 1


def add_to_e_counter(counter, keys):
    for word, (tag, num) in keys:
        if word in counter:
            if tag in counter[word]:
                counter[word][tag] += num
            else:
                counter[word][tag] = num
        else:
            counter[word] = dict()
            counter[word][tag] = num


def get_e_counter(filename):
    counter = dict()
    total_words = 0

    f = open(filename, 'r')
    lines = f.read().splitlines()
    f.close()

    for line in lines:
        words, num = line.rsplit('\t', 1)
        word, tag = words.split(' ')

        tag_dict = dict()
        tag_dict[tag] = int(num)
        total_words += tag_dict[tag]

        counter[word] = tag_dict
    return counter, total_words


def get_q_counter(filename):
    counter = Counter()

    f = open(filename, 'r')
    lines = f.read().splitlines()
    f.close()

    for line in lines:
        words, num = line.rsplit('\t', 1)
        words = words.split(' ')

        if len(words) == 1:
            words = (words[0],)
        else:
            words = tuple(words)
        counter[words] = int(num)
    return counter


class DataHandler:
    def __init__(self, q_filename, e_filename, lamdas=None):
        # assign members
        self._q_counter = get_q_counter(q_filename)
        self._e_counter, self._total_words = get_e_counter(e_filename)
        if lamdas:
            self._lamdas = lamdas
        else:
            self._lamdas = [0.8, 0.15, 0.05]

        # more data manipulation
        self._prefixes = ['anti', 'de', 'dis', 'en', 'em', 'fore', 'in', 'im', 'il', 'ir', 'mid', 'mis', 'non', 'over',
                          'pre', 're', 'semi', 'sub', 'super', 'trans', 'un']
        self._suffixes = ['ble', 'al', 'ed', 'en', 'er', 'est', 'ful', 'ic', 'ing', 'ion', 'ty', 'ive', 'less', 'ly',
                          'ment', 'ness', 'ous', 'es']
        self._prefix_counter = Counter()
        self._suffix_counter = Counter()
        self.tags = set()
        self._count_special()

    @property
    def tags(self):
        return self.tags

    @tags.setter
    def tags(self, value):
        pass

    def _count_special(self):
        """
        Go over e_counter and check for:
        - unknown words
        - prefixes
        - suffixes
        Fill the tag-set.
        """
        for word, tag_dict in self._e_counter.items():
            # fill tag set
            # self.tags.add(tag)

            # check for unknown word
            for tag, num in tag_dict.items():
                # check for prefix
                for prefix in self._prefixes:
                    if word.startswith(prefix):
                        add_to_counter(self._prefix_counter, [(prefix, tag)])
                        break

                # check for suffix
                for suffix in self._suffixes:
                    if word.endswith(suffix):
                        add_to_counter(self._suffix_counter, [(suffix, tag)])
                        break

    def get_q(self, t1, t2, t3):
        """
        return q(t3 | t1, t2)
        """
        first = smart_div(self._q_counter[(t1, t2, t3)], self._q_counter[(t1, t2)])
        second = smart_div(self._q_counter[(t2, t3)], self._q_counter[(t2,)])
        third = smart_div(self._q_counter[(t3,)], self._total_words)
        return self._lamdas[0] * first + self._lamdas[1] * second + self._lamdas[2] * third

    def get_e(self, word, tag):
        """
        return e(word | tag)
        """
        first = 0
        e_word_dict = self._e_counter[word]
        if tag in e_word_dict:
            first = e_word_dict[tag]

        if first == 0:  # the given word is unknown
            # unk counting
            unk_c = self._e_counter['_UNK_'][tag]

            # prefix counting
            prefix_c = 0
            for prefix in self._prefixes:
                if word.startswith(prefix):
                    prefix_c = self._prefix_counter[(prefix, tag)]
                    break

            # suffix counting
            suffix_c = 0
            for suffix in self._suffixes:
                if word.endswith(suffix):
                    suffix_c = self._suffix_counter[(suffix, tag)]
                    break

            first = (unk_c + prefix_c + suffix_c) / 3.0

            # get the max of them
            # TODO: maybe set 'first' as the average of three of them
            # first = max([unk_c, prefix_c, suffix_c])

        second = self._q_counter[(tag,)]
        p = smart_div(first, second)
        return p

    def get_optimal_tag(self, word, tag2, tag1):
        opt_tag = None
        p = 0

        if word not in self._e_counter:
            word = '_UNK_'
        for tag in self._e_counter[word]:
            e = self.get_e(word, tag)
            q = self.get_q(tag2, tag1, tag)
            e_q = e * q
            if e_q > p:
                opt_tag = tag
                p = e_q
        return opt_tag
