import os

directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/"  # Stichprobe - Annotationen - Export
outputPath = "./HIPE-scorer/output-tsv-annotations/"

# the directory where the files are stored
directory = os.fsencode(directoryPath)

# keeps track of how many files haven been processed
fileCount = 1

# for every file in the directory which ends with .conll
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".conll"):
        # stores the entities
        entities = []

        # open file
        readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

        # stores every line of file
        lines = readFromFile.readlines()

        # open file to write to tsv file
        writeToFile = open(
            outputPath
            + filename.replace(".conll", "").replace("_", "-")
            + "-annotations"
            ".tsv",
            "a",
            encoding="utf-8",
        )

        # write first line
        writeToFile.write(
            "TOKEN	NE-COARSE-LIT	NE-COARSE-METO	NE-FINE-LIT	NE-FINE-METO	NE-FINE-COMP	NE-NESTED	NEL-LIT	NEL-METO	MISC"
            + "\n"
        )

        # write every word
        for line in lines:
            lineSplit = line.split()

            if lineSplit:
                # save first word of line
                firstWord = lineSplit[0]

                # set the default predicate
                predicate = "O"

                # checks if line ends with entity type
                if (
                    line.endswith("I-PER\n")
                    or line.endswith("B-PER\n")
                    or line.endswith("I-LOC\n")
                    or line.endswith("B-LOC\n")
                    or line.endswith("I-OTH\n")
                    or line.endswith("B-OTH\n")
                    or line.endswith("I-ORG\n")
                    or line.endswith("B-ORG\n")
                ):
                    # if so, get the entity type
                    predicate = lineSplit[-1]

                # ignore special characters
                if firstWord != "," and firstWord != "." and firstWord != "¬":
                    # write entity and entity type to file
                    writeToFile.write(
                        firstWord + "	" + predicate + "	O	O	O	O	O	_	_	_" + "\n"
                    )

        writeToFile.close()

        print("[DEBUG] ENTITIES WRITTEN")
        print("[DEBUG] " + str(fileCount) + " FILES DONE")
        fileCount += 1
        continue
    else:
        continue
