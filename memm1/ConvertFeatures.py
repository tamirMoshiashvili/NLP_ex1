import sys
from StringIO import StringIO


def index_in(value, some_list):
    # (str,list)->int
    if value not in some_list:
        some_list.append(value)
    return some_list.index(value)


def map_feature_and_labels(feature_file):
    label_list = []
    feature_list = []
    f = open(feature_file, 'r')
    file_lines = f.read().splitlines()
    f.close()
    for line in file_lines:
        parts = line.split()
        index_in(parts[0], label_list)
        for feature in parts[1:]:
            index_in(feature, feature_list)

    return label_list, sorted(feature_list)

from time import time
def write_feature_map(feature_map_file, label_list, feature_list):

    stream = StringIO()
    for i in range(0, len(label_list) - 1):
        stream.write(label_list[i] + " " + str(i) + "\t")
    stream.write('\n')
    for i in range(0, len(feature_list) - 1):
        stream.write(feature_list[i] + " " + str(i) + "\n")

    output_file = open(feature_map_file, "w")
    output_file.write(stream.getvalue())
    output_file.close()


if __name__ == '__main__':
    feature_vecs_file = sys.argv[2]
    last_time = time()
    label_list, feature_list = map_feature_and_labels(sys.argv[1])
    now = time()
    print("create lists: "+ str(last_time - now))
    last_time = now

    write_feature_map(sys.argv[3], label_list, feature_list)
    now = time()
    print("write lists to map file: " + str(last_time - now))
    last_time = now

    stream = StringIO()
    f = open(sys.argv[1], 'r')
    file_lines = f.read().splitlines()
    f.close()

    for line in file_lines:
        parts = line.split()
        stream.write(str(index_in(parts[0], label_list)) + " ")
        f = []
        for feature in parts[1:]:
            f.append(index_in(feature, feature_list))
        map(lambda x: stream.write(x + ":1 "), sorted(f))
        stream.write('\n')

    output_file = open(feature_vecs_file, "w")
    output_file.write(stream.getvalue())
    output_file.close()

    now = time()
    print("write vectors file: " + str(last_time - now))
    last_time = now







