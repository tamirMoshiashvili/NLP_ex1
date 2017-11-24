import sys
from StringIO import StringIO
from time import time


def read_file(filename):
    """
    :param filename: features filename.
    :return: list of lines, each line is a list of strings.
    """
    f = open(filename, 'r')
    file_lines = f.read().splitlines()
    f.close()

    for i, line in enumerate(file_lines):
        file_lines[i] = line.split(' ')
    return file_lines


def add_to_dict(d, key, val):
    """
    Add the given (key, val) if key is new to the dictionary.
    :param d: dictionary.
    :param key: string.
    :param val: id value, val >= 0
    :return: the next available id.
    """
    if key not in d:
        d[key] = val
        val += 1
    return val


def get_feature_to_id_dict(file_lines):
    """
    :param file_lines: list of lines, each line is a list of strings.
    :return: dictionary that maps feature-string to its id.
    """
    feature_to_id_dict = dict()
    i = 0

    # give tags the first id from zero
    for line in file_lines:
        tag = line[0]
        if tag not in feature_to_id_dict:
            i = add_to_dict(feature_to_id_dict, "t=" + tag, i)
    i = 1
    # give id to other features
    for line in file_lines:
        for feature in line:
            i = add_to_dict(feature_to_id_dict, feature, i)

    return feature_to_id_dict


def write_vecs_file(vecs_filename, feature_to_id_dict, file_lines):
    """
    Write the file with the given features mapped to their ids.
    """
    stream = StringIO()

    for line in file_lines:
        line_iter = iter(line)

        # get the tag
        tag = next(line_iter)
        stream.write(str(feature_to_id_dict["t=" + tag]))

        # get the other features and sort them
        sorted_list = list()
        for feature in line_iter:
            sorted_list.append(feature_to_id_dict[feature])
        sorted_list.sort()

        for feature_id in sorted_list:
            stream.write(' ' + str(feature_id) + ':1')
        stream.write('\n')

    vecs_file = open(vecs_filename, 'w')
    vecs_file.write(stream.getvalue())
    vecs_file.close()


def write_map_file(filename, feature_to_id_dict):
    stream = StringIO()

    for feature in feature_to_id_dict:
        stream.write(feature + ' ' + str(feature_to_id_dict[feature]) + '\n')

    f = open(filename, 'w')
    f.write(stream.getvalue())
    f.close()


# args: features_file feature_vecs_file feature_map_file
if __name__ == '__main__':
    t = time()

    feature_filename = sys.argv[1]
    feature_vecs_filename = sys.argv[2]
    feature_map_filename = sys.argv[3]

    lines = read_file(feature_filename)
    feature_to_id = get_feature_to_id_dict(lines)

    write_vecs_file(feature_vecs_filename, feature_to_id, lines)
    write_map_file(feature_map_filename, feature_to_id)

    print time() - t
