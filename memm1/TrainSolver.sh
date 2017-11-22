#!/bin/bash
# build model from features vectors file
# input should be: feature_vecs_file output_model_file_name

java -cp liblinear.jar de.bwaldvogel.liblinear.Train -s 0 $1 $2
echo "Done!"
