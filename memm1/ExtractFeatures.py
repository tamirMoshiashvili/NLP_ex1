import sys
from StringIO import StringIO


def read_file(filename):
    """
    :return list of lines, each line is a list of (word, tag) tuples.
    """
    f = open(filename, 'r')
    file_lines = f.read().splitlines()
    f.close()

    for i, line in file_lines:
        line = line.split(' ')
        file_lines[i] = line
        for j, pair in enumerate(line):
            word, tag = pair.rsplit('/', 1)
            file_lines[i][j] = (word, tag)
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


def is_rare(counter, word):
    """
    Check if the given word is rare, according to the MEMM-paper.
    :return: boolean.
    """
    return counter[word] < 5


if __name__ == '__main__':
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    lines = read_file(input_filename)
    words_counter = get_words_counter(lines)
    stream = StringIO()
    for line in lines:
        for word, tag in line:
            # TODO: complete
    # write output
    output_file = open(output_filename, 'w')
    output_file.write(stream.getvalue())
    output_file.close()
