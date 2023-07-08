import os
import B_get2OverlapEntitiesFromNEROutput
import B_extractAllWithWikidata
import B_replaceSpecialCharacters


def run(
    directories,
    directoryPath,
    outputPath,
):
    """
    Creates a TSV file for the 2 Overlap output in a format the HIPE-scorer accepts.

    directories: A list of the directories that store the output of the NER-systems.
    directoryPath: The path of the directory where the tokenized letters are stored in.
    outputPath: The path of the directory where the output should be stored in.
    """

    # generate 2 Overlap entities and save them
    entities2Overlap = B_get2OverlapEntitiesFromNEROutput.run(directories, boolWriteToFile=False)
    print(entities2Overlap)

    # extract entities from wikidata and save them
    wikidataEntites = B_extractAllWithWikidata.run()
    religionEntities = wikidataEntites[0]
    foodEntities = wikidataEntites[1]

    print("------------------------ RELIGION ------------------------")
    print(religionEntities)
    print("------------------------ FOOD ------------------------")
    print(foodEntities)

    # keeps track of how many files haven been processed
    fileCount = 1

    # to check if there has been an error
    error = 0

    # length of entities list
    entitiesListLength = 0

    # for every file in the directory which ends with .txt
    for file in os.listdir(directoryPath):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            # save the filename without .txt and with _ instead of - to conform with filenames from 2 Overlap
            filenameClean = filename.replace(".txt", "").replace("_", "-")

            print("--------------------------------------------------")
            print("[INFO] FILENAME: " + filenameClean)

            # open file
            readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

            # read every line
            lines = readFromFile.readlines()
            # print("[INFO] read lines")

            # create folder if it does not exist
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)

            # open file to write into
            writeToFile = open(
                outputPath
                + filename.replace(".txt", "").replace("_", "-")
                + "-2Overlap"
                + "_bundle1_hipe2020_de_1"
                + ".tsv",
                "a",
                encoding="utf-8",
            )
            # print("[INFO] opened output file")

            # write first line
            writeToFile.write(
                "TOKEN	NE-COARSE-LIT	NE-COARSE-METO	NE-FINE-LIT	NE-FINE-METO	NE-FINE-COMP	NE-NESTED	NEL-LIT	NEL-METO	MISC"
                + "\n"
            )

            # keeps track of the number of entities added
            count = 0

            # write every word
            for line in lines:
                lineSplit = line.split()
                # print("[INFO] lineSplit: " + str(lineSplit))
                if lineSplit:
                    # save first word of line
                    firstWord = lineSplit[0]

                    # set default predicate and Wikidata Q ID
                    predicate = "O"
                    wikidataQID = "_"

                    # ignore special characters at the beginning
                    if (
                        firstWord != ","
                        and firstWord != "."
                        and firstWord != "¬"
                        and firstWord != "?"
                        and firstWord != ":"
                        and firstWord != ";"
                        and firstWord != "-"
                        and firstWord != "!"
                        and firstWord != "("
                        and firstWord != ")"
                        and firstWord != "/"
                        and firstWord != " "
                        and firstWord != "	"
                    ):
                        # replace special characters
                        firstWordReplaced = B_replaceSpecialCharacters.replace(firstWord)

                        # print(firstWordReplaced)

                        # iterate over all 2-overlap-entities
                        for entities in entities2Overlap:
                            if len(entities) > 0:
                                # check if filename is the same
                                if entities[0] == filenameClean:
                                    # print("EQUAL FILENAME")
                                    # print(entities[0], filenameClean)

                                    entitiesListLength = len(entities[1:])

                                    # iterate over the entities only
                                    for entity in entities[1:]:
                                        # split entity and get the name
                                        entityName = entity.split()[0]

                                        # print(firstWord, entityName)

                                        # check for every word if it is an entity
                                        if firstWordReplaced == entityName:
                                            # set the predicate, if word is an entity
                                            predicate = entity.split()[1]
                                            count += 1

                        # gets the wikidata link for a entity with a B-LOC entity type
                        if predicate == "B-LOC":
                            # search for location with wikidata
                            y = 1

                        # iterate over all food entities
                        for foodEntity in foodEntities:
                            # check if there are entities in the list
                            if len(foodEntity) > 1:
                                # check if filename is the same
                                if foodEntity[0] == filenameClean:
                                    for entity in foodEntity[1:]:
                                        # split entity and get the name
                                        entityName = entity.split()[0]

                                        # check for every word if it is an entity
                                        # ignore PER entities
                                        if (
                                            firstWordReplaced == entityName
                                            and predicate != "B-PER"
                                            and predicate != "I-PER"
                                        ):
                                            predicate = "B-OTH"
                                            wikidataQID = entity.split()[1]
                                            # print("FOOD")
                                            # print(firstWordReplaced, entity.split()[1])

                        # iterate over all location entities
                        for religionEntity in religionEntities:
                            # check if there are entities in the list
                            if len(foodEntity) > 1:
                                # check if filename is the same
                                if religionEntity[0] == filenameClean:
                                    for entity in religionEntity[1:]:
                                        # split entity and get the name
                                        entityName = entity.split()[0]

                                        # check for every word if it is an entity
                                        # ignore PER entities
                                        if (
                                            firstWordReplaced == entityName
                                            and predicate != "B-PER"
                                            and predicate != "I-PER"
                                        ):
                                            predicate = "B-OTH"
                                            wikidataQID = entity.split()[1]
                                            # print("RELIGION")
                                            # print(firstWordReplaced, entity.split()[1])

                        if predicate != "O":
                            print(firstWordReplaced, predicate, wikidataQID)

                        # write entity and predicate to file
                        writeToFile.write(
                            firstWordReplaced + "	" + predicate + "	O	O	O	O	O	" + wikidataQID + "	_	_" + "\n"
                        )

            # check if all entities have been mapped
            if count < entitiesListLength:
                # if not, set error to 1 so that error message can be printed
                error = 1
                print("[ERROR]: " + str(count) + " " + str(entitiesListLength))
                print("[ERROR] NOT ALL ENTITIES MAPPED IN " + filename + " (TSV Parser 2 Overlap)")

            writeToFile.close()

            print("[INFO] " + str(fileCount) + " FILES DONE (TSV Parser 2 Overlap)")

            fileCount += 1

    # error message, if not all entites have been mapped
    if error == 1:
        print("[ERROR] NOT ALL ENTITIES HAVE BEEN MAPPED (TSV Parser 2 Overlap)")
