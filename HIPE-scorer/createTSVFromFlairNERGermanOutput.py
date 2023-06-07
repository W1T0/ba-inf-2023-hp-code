from flair.data import Sentence
from flair.models import SequenceTagger
import os

# load tagger
tagger = SequenceTagger.load("flair/ner-german-large")
print("[INFO] tagger loaded")

# path of the directory
directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/nergermantest/"

# path of the output file
writeFilename = "./NER-german/entities1.txt"

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
            "./HIPE-scorer/output-flair-ner-german/" + filename + ".tsv",
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
            # todo every word in a line?
            print("[INFO] lineSplit: " + str(lineSplit))
            if lineSplit:
                firstWord = lineSplit[0]

                predicate = "O"

                print(
                    "[INFO] firstWord: " + firstWord + "entity: " + entities[index][0]
                )
                if firstWord == entities[index][0]:
                    predicate = entities[0][1]
                    print(predicate)
                    index += 1

                writeToFile.write(
                    firstWord + "	" + predicate + "	O	O	O	O	O	_	_	_" + "\n"
                )

        writeToFile.close()

        print("[INFO] " + str(fileCount) + " FILES DONE")

        fileCount = fileCount + 1

        continue
    else:
        continue
