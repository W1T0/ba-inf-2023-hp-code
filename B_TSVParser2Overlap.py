import os
import B_get2OverlapEntitiesFromNEROutput
import B_queryRunner
import B_replaceSpecialCharacters
import B_wikidataSPARQLQuery


def run(
    directories,
    directoryPath,
    outputPath,
    outputPathFoodReligion,
):
    """
    Creates a TSV file for the 2 Overlap output in a format the HIPE-scorer accepts.

    directories: A list of the directories that store the output of the NER-systems.
    directoryPath: The path of the directory where the tokenized letters are stored in.
    outputPath: The path of the directory where the output should be stored in.
    outputPathFoodReligion: The path of the directory where the output for the food and religion evaluation should be stored in.
    """

    # generate 2 Overlap entities and save them
    entities2Overlap = B_get2OverlapEntitiesFromNEROutput.run(directories, boolWriteToFile=False)
    print(entities2Overlap)

    # extract entities from wikidata and save them
    wikidataEntites = B_queryRunner.run()
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

            # create folder if it does not exist
            if not os.path.exists(outputPathFoodReligion):
                os.makedirs(outputPathFoodReligion)

            # open file to write into for food and religion evaluation
            writeToFileFoodReligion = open(
                outputPathFoodReligion
                + filename.replace(".txt", "").replace("_", "-")
                + "-2Overlap"
                + "_food_and_religion_eval"
                + ".tsv",
                "a",
                encoding="utf-8",
            )

            # write first line
            writeToFile.write(
                "TOKEN	NE-COARSE-LIT	NE-COARSE-METO	NE-FINE-LIT	NE-FINE-METO	NE-FINE-COMP	NE-NESTED	NEL-LIT	NEL-METO	MISC"
                + "\n"
            )
            writeToFileFoodReligion.write("TOKEN	NE-COARSE-LIT	FOO-OR-RED	-	-	-	-	NEL-LIT	-	-" + "\n")

            # keeps track of the number of entities added
            count = 0

            # write every word
            for line in lines:
                lineSplit = line.split()
                # print("[INFO] lineSplit: " + str(lineSplit))
                if lineSplit:
                    # save first word of line
                    firstWord = lineSplit[0]

                    # set default entityType and Wikidata Q ID
                    entityType = "O"
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

                        # create a special entity type to later store food and religion entity types
                        specialEntityType = "O"

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
                                            # set the entityType, if word is an entity
                                            entityType = entity.split()[1]
                                            count += 1

                        # ignore the wikidata linking if entityType is B-PER
                        if not entityType == "B-PER":
                            # gets the wikidata link for a entity with a B-LOC entity type
                            # if entityType is B-LOC the food and religion query do not have to run, see else below
                            if entityType == "B-LOC":
                                # search for location with wikidata
                                query = (
                                    """
                                    SELECT ?item ?itemLabel WHERE {
                                        VALUES ?itemLabel { '"""
                                    + firstWordReplaced
                                    + """'@de }
                                        ?item rdfs:label|skos:altLabel ?itemLabel .
                                        {
                                            SELECT ?item WHERE {      
                                            { ?item wdt:P31 wd:Q6256 } # country
                                            UNION
                                            { ?item wdt:P31 wd:Q3624078} # sovereign state
                                            UNION
                                            { ?item wdt:P31 wd:Q15334 } # municipality of Poland
                                            UNION
                                            { ?item wdt:P31 wd:Q515 } # city
                                            UNION
                                            { ?item wdt:P31 wd:Q5119 } # capital city
                                            UNION
                                            { ?item wdt:P31 wd:Q1549591 } # big city
                                            UNION
                                            { ?item wdt:P31 wd:Q1093829 } # city in the United States         
                                            UNION
                                            { ?item wdt:P31 wd:Q15974307 } # administrative unit of Germany
                                            UNION
                                            { ?item wdt:P31 wd:Q42744322 } # urban municipality of Germany 
                                            UNION
                                            { ?item wdt:P31 wd:Q116457956 } # non-urban municipality in Germany
                                            UNION
                                            { ?item wdt:P31 wd:Q1221156 } # federated state of Germany
                                            UNION
                                            { ?item wdt:P31 wd:Q82794 } # geographic region
                                            UNION
                                            { ?item wdt:P31 wd:Q1620908 } # historical region
                                            }
                                        }
                                    }
                                """
                                )

                                # run query and save as dataframe
                                data_extracter = B_wikidataSPARQLQuery.WikiDataQueryResults(query)
                                queryDF = data_extracter.load_as_dataframe()

                                if not queryDF.empty:
                                    # iterate over labels in query result
                                    for label in queryDF.itemLabel:
                                        # get wikidata link and check if there are more than one link
                                        if queryDF.loc[(queryDF.itemLabel == label)].item.shape[0] > 1:
                                            # if there are more than one link, choose the first one
                                            wikidataQID = (
                                                (queryDF.loc[(queryDF.itemLabel == label)])
                                                .values[0, 0]
                                                .split("/")[-1]
                                            )
                                        else:
                                            # get QID from dataframe
                                            wikidataQID = (
                                                queryDF.loc[(queryDF.itemLabel == label)]
                                                .item.item()
                                                .split("/")[-1]
                                            )

                            # if entityType is B-LOC the food and religion query do not have to run
                            else:
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
                                                    and entityType != "B-PER"
                                                    and entityType != "I-PER"
                                                ):
                                                    entityType = "B-OTH"
                                                    wikidataQID = entity.split()[1].split("/")[-1]
                                                    # print("FOOD")
                                                    # print(firstWordReplaced, entity.split()[1])

                                                    specialEntityType = "FOOD"

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
                                                    and entityType != "B-PER"
                                                    and entityType != "I-PER"
                                                ):
                                                    entityType = "B-OTH"
                                                    wikidataQID = entity.split()[1].split("/")[-1]
                                                    # print("RELIGION")
                                                    # print(firstWordReplaced, entity.split()[1])

                                                    specialEntityType = "RELIGION"

                        if entityType != "O":
                            print(firstWordReplaced, entityType, wikidataQID)

                        # write entity and entityType to file
                        writeToFile.write(
                            firstWordReplaced + "	" + entityType + "	O	O	O	O	O	" + wikidataQID + "	_	_" + "\n"
                        )
                        writeToFileFoodReligion.write(
                            firstWordReplaced
                            + "	"
                            + entityType
                            + "	"
                            + specialEntityType
                            + "	O	O	O	O	"
                            + wikidataQID
                            + "	_	_"
                            + "\n"
                        )

            # check if all entities have been mapped
            if count < entitiesListLength:
                # if not, set error to 1 so that error message can be printed
                error = 1
                print("[ERROR]: " + str(count) + " " + str(entitiesListLength))
                print("[ERROR] NOT ALL ENTITIES MAPPED IN " + filename + " (TSV Parser 2 Overlap)")

            writeToFile.close()
            writeToFileFoodReligion.close()

            print("[INFO] " + str(fileCount) + " FILES DONE (TSV Parser 2 Overlap)")

            fileCount += 1

    # error message, if not all entites have been mapped
    if error == 1:
        print("[ERROR] NOT ALL ENTITIES HAVE BEEN MAPPED (TSV Parser 2 Overlap)")
