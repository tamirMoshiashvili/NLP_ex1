def read_file(filepath):
    f = open(filepath, 'r')
    lines = f.read().splitlines()
    f.close()
    return get_list_of_words(lines)


def get_list_of_words(lines):
    words = []
    for line in lines:
        words.extend(line.split(' '))
    return words


if __name__ == '__main__':
    good = bad = 0.0

    # extract text
    test_words = read_file('/home/tamir/PycharmProjects/NLP_ex1/data/ass1-tagger-test-copy')
    pred_words = read_file('output_file.txt')

    # compare
    for (test, pred) in zip(test_words, pred_words):
        w1, t1 = test.rsplit('/', 1)
        w2, t2 = pred.rsplit('/', 1)

        if t1 == t2:
            good += 1
        else:
            bad += 1
            print 'test: ' + t1 + ', pred: ' + t2

    print good / (good + bad)
