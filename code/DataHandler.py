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


def is_number(var):
    var = var.replace(',', '').replace(':', '').replace('-', '')
    try:
        float(var)
        return True
    except:
        return False


def argmax(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


eps = 1e-7
UNK = '_UNK_'
START = '_START_'


class DataHandler:
    def __init__(self, q_filename, e_filename, lamdas=None):
        if lamdas is None:
            lamdas = [0.8, 0.15, 0.05]
        self._q = get_q_counter(q_filename)
        self._e, self._tag_set, self._num_words = get_e_counter(e_filename)
        self._lamdas = lamdas
        self._tag_set.add(START)

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

    def get_tags_viterbi(self, line):
        n = len(line) - 1
        bp = [{} for word in line] + [{}]
        v = [{} for word in line] + [{}]
        for t in self._tag_set:
            v[0][t] = {}
            for r in self._tag_set:
                v[0][t][r] = 0
        v[0][START][START] = 1

        prev_prev_tag_set = [START]
        prev_tag_set = [START]
        for i in range(0, n + 1):
            word = line[i]
            curr_tag_set = self._tag_set
            if word in self._e:
                curr_tag_set = self._e[word].keys()

            bp[i + 1] = {}
            v[i + 1] = {}
            for t in prev_tag_set:
                bp[i + 1][t] = {}
                v[i + 1][t] = {}
                for r in curr_tag_set:
                    l = {}
                    for tt in prev_prev_tag_set:
                        l[tt] = v[i][tt][t] * self.get_e_of(word, r) * self.get_q_of_tags(tt, t, r)

                    v[i + 1][t][r] = max(list(l.values()))
                    bp[i + 1][t][r] = argmax(l)

            prev_prev_tag_set = prev_tag_set
            prev_tag_set = curr_tag_set

        bp.pop(0)
        v.pop(0)

        end_matrix = map(lambda x: x.values(), v[n].values())

        max_end = list(map(max, end_matrix))
        max_v = max(max_end)

        max_t_index = max_end.index(max_v)
        max_t = list(v[n].keys())[max_t_index]
        max_r = argmax(v[n][max_t])

        y = [0 for i in range(0, n + 1)]
        y[n] = max_r
        y[n - 1] = max_t

        for i in reversed(range(0, n - 1)):
            y[i] = bp[i + 2][y[i + 1]][y[i + 2]]

        return y
