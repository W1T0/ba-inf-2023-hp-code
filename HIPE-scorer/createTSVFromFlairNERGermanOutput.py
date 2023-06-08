from flair.data import Sentence
from flair.models import SequenceTagger
import os

# load tagger
tagger = SequenceTagger.load("flair/ner-german-large")
print("[INFO] tagger loaded")

# path of the directory
directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/nergermantest/"

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

        # process file with flair NER and predict NER tags
        sentence = Sentence(readFromFile.read())
        tagger.predict(sentence)
        print("[INFO] NER tags predicted")

        entities = []

        # iterate over entities and print
        for entity in sentence.get_spans("ner"):
            print("-----------------------")
            print(str(entity))
            entitySplit = str(entity).split()
            print("-----------------------")
            print("Entity: " + entitySplit[1].replace('"', ""))
            print("Predicate: " + entitySplit[3])
            entities.append([entitySplit[1].replace('"', ""), entitySplit[3]])

        print("[INFO] entities list full, length: " + str(len(entities)))

        # # write tsv
        # for file in os.listdir(directory):
        #     filename = os.fsdecode(file)
        #     if filename.endswith(".txt"):
        # open file
        readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

        # read every line
        lines = readFromFile.readlines()
        print("[INFO] read lines")

        # open file to write into
        writeToFile = open(
            "./HIPE-scorer/output-tsv-flair-ner-german/"
            + filename.replace(".txt", "")
            + "-flairNERGerman"
            + ".tsv",
            "a",
            encoding="utf-8",
        )
        print("[INFO] opened output file")

        # write first line
        writeToFile.write(
            "TOKEN	NE-COARSE-LIT	NE-COARSE-METO	NE-FINE-LIT	NE-FINE-METO	NE-FINE-COMP	NE-NESTED	NEL-LIT	NEL-METO	MISC"
            + "\n"
        )

        index = 0

        # write every word
        for line in lines:
            lineSplit = line.split()
            print("[INFO] lineSplit: " + str(lineSplit))
            if lineSplit:
                for word in lineSplit:
                    predicate = "O"

                    print(
                        "[INFO] firstWord: "
                        + word
                        + " || entity: "
                        + entities[index][0]
                    )

                    if word.replace("¬", "") == entities[index][0]:
                        predicate = "I-" + entities[index][1]
                        # print(predicate)
                        # print("len(entities): " + str(len(entities)))
                        # print("Index: " + str(index))
                        if index != len(entities) - 1:
                            index += 1

                    writeToFile.write(
                        word + "	" + predicate + "	O	O	O	O	O	_	_	_" + "\n"
                    )

        writeToFile.close()

        print("[INFO] " + str(fileCount) + " FILES DONE")

        fileCount = fileCount + 1

        continue
    else:
        continue
