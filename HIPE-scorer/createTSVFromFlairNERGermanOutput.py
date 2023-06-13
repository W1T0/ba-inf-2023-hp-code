from flair.data import Sentence
from flair.models import SequenceTagger
import os
import re

# load tagger
tagger = SequenceTagger.load("flair/ner-german-large")
print("[INFO] tagger loaded")

# path of the directory
directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/Stichprobe - Annotationen/"  # Stichprobe - Annotationen

# the directory where the transcripts are stored
directory = os.fsencode(directoryPath)

# keeps track of how many files haven been processed
fileCount = 1

# to check if there has been an error
error = 0

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

        # save entities
        entities = []

        # iterate over entities, split them and print
        for entity in sentence.get_spans("ner"):
            print("-----------------------")
            print(str(entity))
            # get only the entites (is between '"' and '"')
            entityString = re.search('"(.*)"', str(entity)).group(1)

            # get the predicat (is between "→" and " ")
            predicate = re.search("→(.*) ", str(entity)).group(1).replace(" ", "")

            # check if there is a space in the entity string. If so, then that means more than one word is an entity and it needs to be split to fit the required format
            if " " in entityString:
                entityStringSplit = entityString.split()
                # iterate over every word and add it to the entities list
                for entitySplit in entityStringSplit:
                    entities.append([entitySplit, predicate])
                    print("-----------------------")
                    print("Entity: " + entitySplit)
                    print("Predicate: " + predicate)
            else:
                print("-----------------------")
                print("Entity: " + entityString)
                print("Predicate: " + predicate)
                entities.append([entityString, predicate])

        print("[INFO] entities list full, length: " + str(len(entities)))

        # open file (again, because otherwise there are errors)
        readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

        # read every line
        lines = readFromFile.readlines()
        print("[INFO] read lines")

        # open file to write into
        writeToFile = open(
            "./HIPE-scorer/output-tsv-flair-ner-german/"
            + filename.replace(".txt", "").replace("_", "-")
            + "-flairNERGerman"
            + "_bundle1_hipe2020_de_1"
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

        # keeps track of the number of entities added and the index of the entities list
        index = 0
        count = 0

        # write every word
        for line in lines:
            lineSplit = line.split()
            print("[INFO] lineSplit: " + str(lineSplit))
            if lineSplit:
                for word in lineSplit:
                    predicate = "O"

                    # checks if entites are present
                    if len(entities) > 0:
                        print(
                            "[INFO] firstWord: "
                            + word
                            + " || entity: "
                            + entities[index][0]
                        )

                        # check for every word if it is an entity
                        if word.replace("¬", "").replace(",", "").replace(
                            ".", ""
                        ) == entities[index][0].replace("¬", "").replace(
                            ",", ""
                        ).replace(
                            ".", ""
                        ):
                            predicate = "I-" + entities[index][1]
                            # increase index, if size of entities list is not already reached
                            if index != len(entities) - 1:
                                index += 1
                            count += 1
                            print(
                                "[INFO] "
                                + str(count)
                                + " / "
                                + str(len(entities))
                                + " DONE "
                            )

                    writeToFile.write(
                        word.replace(",", "").replace(".", "").replace("¬", "")
                        + "	"
                        + predicate
                        + "	O	O	O	O	O	_	_	_"
                        + "\n"
                    )

        if count == len(entities):
            print("[INFO] ALL ENTITIES MAPPED")
        else:
            error = 1

        writeToFile.close()

        print("[INFO] " + str(fileCount) + " FILES DONE")

        fileCount = fileCount + 1

        continue
    else:
        continue

if error == 1:
    print("[ERROR] Not all Entities have been mapped")
