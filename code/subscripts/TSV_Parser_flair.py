from flair.data import Sentence
from flair.models import SequenceTagger
import os
import re
from subscripts import replace_special_characters


def run(directoryPath, outputPath, debug):
    """
    Creates a TSV file for the flair/ner-german-large output in a format the HIPE-scorer accepts.

    directoryPath: The path of the directory where the files are stored in.
    outputPath: The path of the directory where the output should be stored in.
    debug: A boolean that enables debug prints if set to true.
    """

    # load sequence tagger
    tagger = SequenceTagger.load("flair/ner-german-large")
    print("[INFO] SequenceTagger loaded")

    # keeps track of how many files haven been processed
    fileCount = 1

    # variable to check if there has been an error
    error = 0

    # for every file in the directory which ends with .txt
    for file in os.listdir(directoryPath):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            # open file
            readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

            # process file with flair NER and predict NER tags
            sentence = Sentence(readFromFile.read())
            tagger.predict(sentence)

            if debug:
                print("[DEBUG] NER tags predicted")

            # save entities
            entities = []

            # iterate over entities, split them and print
            for entity in sentence.get_spans("ner"):
                # get only the entites (is between '"' and '"')
                entityString = re.search('"(.*)"', str(entity)).group(1)

                # get the predicate (is between "→" and " ")
                predicate = re.search("→(.*) ", str(entity)).group(1).replace(" ", "")

                # check if there is a space in the entity string.
                # If so, then that means more than one word is an entity and it needs to be split to fit the required format
                if " " in entityString:
                    entityStringSplit = entityString.split()

                    # iterate over every word and add it to the entities list
                    for entitySplit in entityStringSplit:
                        entities.append([entitySplit, predicate])

                else:
                    entities.append([entityString, predicate])

            if debug:
                print("[INFO] Entities list full, length: " + str(len(entities)))

            # open file (again, because otherwise there are errors)
            readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

            # read every line
            lines = readFromFile.readlines()

            # create folder if it does not exist
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)

            # open file to write into
            writeToFile = open(
                outputPath
                + filename.replace(".txt", "").replace("_", "-")
                + "-flairNERGerman"
                + "_bundle1_hipe2020_de_1"
                + ".tsv",
                "a",
                encoding="utf-8",
            )

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
                if lineSplit:
                    # for every word in the line split
                    for word in lineSplit:
                        # ignore special characters at the beginning
                        if (
                            word != ","
                            and word != "."
                            and word != "¬"
                            and word != "?"
                            and word != ":"
                            and word != ";"
                            and word != "-"
                            and word != "!"
                            and word != "("
                            and word != ")"
                            and word != "/"
                            and word != " "
                            and word != "	"
                        ):
                            # replace special characters
                            wordReplaced = replace_special_characters.replace(word)

                            # set default predicate
                            predicate = "O"

                            # checks if entites are present
                            if len(entities) > 0:
                                # replace special characters
                                entity = replace_special_characters.replace(entities[index][0])

                                # skips an entity if it is an emtpy string
                                if entity == " " or entity == "":
                                    print("[INFO] empty entity")
                                    index += 1
                                    count += 1
                                    entity = replace_special_characters.replace(entities[index][0])

                                if debug:
                                    print("[DEBUG] firstWord: " + wordReplaced + " || entity: " + entity)

                                # check for every word if it is an entity
                                if wordReplaced == entity:
                                    # set the predicate, if word is an entity
                                    predicate = "B-" + entities[index][1]

                                    # replace MISC entity types with OTH
                                    if predicate == "B-MISC":
                                        predicate = "B-OTH"

                                    # increase index, if size of entities list is not already reached
                                    if index != len(entities) - 1:
                                        index += 1

                                    # increase count to check later if all entities have been mapped
                                    count += 1

                                    if debug:
                                        print("[INFO] " + str(count) + " / " + str(len(entities)) + " DONE ")

                            # write entity and predicate to file
                            writeToFile.write(wordReplaced + "	" + predicate + "	O	O	O	O	O	_	_	_" + "\n")

            # check if all entities have been mapped
            if count != len(entities):
                # if not, set error to 1 so that error message can be printed
                error = 1
                print("[ERROR] NOT ALL ENTITIES MAPPED IN " + filename + " (TSV Parser Flair)")

            writeToFile.close()

            print("[INFO] " + str(fileCount) + " FILES DONE (TSV Parser Flair)")

            fileCount += 1

            continue
        else:
            continue

    # error message, if not all entites have been mapped
    if error == 1:
        print("[ERROR] NOT ALL ENTITIES HAVE BEEN MAPPED (TSV Parser Flair)")
