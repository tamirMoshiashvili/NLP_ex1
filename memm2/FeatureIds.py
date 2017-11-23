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


class FeatureIds:
    def __init__(self, feature_map_file):
        self.feature_map = {}
        self.labels = {}
        self._map_file_to_dict(feature_map_file)

    def _map_file_to_dict(self, feature_map_file):
        lines = read_file(feature_map_file)
        for line in lines:
            key, value = line
            if not key.startswith("t=", 0, 2):
                self.feature_map[key] = value
            else:
                self.labels[value] = key.split("=", 1)[1]
        print "debug: labels is: " + str(self.labels)

    def _add_to(self, feature_list, feature):
        if feature.split("=", 1)[1] != "" and feature in self.feature_map:
            feature_list.append(int(self.feature_map[feature]))

    def get_feature_vector(self, word, pre_word, pre_pre_word, pre_label, pre_pre_label, next_word, next_next_word):
        feature_list = []
        if "w=" + word in self.feature_map:
            feature_list.append(int(self.feature_map["w=" + word]))
        else:
            self._add_to(feature_list, 'hyphen=' + str('-' in word))
            self._add_to(feature_list, 'num=' + str(any(char.isdigit() for char in word)))
            self._add_to(feature_list, 'upper=' + str(any(char == char.upper() for char in word)))

            # prefixes and suffixes
            n = len(word)
            for j in range(4):
                if n > j:
                    self._add_to(feature_list, 'pre_' + str(j + 1) + "=" + word[:j + 1])
                    self._add_to(feature_list, 'suf_' + str(j + 1) + "=" + word[n - j - 1:])

        self._add_to(feature_list, 'pr_w=' + pre_word)
        self._add_to(feature_list, 'pr_pr_w=' + pre_pre_word)
        self._add_to(feature_list, 'pr_t=' + pre_label)
        self._add_to(feature_list, 'pr_pr_t=' + pre_pre_label)

        self._add_to(feature_list, 'nx_w=' + next_word)
        self._add_to(feature_list, 'nx_nx_w=' + next_next_word)

        return feature_list
