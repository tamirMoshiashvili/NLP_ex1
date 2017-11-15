import sys
from collections import Counter

"""
TODO: Complete te needed functions specified in assignment of HMM task-1
      Organize the current main-function
"""

if __name__ == '__main__':
    args = sys.argv[1:]

    # read and collect data on the text
    train_file = open(args[0], 'r')
    lines = train_file.read().splitlines()
    e_mle_counter = Counter()
    q_mle_counter = Counter()
    for line in lines:
        words_iter = iter(line.split(' '))

        # first 2 items - e.mle update
        prev_2 = next(words_iter).rsplit('/', 1)
        tag2 = prev_2[1]
        tag1 = None
        try:
            prev_1 = next(words_iter).rsplit('/', 1)
            tag1 = prev_1[1]
            e_mle_counter.update([(prev_2[0], tag2), (prev_1[0], tag1)])

            # first 2 items - q.mle update
            q_mle_counter.update([(tag2,), (tag1,), (tag2, tag1)])
        except StopIteration:
            # in case of short sentences of one word
            e_mle_counter.update([(prev_2[0], tag2)])
            q_mle_counter.update([(tag2,)])

        for item in words_iter:
            word, tag = item.rsplit('/', 1)

            # e.mle update
            e_mle_counter.update([(word, tag)])

            # q.mle update
            q_mle_counter.update([(tag,), (tag1, tag), (tag2, tag1, tag)])

            # update last 2 items
            tag2 = tag1
            tag1 = tag

    # write to q.mle
    q_mle_file = open(args[1], 'w')
    for tup, n in q_mle_counter.items():
        if len(tup) >= 1:
            q_mle_file.write(tup[0])
        if len(tup) >= 2:
            q_mle_file.write(' ' + tup[1])
        if len(tup) >= 3:
            q_mle_file.write(' ' + tup[2])
        q_mle_file.write('\t' + str(n) + '\n')
    q_mle_file.close()

    # write to e.mle
    e_mle_file = open(args[2], 'w')
    for (word, tag), n in e_mle_counter.items():
        e_mle_file.write(word + ' ' + tag + '\t' + str(n) + '\n')
    e_mle_file.close()

    train_file.close()
