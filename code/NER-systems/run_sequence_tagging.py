import os
import sys


# path to input and output
inputPath = "./kiefer-scholz_collection_tokenized/"
outputPath = "./output-sequence_tagging/"


for file in os.listdir(inputPath):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        # get the filename
        inputfile = inputPath + filename

        # create folder if it does not exist
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        # save console print out in file
        sys.stdout = open(outputPath + os.fsdecode(file), "w")

        # create command to execute
        cmd = (
            "python3 test.py model_transfer_learning_conll2003_germeval_emb_wiki/config "
            + inputfile
            + " > "
            + outputPath
            + os.fsdecode(file)
        )

        # execute command
        os.system(cmd)

        # close file
        sys.stdout.close()
