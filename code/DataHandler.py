def read_file(filename):
    f = open(filename, 'r')
    file_lines = f.read().splitlines()
    f.close()
    return file_lines


def get_e_counter(filename):
    counter = dict()
    total_words = 0

    lines = read_file(filename)

    for line in lines:
        words, num = line.rsplit('\t', 1)
        word, tag = words.split(' ')

        if word in counter:
            counter[word][tag] = float(num)
        else:
            tag_dict = dict()
            tag_dict[tag] = float(num)
            total_words += tag_dict[tag]
            counter[word] = tag_dict

    return counter, total_words


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


def is_number(var):
    var = var.replace(',', '').replace(':', '').replace('-', '')
    try:
        float(var)
        return True
    except:
        return False


eps = 1e-7
UNK = '_UNK_'
START = '_START_'


class DataHandler:
    def __init__(self, q_filename, e_filename, lamdas=None):
        if lamdas is None:
            lamdas = [0.8, 0.15, 0.05]
        self._q = get_q_counter(q_filename)
        self._e, self._num_words = get_e_counter(e_filename)
        self._lamdas = lamdas

    def _get_q_value(self, key):
        """ :return: q[key] """
        if key in self._q:
            return self._q[key]
        return eps

    def get_q_of_tags(self, t1, t2, t3):
        """ :return: q(t3 | t1, t2) """
        first = smart_div(self._get_q_value(concat([t1, t2, t3])), self._get_q_value(concat([t1, t2])))
        second = smart_div(self._get_q_value(concat([t2, t3])), self._get_q_value(t2))
        third = smart_div(self._get_q_value(t3), self._num_words)
        return self._lamdas[0] * first + self._lamdas[1] * second + self._lamdas[2] * third

    def get_e_of(self, word, tag):
        """ :return: e(word | tag) """
        if word in self._e:
            if tag in self._e[word]:
                return self._e[word][tag] / self._get_q_value(tag)
        return eps

    def get_opt_tag(self, word, tag2, tag1):
        opt_tag = None
        p = 0

        if is_number(word):
            return 'CD'

        if word not in self._e:
            word = UNK

        for tag in self._e[word]:
            # if tag == START:    # ignore predicting the tag as START
            #     continue

            e = self.get_e_of(word, tag)
            q = self.get_q_of_tags(tag2, tag1, tag)
            eq = e * q
            if eq > p:
                p = eq
                opt_tag = tag
        return opt_tag
