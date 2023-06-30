import os
import sys



# path to directory
directory = "./TokenizedLetters/"

for file in os.listdir(directory):

    # get the filename
    inputfile = directory + os.fsdecode(file)

    # save console print out in file
    sys.stdout = open("./outputSequence_tagging/"+ os.fsdecode(file), "w")

    # create command to execute
    cmd = "python3 test.py model_transfer_learning_conll2003_germeval_emb_wiki/config " + inputfile + " > " + "./outputSequence_tagging/" + os.fsdecode(file)

    # execute command
    os.system(cmd)

    # close file
    sys.stdout.close()

