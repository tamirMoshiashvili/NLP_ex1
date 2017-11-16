import sys
from collections import Counter


def write_to_file_mle(counter, filename):
    mle_file = open(filename, 'w')
    for tup, num in counter.items():
        if len(tup) >= 1:
            mle_file.write(tup[0])
        if len(tup) >= 2:
            mle_file.write(' ' + tup[1])
        if len(tup) == 3:
            mle_file.write(' ' + tup[2])
        mle_file.write('\t' + str(num) + '\n')
    mle_file.close()


if __name__ == '__main__':
    # read and collect data on the text
    train_file = open(sys.argv[1], 'r')
    lines = train_file.read().splitlines()
    q_mle_counter = Counter()
    e_mle_counter = Counter()
    for line in lines:
        words_iter = iter(line.split(' '))

        # first 2 items - e.mle update
        tag2 = '_start_'
        prev_1 = next(words_iter).rsplit('/', 1)
        tag1 = prev_1[1]
        e_mle_counter.update([(prev_1[0], tag1)])
        q_mle_counter.update([(tag1,), (tag2, tag1)])

        for item in words_iter:
            word, tag = item.rsplit('/', 1)

            # update counters
            e_mle_counter.update([(word, tag)])
            q_mle_counter.update([(tag,), (tag1, tag), (tag2, tag1, tag)])

            # update last 2 tags
            tag2 = tag1
            tag1 = tag

    # write to mle-files
    write_to_file_mle(q_mle_counter, sys.argv[2])
    write_to_file_mle(e_mle_counter, sys.argv[3])

    train_file.close()
