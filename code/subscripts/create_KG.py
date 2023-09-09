import os
from subscripts import wikidata_SPARQL_query


def getCoordinates(wikidataQID):
    """
    Returns the coordinates (latitude and longitude) of a location given the Wikidata QID

    wikidataQID: The Wikidata QID of the location.
    """

    query = (
        """
        SELECT ?geo WHERE {
            wd:"""
        + wikidataQID
        + """ wdt:P625 ?geo .
        }
        """
    )

    # run query and save as dataframe
    data_extracter = wikidata_SPARQL_query.WikiDataQueryResults(query)
    queryDF = data_extracter.load_as_dataframe()

    # save latitude and longitude
    lat = str(queryDF.values[0, 0]).split(" ")[1].replace(")", "").replace(".", ",")
    long = str(queryDF.values[0, 0]).split(" ")[0].replace("Point(", "").replace(".", ",")

    # return latitude and longitude
    return "" + lat + "-" + long


def run(inputPath: str, outputPathFull: str, outputPathSingle: str, debug: bool):
    """
    Creates a KG from the TSV 2 Overlap food and religin files.

    inputPath: The path where the TSV 2 Overlap food and religin files are stored.
    outputPath: The path where the final KG should be stored.

    """
    if debug:
        print("[DEBUG]#######################################################")
        print("[DEBUG] SCRIPT: A3_create_KG.py")

    # keeps track of how many files haven been processed
    fileCount = 1

    # open file to write entities to txt file
    writeToFileFull = open(outputPathFull, "a", encoding="utf-8")

    # write prefix
    writeToFileFull.write(
        "\nprefix ex: <http://example.org/>\nprefix xsd: <http://www.w3.org/2001/XMLSchema#>\n\n"
    )
    writeToFileFull.close()

    # for every file in the directory which ends with .tsv
    for file in os.listdir(inputPath):
        filename = os.fsdecode(file)
        if filename.endswith(".tsv"):
            # stores the entities
            entitiesLine = []

            # open file
            readFromFile = open(inputPath + filename, "r", encoding="utf-8")

            # stores every line of file
            lines = readFromFile.readlines()

            # checks if a line ends with a specific string
            for line in lines[1:-1]:
                # split the line
                lineSplit = line.split()

                # get the entity type
                entityType = lineSplit[1]

                if entityType != "O":
                    entitiesLine.append(line)

            # remove duplicates
            entitiesLineDistinct = [*set(entitiesLine)]

            # open file to write entities to txt file with the full KG
            writeToFileFull = open(outputPathFull, "a", encoding="utf-8")

            # removed unwanted info from filename
            filename = filename[:22]

            # open file to write entities to txt file with the single KGs
            writeToFileSingle = open(
                outputPathSingle + filename + ".txt",
                "a",
                encoding="utf-8",
            )

            # header
            writeToFileFull.write("# --- ENTITIES OF " + filename + " ---\n")

            year = "1" + filename[1:4]
            month = filename[4:6]
            day = filename[6:8]

            # write year triple
            writeToFileFull.write(
                "ex:"
                + filename.replace(".", "")
                + " ex:date '"
                + year
                + "-"
                + month
                + "-"
                + day
                + "'"
                + "^^xsd:date .\n"
            )

            writeToFileSingle.write(
                "ex:"
                + filename.replace(".", "")
                + " ex:date '"
                + year
                + "-"
                + month
                + "-"
                + day
                + "'"
                + "^^xsd:date .\n"
            )

            # write entities
            for line in entitiesLineDistinct:
                # split the line
                lineSplit = line.split()

                # get the entity name
                entity = lineSplit[0]

                # get the entity type
                entityType = lineSplit[1]

                # add religion or food string to entityType if entity is of that type
                if entityType == "B-OTH" and lineSplit[2] != "O":
                    entityType = entityType + "_" + lineSplit[2]

                # get the wikidata QID
                wikidataQID = lineSplit[7]

                # default value for coordinates to check if it has been set
                coordinates = "-"

                # get the coordinates for a location if there is a wikidataQID
                if entityType == "B-LOC" and wikidataQID != "_":
                    coordinates = getCoordinates(wikidataQID)

                # write entity triple
                writeToFileFull.write(
                    "ex:" + filename.replace(".", "") + " ex:" + entityType + " ex:" + entity + " .\n"
                )
                writeToFileSingle.write(
                    "ex:" + filename.replace(".", "") + " ex:" + entityType + " ex:" + entity + " .\n"
                )

                # write wikidata QID triple
                if wikidataQID != "_":
                    writeToFileFull.write(
                        "ex:" + entity + " ex:" + "wikidataQID" + " ex:" + wikidataQID + " .\n"
                    )
                    writeToFileSingle.write(
                        "ex:" + entity + " ex:" + "wikidataQID" + " ex:" + wikidataQID + " .\n"
                    )

                if coordinates != "-":
                    writeToFileFull.write(
                        "ex:" + entity + " ex:" + "coordinates" + " ex:'" + coordinates + "' .\n"
                    )
                    writeToFileSingle.write(
                        "ex:" + entity + " ex:" + "coordinates" + " ex:'" + coordinates + "' .\n"
                    )

            writeToFileFull.write("\n")
            writeToFileSingle.write("\n")
            writeToFileFull.close
            writeToFileSingle.close()

            print("[INFO] " + str(fileCount) + " FILES DONE (CREATE KG)")
            fileCount += 1
            continue
        else:
            continue
