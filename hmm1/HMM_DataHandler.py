def read_file(filename):
    f = open(filename, 'r')
    file_lines = f.read().splitlines()
    f.close()
    return file_lines


def get_e_counter(filename):
    counter = dict()
    total_words = 0
    tagset = set()

    lines = read_file(filename)

    for line in lines:
        words, num = line.rsplit('\t', 1)
        word, tag = words.split(' ')
        tagset.add(tag)

        if word in counter:
            counter[word][tag] = float(num)
        else:
            tag_dict = dict()
            tag_dict[tag] = float(num)
            total_words += tag_dict[tag]
            counter[word] = tag_dict

    return counter, tagset, total_words


def get_q_counter(filename):
    counter = dict()
    lines = read_file(filename)
    for line in lines:
        key, num = line.rsplit('\t', 1)
        counter[key] = float(num)
    return counter


def smart_div(x, y):
    if y == 0:
        return 1e-7
    return float(x) / y


def concat(words):
    w1 = words[0]
    for word in words[1:]:
        w1 += ' ' + word
    return w1


eps = 1e-7
START = '_START_'


class DataHandler:
    def __init__(self, q_filename, e_filename, lamdas=None):
        if lamdas is None:
            lamdas = [0.8, 0.15, 0.05]
        self.q = get_q_counter(q_filename)
        self.e, self.tag_set, self._num_words = get_e_counter(e_filename)
        self._lamdas = lamdas
        self.tag_set.add(START)

    def _get_q_value(self, key):
        """ :return: q[key] """
        if key in self.q:
            return self.q[key]
        return eps

    def get_q_of_tags(self, t1, t2, t3):
        """ :return: q(t3 | t1, t2) """
        first = smart_div(self._get_q_value(concat([t1, t2, t3])), self._get_q_value(concat([t1, t2])))
        second = smart_div(self._get_q_value(concat([t2, t3])), self._get_q_value(t2))
        third = smart_div(self._get_q_value(t3), self._num_words)
        return self._lamdas[0] * first + self._lamdas[1] * second + self._lamdas[2] * third

    def get_e_of(self, word, tag):
        """ :return: e(word | tag) """
        if word in self.e:
            if tag in self.e[word]:
                return self.e[word][tag] / self._get_q_value(tag)
        return eps

    def get_score(self, word, tag2, tag1, tag):
        """ :return: score of the given parameters, which is e * q """
        return self.get_e_of(word, tag) * self.get_q_of_tags(tag2, tag1, tag)
