from memm2.FeatureIds import FeatureIds as FeatureIds
from memm2.liblin import LiblinearLogregPredictor as predictor
from StringIO import StringIO
import sys

START = '_START_'


def argmax(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


class MEMMTagger:
    def __init__(self, model_file, map_file, extra_file):
        self.predictor = predictor(model_file)
        self.vector_creator = FeatureIds(map_file)
        self.tags_for_word = self.get_tag_of_words(extra_file)
        self.labels_by_name = {}
        for key, value in self.vector_creator.labels.iteritems():
            self.labels_by_name[value] = key

    def get_tag_of_words(self, extra_file):
        f = open(extra_file, 'r')
        file_lines = f.read().splitlines()
        f.close()

        words = dict()
        for line in file_lines:
            line = line.split()
            words[line[0]] = line[1:]

        return words

    def tag_file(self, input_file, output_file):
        f = open(input_file, 'r')
        file_lines = f.read().splitlines()
        f.close()

        stream = StringIO()

        for line in file_lines:
            line = line.split(' ')
            tags = self.predict_line(line)

            word = line[0]
            tag = tags[0]
            stream.write(word + '/' + tag)

            for word, tag in zip(line[1:], tags[1:]):
                stream.write(' ' + word + '/' + tag)
            stream.write('\n')

        out_file = open(output_file, 'w')
        out_file.write(stream.getvalue())
        out_file.close()

    def predict_line(self, line):
        all_labels = self.vector_creator.labels.values()
        n = len(line) - 1
        line.append("")
        line.append("")
        bp = [{} for _ in line] + [{}]
        v = [{} for _ in line] + [{}]
        extended_label_list = all_labels + [START]
        for prev_tag in extended_label_list:
            v[0][prev_tag] = {}
            for r in extended_label_list:
                v[0][prev_tag][r] = 0
        v[0][START][START] = 1

        pre_word = pre_pre_word = ""
        prev_prev_tag_set = [START]
        prev_tag_set = [START]
        for i in range(0, n + 1):
            word = line[i]
            if word in self.tags_for_word:
                curr_tag_set = self.tags_for_word[word]
            else:
                curr_tag_set = all_labels

            bp[i + 1] = {}
            v[i + 1] = {}
            for prev_tag in prev_tag_set:
                bp[i + 1][prev_tag] = {}
                v[i + 1][prev_tag] = {}
                for r in curr_tag_set:
                    l = {}
                    r_num = self.labels_by_name[r]
                    for prev_prev_tag in prev_prev_tag_set:
                        vector = self.vector_creator.get_feature_vector(word, pre_word, pre_pre_word, prev_tag,
                                                                        prev_prev_tag, line[i + 1], line[i + 2])
                        result = self.predictor.predict(vector)
                        l[prev_prev_tag] = v[i][prev_prev_tag][prev_tag] * result[r_num]

                    v[i + 1][prev_tag][r] = max(list(l.values()))
                    bp[i + 1][prev_tag][r] = argmax(l)

            pre_pre_word = pre_word
            pre_word = word
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


from time import time

# input_file_name, modelname, feature_map_file, out_file_name, extra_file (from mmem1)
if __name__ == '__main__':
    print "initializing..."
    first = time()

    tagger = MEMMTagger(sys.argv[2], sys.argv[3], sys.argv[5])
    second = time()
    print str(second - first) + ": start tagging file"

    tagger.tag_file(sys.argv[1], sys.argv[4])
    print "Done after : " + str(time() - first)
