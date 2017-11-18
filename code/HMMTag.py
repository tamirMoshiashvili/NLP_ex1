import sys
from StringIO import StringIO
from time import time

from DataHandler import DataHandler


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

    data_handler = DataHandler(q_filename, e_filename)

    lines = read_file(input_filename)
    stream = StringIO()

    for line in lines:
        tags = data_handler.get_tags_viterbi(line)

        word = line[0]
        tag = tags[0]
        stream.write(word + '/' + tag)

        for word, tag in zip(line[1:], tags[1:]):
            stream.write(' ' + word + '/' + tag + '\n')

    out_file = open(output_filename, 'w')
    out_file.write(stream.getvalue())
    out_file.close()

    print time() - t