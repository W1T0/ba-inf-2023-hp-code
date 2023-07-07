import os
import replaceSpecialCharacters


def run(directoryPath, outputDirectoryPath):
    # count the files
    count = 1

    # for every file in the directory which ends with .txt
    for file in os.listdir(directoryPath):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            # open file
            readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

            # read every line
            lines = readFromFile.readlines()

            # create folder if it does not exist
            if not os.path.exists(outputDirectoryPath):
                os.makedirs(outputDirectoryPath)

            # open file to write into
            writeToFile = open(
                outputDirectoryPath
                + filename.replace("_", "-")
                + "-germaNER"
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

            # for every line in lines
            for line in lines:
                # split lines
                lineSplit = line.split()

                if lineSplit:
                    # replace special characters
                    firstWord = replaceSpecialCharacters.replace(lineSplit[0])

                    # set default predicate
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

                    # checks that the firstWord is a valid word
                    # if firstWord != "O" and firstWord != "#" and firstWord != " ":
                    # write word
                    writeToFile.write(
                        firstWord + "	" + predicate + "	O	O	O	O	O	_	_	_" + "\n"
                    )

            writeToFile.close()
            print("[INFO] " + str(count) + " Files done")
            count += 1
