import sys
from StringIO import StringIO
from time import time

from hmm2.GreedyTagger import GreedyTagger
from hmm1.HMM_DataHandler import DataHandler

START = '_START_'


def read_file(filename):
    f = open(filename, 'r')
    file_lines = f.read().splitlines()
    f.close()
    return file_lines


if __name__ == '__main__':
    t = time()

    input_filename = sys.argv[1]
    q_filename = sys.argv[2]
    e_filename = sys.argv[3]
    output_filename = sys.argv[4]

    tagger = GreedyTagger(DataHandler(q_filename, e_filename))

    lines = read_file(input_filename)
    stream = StringIO()
    for line in lines:
        words = iter(line.split(' '))
        tag2 = tag1 = START

        w0 = next(words)
        tag = tagger.get_opt_tag(w0, tag2, tag1)
        stream.write(w0 + '/' + tag)

        for word in words:
            tag = tagger.get_opt_tag(word, tag2, tag1)
            stream.write(' ' + word + '/' + tag)

            tag2 = tag1
            tag1 = tag

        # end of line
        stream.write('\n')

    out_file = open(output_filename, 'w')
    out_file.write(stream.getvalue())
    out_file.close()

    print time() - t
