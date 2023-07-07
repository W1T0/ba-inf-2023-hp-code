import os
import B_get2OverlapEntitiesFromNEROutput
import B_extractAllWithWikidata
import B_replaceSpecialCharacters


def run(
    directoriesList,
    directory="D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/test/",  # Stichprobe - Annotationen - Export
    output="./HIPE-scorer-output/",
):
    # generate 2 Overlap entities and save them
    entities2Overlap = B_get2OverlapEntitiesFromNEROutput.run(
        directoriesList, boolWriteToFile=False
    )
    print(entities2Overlap)

    # extract entities from wikidata and save them
    wikidataEntites = B_extractAllWithWikidata.run()
    religionEntities = wikidataEntites[0]
    foodEntities = wikidataEntites[1]

    print("------------------------ RELIGION ------------------------")
    print(religionEntities)
    print("------------------------ FOOD ------------------------")
    print(foodEntities)

    # path of the directory
    directoryPath = directory

    # output path
    outputPath = output

    # the directory where the files are stored
    directory = os.fsencode(directoryPath)

    # keeps track of how many files haven been processed
    fileCount = 1

    # to check if there has been an error
    error = 0

    # length of entities list
    entitiesListLength = 0

    # maybe relevant for later
    # filenamesFile2Overlap = []

    # # open file with 2Overlap entities and read every line
    # file2Overlap = open(
    #     "./NER-german/comparison2OverlapOutput2.txt", "r", encoding="utf-8"
    # )
    # file2OverlapLines = file2Overlap.readlines()

    # # save the filenames
    # for line in file2OverlapLines:
    #     if line.startswith("FILE"):
    #         filenamesFile2Overlap.append(line[49:71])

    # for every file in the directory which ends with .conll
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            # save the filename without .conll and with _ instead of - to conform with filenames from 2 Overlap
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

                    # ignore special characters
                    if (
                        firstWord != ","
                        and firstWord != "."
                        and firstWord != "¬"
                        and firstWord != "?"
                        and firstWord != ":"
                        and firstWord != ";"
                        and firstWord != "-"
                        and firstWord != " "
                        and firstWord != "	"
                    ):
                        # replace special characters
                        firstWordReplaced = B_replaceSpecialCharacters.replace(
                            firstWord
                        )

                        # print(firstWordReplaced)

                        # iterate over all 2-overlap-entities
                        for entities in entities2Overlap:
                            if len(entities) > 0:
                                # check if filename is the same
                                if entities[0] == filenameClean:
                                    # print("EQUAL FILENAME")
                                    # print(entities[0], filenameClean)

                                    entitiesListLength = len(entities[1:])

                                    # iterate over the entites only
                                    for entity in entities[1:]:
                                        # split entity and get the name
                                        entityName = entity.split()[0]

                                        # print(firstWord, entityName)

                                        # check for every word if it is an entity
                                        if firstWordReplaced == entityName:
                                            # set the predicate, if word is an entity
                                            predicate = entity.split()[1]
                                            count += 1

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
                                        if firstWordReplaced == entityName:
                                            predicate = "B-OTH"
                                            wikidataQID = entity.split()[1]
                                            # print("FOOD")
                                            # print(firstWordReplaced, entity.split()[1])

                        # # iterate over all location entities
                        # for locationEntity in locationEntities:
                        #     # check if there are entities in the list
                        #     if len(foodEntity) > 1:
                        #         # check if filename is the same
                        #         if locationEntity[0] == filenameClean:
                        #             for entity in locationEntity[1:]:
                        #                 # split entity and get the name
                        #                 entityName = entity.split()[0]

                        #                 # check for every word if it is an entity
                        #                 if firstWordReplaced == entityName:
                        #                     predicate = "B-LOC"
                        #                     wikidataQID = entity.split()[1]
                        #                     # print("LOCATION")
                        #                     # print(firstWordReplaced, entity.split()[1])

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
                                        if firstWordReplaced == entityName:
                                            predicate = "B-OTH"
                                            wikidataQID = entity.split()[1]
                                            # print("RELIGION")
                                            # print(firstWordReplaced, entity.split()[1])

                        if predicate != "O":
                            print(firstWordReplaced, predicate, wikidataQID)

                        # write entity and predicate to file
                        writeToFile.write(
                            firstWordReplaced
                            + "	"
                            + predicate
                            + "	O	O	O	O	O	"
                            + wikidataQID
                            + "	_	_"
                            + "\n"
                        )

            # check if all entities have been mapped
            if count >= entitiesListLength:
                print("[INFO] ALL ENTITIES MAPPED")
            else:
                # if not, set error to 1 so that error message can be printed
                error = 1
                print("[ERROR]: " + str(count) + " " + str(entitiesListLength))

            writeToFile.close()

            print("[INFO] " + str(fileCount) + " FILES DONE")
            fileCount = fileCount + 1

    # error message, if not all entites have been mapped
    if error == 1:
        print("[ERROR] Not all Entities have been mapped")
