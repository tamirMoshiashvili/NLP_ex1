from FeatureIds import FeatureIds as FeatureIds
from liblin import LiblinearLogregPredictor as predictor
from StringIO import StringIO
import sys
START = '_START_'



class GreedyMaxEntTag:
    def __init__(self, model_file_name,feature_map_file ):
        self.feature_ids = FeatureIds(feature_map_file)
        self.predictor = predictor(model_file_name)

    def get_max_predict(self,word,pre_word, pre_pre_word, pre_label, pre_pre_label, next_word, next_next_word):
        vector = self.feature_ids.get_feature_vector(word,pre_word, pre_pre_word, pre_label,
                                                                   pre_pre_label, next_word, next_next_word)
        result = self.predictor.predict(sorted(vector))
        max_val = max(result.values())
        return result.keys()[result.values().index(max_val)]


    def tag_file(self,input_file_name, output_file_name):
        f = open(input_file_name, 'r')
        file_lines = f.read().splitlines()
        f.close()

        stream = StringIO()

        for line in file_lines:
            pre_tag = pre_pre_tag = START
            pre_word = pre_pre_word = ""
            words = line.split()
            words.append("")
            words.append("")

            for i in range(0,len(words)-3):
                tag = self.get_max_predict(words[i], pre_word, pre_pre_word, pre_tag, pre_pre_tag, words[i+1], words[i+2])
                pre_pre_tag = pre_tag
                pre_tag = tag
                pre_pre_word = pre_word
                pre_word = words[i]
                stream.write(words[i] + "/" + tag + " ")
            stream.write("\n")
        ot = open(output_file_name,"w")
        ot.write(stream.getvalue())
        ot.close()


# input_file_name , modelname, feature_map_file, out_file_name
if __name__ == '__main__':
    tagger = GreedyMaxEntTag(sys.argv[2],sys.argv[3])
    tagger.tag_file(sys.argv[1], sys.argv[4])

