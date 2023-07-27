import os

directoryPath = "./HIPE-scorer-input/outputFW10/output-tsv-2overlap/"
outputPath = "./Visualization/output-kg-2overlap.txt"

# keeps track of how many files haven been processed
fileCount = 1

# open file to write entities to txt file
writeToFile = open(outputPath, "a", encoding="utf-8")

# write prefix
writeToFile.write("\nprefix ex: <http://example.org/>\n")
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

        # write entities
        writeToFile.write("# --- ENTITIES OF " + filename + " ---\n")
        for line in entitiesLineDistinct:
            # split the line
            lineSplit = line.split()

            # get the entity name
            entity = lineSplit[0]

            # get the entity type
            entityType = lineSplit[1]

            # get the wikidata QID
            wikidataQID = lineSplit[7]

            writeToFile.write(
                "ex:" + filename.replace(".", "") + " ex:" + entityType + " ex:" + entity + " .\n"
            )

            if wikidataQID != "_":
                writeToFile.write("ex:" + entity + " ex:" + "wikidataQID" + " ex:" + wikidataQID + " .\n")

        writeToFile.write("\n")
        writeToFile.close()

        print("[DEBUG] ENTITIES WRITTEN")
        print("[DEBUG] " + str(fileCount) + " FILES DONE")
        fileCount += 1
        continue
    else:
        continue
