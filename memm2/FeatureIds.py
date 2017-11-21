
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
        self._map_file_to_dict(feature_map_file)

    def _map_file_to_dict(self, feature_map_file):
        lines = read_file(feature_map_file)
        for line in lines:
            key, value = line.rsplit(" ", 1)
            self.feature_map[key] = value

    def _add_to(self, feature_list, feature):
        if feature in self.feature_map:
            feature_list.append(self.feature_map[feature])

    def get_feature_vector(self, word,pre_word, pre_pre_word, pre_label, pre_pre_label, next_word, next_next_word):
        feature_list = []
        if "w="+word in self.feature_map:
            feature_list.append(str(self.feature_map["w="+word]) + ":1")
        else:
            feature_list.append(self.feature_map['hyphen='+str('-' in word)])
            feature_list.append(self.feature_map['num=' + str(any(char.isdigit() for char in word))])
            feature_list.append(self.feature_map['upper=' + str( any(char == char.upper() for char in word))])

            # prefixes and suffixes
            n = len(word)
            for j in range(4):
                if n > j:
                    try:
                        feature_list.append(self.feature_map['pre_' + str(j + 1) + "=" + word[:j + 1]])
                    except:
                        pass
                    try:
                        feature_list.append(self.feature_map['suf_' + str(j + 1) + "=" +  word[n - j - 1:]])
                    except:
                        pass
        self._add_to(feature_list,'pr_w=' + pre_word)
        self._add_to(feature_list,'pr_pr_w=' + pre_pre_word)
        self._add_to(feature_list,'pr_t=' + pre_label)
        self._add_to(feature_list,'pr_pr_t=' + pre_pre_label)

        if next_word:
            self._add_to(feature_list,'nx_w='+next_word )
        if next_next_word:
            self._add_to('nx_nx_w=' + next_next_word)

        vector_str = ''
        map(lambda x: vector_str + x + ":1 " ,sorted(feature_list))
        vector_str += "\n"
        return vector_str



