#!/bin/bash
java -cp liblinear.jar de.bwaldvogel.liblinear.Train -s 0 -c 0.1 $1 $2
echo "Done!"
