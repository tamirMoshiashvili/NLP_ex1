START = '_START_'
UNK = '_UNK_'

def argmax(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


class ViterbiTagger:
    def __init__(self, data_handler):
        self.dh = data_handler

    def get_opt_tags(self, line):
        """
        :param line: list of words.
        :return: list of tags such that tag[i] match line[i].
        """
        # init
        n = len(line) - 1
        bp = [{} for _ in line] + [{}]
        v = [{} for _ in line] + [{}]
        for prev_tag in self.dh.tag_set:
            v[0][prev_tag] = {}
            for r in self.dh.tag_set:
                v[0][prev_tag][r] = 0
        v[0][START][START] = 1

        prev_prev_tag_set = [START]
        prev_tag_set = [START]
        for i in range(0, n + 1):
            word = line[i]
            if word in self.dh.e:
                curr_tag_set = self.dh.e[word].keys()
            else:
                curr_tag_set = self.dh.e[UNK].keys()

            bp[i + 1] = {}
            v[i + 1] = {}
            for prev_tag in prev_tag_set:
                bp[i + 1][prev_tag] = {}
                v[i + 1][prev_tag] = {}
                for r in curr_tag_set:
                    l = {}
                    for prev_prev_tag in prev_prev_tag_set:
                        l[prev_prev_tag] = v[i][prev_prev_tag][prev_tag] +\
                                           self.dh.get_score(word, prev_prev_tag, prev_tag, r)

                    v[i + 1][prev_tag][r] = max(list(l.values()))
                    bp[i + 1][prev_tag][r] = argmax(l)

            prev_prev_tag_set = prev_tag_set
            prev_tag_set = curr_tag_set

        # ignore START tag
        bp.pop(0)
        v.pop(0)

        end_matrix = map(lambda x: x.values(), v[n].values())

        max_end = list(map(max, end_matrix))
        max_v = max(max_end)

        max_t_index = max_end.index(max_v)
        max_t = list(v[n].keys())[max_t_index]
        max_r = argmax(v[n][max_t])

        y = [0 for _ in range(0, n + 1)]
        y[n] = max_r
        y[n - 1] = max_t

        # get tags in reverse way
        for i in reversed(range(0, n - 1)):
            y[i] = bp[i + 2][y[i + 1]][y[i + 2]]

        return y
