from FeatureIds import FeatureIds as FeatureIds
from liblin import LiblinearLogregPredictor as predictor
START = '_START_'



class GreedyMaxEntTag:
    def __init__(self, model_file_name,feature_map_file ):
        self.feature_ids = FeatureIds(feature_map_file)
        self.predictor = predictor(model_file_name)

    def get_max_predict(self,word,pre_word, pre_pre_word, pre_label, pre_pre_label, next_word, next_next_word):
        result = self.predictor.predict(self.feature_ids.get_feature_vector(word,pre_word, pre_pre_word, pre_label,
                                                                   pre_pre_label, next_word, next_next_word))
        max_val = max(result.values())
        return result.keys()[result.values().index(max_val)]


    def tag_file(self,input_file_name, output_file_name):
        f = open(input_file_name, 'r')
        file_lines = f.read().splitlines()
        f.close()

        for line in file_lines:
            pre_tag = pre_pre_tag = START
            words = line.split()

            for i in range(0,len(words)-1):
                # on it now...
                pass





