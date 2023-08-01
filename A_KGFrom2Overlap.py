import os
import B_wikidataSPARQLQuery


# function that returns the coordinates of a location given the wikidata QID of that location
def getCoordinates(wikidataQID):
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
    data_extracter = B_wikidataSPARQLQuery.WikiDataQueryResults(query)
    queryDF = data_extracter.load_as_dataframe()

    # save latitude and longitude
    lat = str(queryDF.values[0, 0]).split(" ")[1].replace(")", "").replace(".", ",")
    long = str(queryDF.values[0, 0]).split(" ")[0].replace("Point(", "").replace(".", ",")

    # return latitude and longitude
    return "" + lat + "-" + long


directoryPath = "./FoodReligionEvaluation/output15/output-tsv-2overlap/"  # "./HIPE-scorer-input/output15/output-tsv-2overlap/"
outputPath = "./Visualization/output-kg/output-kg-2overlap-3-withReligionAndFood.txt"

# keeps track of how many files haven been processed
fileCount = 1

# open file to write entities to txt file
writeToFile = open(outputPath, "a", encoding="utf-8")

# write prefix
writeToFile.write("\nprefix ex: <http://example.org/>\nprefix xsd: <http://www.w3.org/2001/XMLSchema#>\n\n")
writeToFile.close()

# for every file in the directory which ends with .tsv
for file in os.listdir(directoryPath):
    filename = os.fsdecode(file)
    if filename.endswith(".tsv"):
        # stores the entities
        entitiesLine = []

        # open file
        readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

        # stores every line of file
        lines = readFromFile.readlines()

        # checks if a line ends with a specific string
        for line in lines[1:-1]:
            # split the line
            lineSplit = line.split()

            # get the entity type
            entityType = lineSplit[1]

            if entityType != "O":
                # print(line)
                entitiesLine.append(line)

        # remove duplicates
        entitiesLineDistinct = [*set(entitiesLine)]

        # open file to write entities to txt file
        writeToFile = open(outputPath, "a", encoding="utf-8")

        # removed unwanted info from filename
        filename = filename[:22]

        # header
        writeToFile.write("# --- ENTITIES OF " + filename + " ---\n")

        year = "1" + filename[1:4]
        month = filename[4:6]
        day = filename[6:8]

        # write year triple
        writeToFile.write(
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
            writeToFile.write(
                "ex:" + filename.replace(".", "") + " ex:" + entityType + " ex:" + entity + " .\n"
            )

            # write wikidata QID triple
            if wikidataQID != "_":
                writeToFile.write("ex:" + entity + " ex:" + "wikidataQID" + " ex:" + wikidataQID + " .\n")

            if coordinates != "-":
                writeToFile.write("ex:" + entity + " ex:" + "coordinates" + " ex:'" + coordinates + "' .\n")

        writeToFile.write("\n")
        writeToFile.close()

        print("[DEBUG] ENTITIES WRITTEN")
        print("[DEBUG] " + str(fileCount) + " FILES DONE")
        fileCount += 1
        continue
    else:
        continue
