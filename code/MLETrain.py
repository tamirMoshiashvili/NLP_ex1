import random
import sys
from time import time

START = '_START_'
UNK = '_UNK_'


def write_to_file(filename, counter):
    f = open(filename, 'w')
    for key, num in counter.iteritems():
        f.write(key + '\t' + str(num) + '\n')
    f.close()


def add_to_counter(counter, keys):
    for key in keys:
        if key in counter:
            counter[key] += 1
        else:
            counter[key] = 1


def read_file(filename):
    """
    :return list of lines.
    """
    f = open(filename, 'r')
    file_lines = f.read().splitlines()
    f.close()
    return file_lines


if __name__ == '__main__':
    t = time()
    lines = read_file(sys.argv[1])

    q = dict()
    e = dict()

    for line in lines:
        pairs = line.split(' ')
        tag2 = tag1 = START

        add_to_counter(q, [tag2, tag1, tag2 + ' ' + tag1])

        is_UNK_line = random.randint(1, 20) == 1
        for pair in pairs:
            word, tag = pair.rsplit('/', 1)
            if is_UNK_line:
                word = UNK

            add_to_counter(e, [word + ' ' + tag])
            add_to_counter(q, [tag, tag1 + ' ' + tag, tag2 + ' ' + tag1 + ' ' + tag])

            tag2 = tag1
            tag1 = tag

    write_to_file(sys.argv[2], q)
    write_to_file(sys.argv[3], e)

    print time() - t
