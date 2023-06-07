from flair.data import Sentence
from flair.models import SequenceTagger
import os

# load tagger
tagger = SequenceTagger.load("flair/ner-german-large")

# path of the directory
directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/Stichprobe - Annotationen/"

# path of the output file
writeFilename = "./NER-german/entities2.txt"

# the directory where the transcripts are stored
directory = os.fsencode(directoryPath)

# keeps track of how many files haven been processed
fileCount = 1

# for every file in the directory which ends with .txt
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        # open file
        readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

        # process file with flair NER
        sentence = Sentence(readFromFile.read())

        # predict NER tags
        tagger.predict(sentence)

        # open file to write entities to txt file
        writeToFile = open(writeFilename, "a", encoding="utf-8")
        writeToFile.write("--------------------------------- \n")
        writeToFile.write("FILENAME: " + filename + "\n")

        # print sentence and write to the txt file
        print("[INFO] SENTENCE:")
        print(sentence)
        print("-----------------------------")
        writeToFile.write(str(sentence) + "\n")

        # print predicted NER spans
        print("The following NER tags are found:")

        # iterate over entities and print
        for entity in sentence.get_spans("ner"):
            print(entity)
            writeToFile.write(str(entity) + "\n")

        print("-----------------------------")
        writeToFile.close()

        print("[INFO] ENTITIES WRITTEN")
        print("[INFO] " + str(fileCount) + " FILES DONE")

        fileCount = fileCount + 1

        continue
    else:
        continue
