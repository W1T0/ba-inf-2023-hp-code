import os
from subscripts import get_2overlap_entities_from_NER_output
from subscripts import query_runner
from subscripts import replace_special_characters
from subscripts import wikidata_SPARQL_query


def run(
    directoriesNERoutput: list,
    inputTokenizedPath: str,
    outputPath: str,
    outputPathFoodReligion: str,
    filenameTSV: str,
    outputPathTXT: str,
    boolWriteToFile: bool,
    inputPathQuery: str,
    similarityMeasureFoodQuery: int,
    similarityMeasureReligionQuery: int,
    outputPathFoodQuery: str,
    outputPathReligionQuery: str,
    boolWriteToFileQuery: bool,
    debug: bool,
):
    """
    Creates a TSV file for the 2 Overlap output in a format the HIPE-scorer accepts.

    directoriesNERoutput: A list of the directories that store the output of the NER-systems.
    inputTokenizedPath: The path of the directory where the tokenized letters are stored in.
    outputPath: The path of the directory where the output should be stored in.
    outputPathFoodReligion: The path of the directory where the output for the food and religion evaluation should be stored in.
    filenameTSV: The ending the final TSV file has.
    outputPathTXT: The path of the file where the output, in this case only the 2Overlap entities, should be stored in.
    boolWriteToFile: A boolean value that determines if the result of this function should be written to the output file. (True or False)
    inputPathQuery: The path of the directory where the files are stored in for the query runner.
    similarityMeasure(-Food,-Religion)Query: The similarity measure. A metric to compare the differences between two strings based on the Levenshtein difference.
    outputPath(-Food,-Religion)Query: The path of the file where the output should be stored in for the query runner.
    boolWriteToFileQuery: A boolean value that determines if the result of this function should be written to the output file. (True or False)
    debug:  A boolean that enables debug prints if set to true.
    """
    # names of the kiefer scholz family
    kieferScholzNames = [
        "Anna",
        "Ernst",
        "Franz",
        "Maria",
        "Hedwig",
        "Josef",
        "Bertha",
        "Frank",
        "Rosalia",
        "Paul",
        "Martha",
        "Thekla",
        "Robert",
        "August",
        "Selma",
        "Agnes",
        "Berthold",
        "Cecilia",
        "Richard",
        "Marjorie",
        "Rita",
        "Helen",
        "Art",
        "Liesbeth",
        "Lene",
        "Erwin",
        "Grete",
        "Johanna",
        "Johann",
        "Ottilie",
        "Tielchen",
        "Walter",
        "Dolores",
    ]

    # generate 2 Overlap entities and save them
    entities2Overlap = get_2overlap_entities_from_NER_output.run(
        directoriesNERoutput, outputPathTXT, boolWriteToFile, debug
    )
    if debug:
        print("[DEBUG]------------------------ 2 OVERLAP ENTITIES ------------------------")
        print(entities2Overlap)
        print("[DEBUG]------------------------------------------------")
    print("[INFO] 2 OVERLAP ENTITIES GENERATED")

    # extract entities from wikidata and save them
    wikidataEntites = query_runner.run(
        inputPathQuery,
        similarityMeasureFoodQuery,
        similarityMeasureReligionQuery,
        outputPathFoodQuery,
        outputPathReligionQuery,
        boolWriteToFileQuery,
        debug,
    )
    religionEntities = wikidataEntites[0]
    foodEntities = wikidataEntites[1]

    if debug:
        print("[DEBUG]------------------------ RELIGION ENTITIES ------------------------")
        print(religionEntities)
        print("[DEBUG]------------------------------------------------")
        print("[DEBUG]------------------------ FOOD ENTITIES ------------------------")
        print(foodEntities)
        print("[DEBUG]------------------------------------------------")

    # keeps track of how many files haven been processed
    fileCount = 1

    # to check if there has been an error
    error = 0

    # length of entities list
    entitiesListLength = 0

    # for every file in the directory which ends with .txt
    for file in os.listdir(inputTokenizedPath):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            # save the filename without .txt and with _ instead of - to conform with filenames from 2 Overlap
            filenameClean = filename.replace(".txt", "").replace("_", "-")

            if debug:
                print("[DEBUG]--------------------------------------------------")
                print("[DEBUG] FILENAME: " + filenameClean)

            # open file
            readFromFile = open(inputTokenizedPath + filename, "r", encoding="utf-8")

            # read every line
            lines = readFromFile.readlines()

            # create folder if it does not exist
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)

            # open file to write into
            writeToFile = open(
                outputPath + filename.replace(".txt", "").replace("_", "-") + filenameTSV + ".tsv",
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
                + "-2overlap"
                + "_food_and_religion"
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
                        firstWordReplaced = replace_special_characters.replace(firstWord)

                        # create a special entity type to later store food and religion entity types
                        specialEntityType = "O"

                        # iterate over all 2-overlap-entities
                        for entities in entities2Overlap:
                            if len(entities) > 0:
                                # check if filename is the same
                                if entities[0] == filenameClean:
                                    entitiesListLength = len(entities[1:])

                                    # iterate over the entities only
                                    for entity in entities[1:]:
                                        # split entity and get the name
                                        entityName = entity.split()[0]

                                        # check for every word if it is an entity
                                        if firstWordReplaced == entityName:
                                            # set the entityType, if word is an entity
                                            entityType = entity.split()[1]
                                            count += 1

                        # checks if word is a name of the kiefer scholz family
                        if firstWordReplaced in kieferScholzNames:
                            #  sets entity type to B-PER if not already
                            if entityType != "B-PER":
                                entityType = "B-PER"

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
                                data_extracter = wikidata_SPARQL_query.WikiDataQueryResults(query)
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
                                                    specialEntityType = "RELIGION"

                        if entityType != "O" and debug:
                            print("[DEBUG] " + firstWordReplaced + " | " + entityType + " | " + wikidataQID)

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
                print("[ERROR] NOT ALL ENTITIES MAPPED IN " + filename + " (TSV PARSER 2 Overlap)")

            writeToFile.close()
            writeToFileFoodReligion.close()

            print("[INFO] " + str(fileCount) + " FILES DONE (TSV PARSER 2 Overlap)")

            fileCount += 1

    # error message, if not all entites have been mapped
    if error == 1:
        print("[ERROR] NOT ALL ENTITIES HAVE BEEN MAPPED (TSV PARSER 2 Overlap)")
    else:
        print("[INFO] FINISHED WITHOUT ERRORS (TSV PARSER 2 Overlap)")
