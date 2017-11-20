import sys
from StringIO import StringIO
from multiprocessing import Process
features_list = ['pr_w', 'pr_t', 'pr_pr_w', 'pr_2_t', 'nx_w', 'nx_nx_w', 'w', 'hyphen', 'num', 'upper',
                'pre_1','pre_2','pre_3','pre_4', 'suf_1', 'suf_2', 'suf_3', 'suf_4']

def add_to(value, some_list):
    if value not in some_list:
        some_list.append(value)


def index_in_list(value, some_list):
    return some_list.index(value)

def index_of_feature(value, feature_dict):
    name, tag = value.split("=",1)
    index_val = 0
    for key in feature_dict.keys():
        if key != name:
            index_val += len(feature_dict[key])-1
        else:
            index_val += index_in_list(tag, feature_dict[key])
            break
    return index_val


def map_feature_and_labels(feature_file):
    labels_list = set()
    feature_dict = {}
    for feat in features_list:
        feature_dict[feat] = []

    f = open(feature_file, 'r')
    for line in f:
        parts = line.split()
        labels_list.add(parts[0])
        for i_feature in parts[1:]:
            name, tag = i_feature.split('=', 1)
            add_to(tag, feature_dict[name])
    f.close()
    print ("a")
    return list(labels_list), feature_dict

from time import time
def write_feature_map(feature_map_file, label_list, feature_list):

    stream = StringIO()
    for i in range(0, len(label_list) - 1):
        stream.write(label_list[i] + " " + str(i) + "\t")
    stream.write('\n')

    for name in feature_list:
        for value in feature_list[name]:
            feature = name + "=" + value
            stream.write(feature + " " + str(index_of_feature(feature, feature_list)) + "\n")

    output_file = open(feature_map_file, "w")
    output_file.write(stream.getvalue())
    output_file.close()


if __name__ == '__main__':
    feature_vecs_file = sys.argv[2]
    last_time = time()
    label_list, features_dict = map_feature_and_labels(sys.argv[1])
    now = time()
    print("create lists: " + str( now - last_time))
    last_time = now

    p = Process(target=write_feature_map,args = (sys.argv[3], label_list, features_dict,))
    p.start()


    stream = StringIO()
    feature_file = open(sys.argv[1], 'r')
    for line in feature_file.readlines():
        parts = line.split()
        stream.write(str(index_in_list(parts[0], label_list)) + " ")
        f = []
        for feature in parts[1:]:
            try:
                f.append(index_of_feature(feature, features_dict))
            except:
                print feature

        map(lambda x: stream.write(str(x) + ":1 "), sorted(f))
        stream.write('\n')

    output_file = open(feature_vecs_file, "w")
    output_file.write(stream.getvalue())
    output_file.close()
    p.join()
    now = time()
    print("write vectors file + map file: " + str(now - last_time))
    last_time = now







