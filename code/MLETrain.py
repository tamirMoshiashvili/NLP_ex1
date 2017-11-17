import random
import sys
from collections import Counter
from time import time

START = '_START_'
UNK = '_UNK_'


def write_to_file_mle(counter, filename):
    mle_file = open(filename, 'w')
    for tup, num in counter.iteritems():
        if len(tup) >= 1:
            mle_file.write(tup[0])
        if len(tup) >= 2:
            mle_file.write(' ' + tup[1])
        if len(tup) == 3:
            mle_file.write(' ' + tup[2])
        mle_file.write('\t' + str(num) + '\n')
    mle_file.close()


def add_to_counter(counter, keys):
    for key in keys:
        if key in counter:
            counter[key] += 1
        else:
            counter[key] = 1


if __name__ == '__main__':
    # read and collect data on the text
    t = time()

    train_file = open(sys.argv[1], 'r')
    lines = train_file.read().splitlines()
    train_file.close()
    q_mle_counter = dict()
    e_mle_counter = dict()

    for line in lines:
        words_iter = iter(line.split(' '))

        # first 2 items - e.mle update
        tag2 = tag1 = START
        add_to_counter(q_mle_counter, [(tag2,), (tag1,), (tag2, tag1)])

        is_UNK_line = random.randint(1, 2) == 1
        for item in words_iter:
            word, tag = item.rsplit('/', 1)
            if is_UNK_line:
                word = UNK

            # update counters
            add_to_counter(e_mle_counter, [(word, tag)])
            add_to_counter(q_mle_counter, [(tag,), (tag1, tag), (tag2, tag1, tag)])

            # update last 2 tags
            tag2 = tag1
            tag1 = tag

    # write to mle-files
    write_to_file_mle(q_mle_counter, sys.argv[2])
    write_to_file_mle(e_mle_counter, sys.argv[3])

    print time() - t
