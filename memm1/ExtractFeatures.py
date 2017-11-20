import sys
from StringIO import StringIO

START = '_START_'


def read_file(filename):
    """
    :return list of lines, each line is a list of (word, tag) tuples.
    """
    f = open(filename, 'r')
    file_lines = f.read().splitlines()
    f.close()

    for i, line in enumerate(file_lines):
        line = line.split(' ')
        file_lines[i] = line
        for j, pair in enumerate(line):
            word, tag = pair.rsplit('/', 1)
            file_lines[i][j] = (word, tag)  # TODO: need to check the alert - says that it is a string
    return file_lines


def get_words_counter(lines):
    """
    :param lines: list of lines, each line is a list of (word, tag) tuples.
    :return: counter that maps word to number of times it appeared.
    """
    counter = dict()
    for line in lines:
        for word, tag in line:
            if word in counter:
                counter[word] += 1
            else:
                counter[word] = 1
    return counter


def fill_with_regular_features(features_dict, line, i):
    """
    :param features_dict: features dictionary.
    :param line: list of (word, tag) tuples.
    :param i: index of the current tuple in line.
    """
    if i > 0:
        prev_word, prev_tag = line[i - 1]
        features_dict['prev_word'] = prev_word
        features_dict['prev_tag'] = prev_tag
    else:
        features_dict['prev_tag'] = START
    if i > 1:
        prev_prev_word, prev_prev_tag = line[i - 2]
        features_dict['prev_prev_word'] = prev_prev_word
        features_dict['prev_2_tags'] = prev_prev_tag + '/' + line[i - 1][1]
    else:
        features_dict['prev_2_tags'] = START + '/' + START

    n = len(line)
    if i < n - 1:
        features_dict['next_word'] = line[i + 1][0]
    if i < n - 2:
        features_dict['next_next_word'] = line[i + 2][0]


def is_rare(counter, w):
    """
    Check if the given word is rare, according to the MEMM-paper.
    :return: boolean.
    """
    return counter[w] < 5


def fill_with_rareness_features(features_dict, counter, w):
    """
    :param features_dict: features dictionary.
    :param counter: counter dictionary for words.
    :param w: word.
    """
    if is_rare(counter, w):
        features_dict['contains_hyphen'] = '-' in w
        features_dict['contains_number'] = any(char.isdigit() for char in w)
        features_dict['contains_uppercase'] = any(char == char.upper() for char in w)

        # prefixes and suffixes
        n = len(w)
        for j in range(n):
            if n > j:
                features_dict['prefix_' + str(j + 1)] = w[:j + 1]
                features_dict['suffix_' + str(j + 1)] = w[n - j - 1:]
    else:
        features_dict['form'] = w


def get_features_str(features_dict):
    """
    :param features_dict: features dictionary.
    :return: string that describe the features-dictionary,
             format - 'key0=val0 key1=val1 ... keyn=valn<end_line>'
    """
    feat_str = StringIO()
    features_dict_iter_items = features_dict.iteritems()

    # first element
    key0, val0 = next(features_dict_iter_items)
    feat_str.write(key0 + '=' + str(val0))

    for key, val in features_dict.iteritems():
        feat_str.write(' ' + key + '=' + str(val))

    return feat_str.getvalue()


if __name__ == '__main__':
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    lines = read_file(input_filename)
    words_counter = get_words_counter(lines)
    stream = StringIO()

    for line in lines:
        features = {}
        for i, (word, tag) in enumerate(line):
            fill_with_regular_features(features, line, i)
            fill_with_rareness_features(features, words_counter, word)

            stream.write(tag + ' ' + get_features_str(features) + '\n')

    # write output
    output_file = open(output_filename, 'w')
    output_file.write(stream.getvalue())
    output_file.close()