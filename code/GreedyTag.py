import StringIO
import sys
from time import time

from DataHandler import DataHandler


if __name__ == '__main__':
    t = time()

    args = sys.argv[1:]
    input_filename = args[0]
    q_mle_filename = args[1]
    e_mle_filename = args[2]
    out_filename = args[3]

    # read input file
    input_file = open(input_filename, 'r')
    lines = input_file.read().splitlines()
    input_file.close()

    data_handler = DataHandler(q_mle_filename, e_mle_filename)
    stream = StringIO.StringIO()
    for line in lines:
        words = iter(line.split(' '))
        tag2 = tag1 = '_START_'

        # first word of the line
        word0 = next(words)
        tag1 = data_handler.get_optimal_tag(word0, tag2, tag1)
        stream.write(word0 + '/' + tag1)

        for word in words:
            tag = data_handler.get_optimal_tag(word, tag2, tag1)
            stream.write(' ' + word + '/' + tag)

            tag2 = tag1
            tag1 = tag

        # end of line
        stream.write('\n')

    out_file = open(out_filename, 'w')
    out_file.write(stream.getvalue())
    out_file.close()

    print time() - t
