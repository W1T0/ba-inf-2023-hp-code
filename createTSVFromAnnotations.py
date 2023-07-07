import os
import replaceSpecialCharacters


def writeFirstWord(firstWord, line, lineSplit, writeToFile):
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
        # write entity and entity type to file
        writeToFile.write(
            replaceSpecialCharacters.replace(firstWord)
            + "	"
            + predicate
            + "	O	O	O	O	O	_	_	_"
            + "\n"
        )


def run(
    directory="D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/",
    output="./HIPE-scorer-output/output-tsv-annotations/",
):
    # path of the directory
    directoryPath = directory

    # output path
    outputPath = output

    # the directory where the files are stored
    directory = os.fsencode(directoryPath)

    # keeps track of how many files haven been processed
    fileCount = 1

    # for every file in the directory which ends with .conll
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".conll"):
            # open file
            readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

            # stores every line of file
            lines = readFromFile.readlines()

            # create folder if it does not exist
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)

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

            # # saves the previous line, if it is a number
            # previousLine = ""

            # write every word
            for line in lines:
                lineSplit = line.split()

                if lineSplit:
                    # save first word of line
                    firstWord = lineSplit[0]

                    writeFirstWord(firstWord, line, lineSplit, writeToFile)

                    # print("firstWord: " + firstWord)

                    # firstWordChanged = False

                    # # checks if the first word is numeric and the previous line has been set
                    # if firstWord.isnumeric() and previousLine != "":
                    #     # if so, add the previous line to the current first word
                    #     firstWord = firstWord + previousLine
                    #     previousLine = ""
                    #     firstWordChanged = True
                    #     print("previousLine + firstWord: " + firstWord)
                    # elif previousLine != "":
                    #     writeFirstWord(previousLine, line, lineSplit, writeToFile)
                    #     previousLine = ""

                    # # checks if the first word is number
                    # if firstWord.isnumeric() and not firstWordChanged:
                    #     # if so, save as previous line and add it to the next line
                    #     previousLine = firstWord
                    #     print("firstWord numeric: " + firstWord)
                    # else:
                    #     writeFirstWord(firstWord, line, lineSplit, writeToFile)

            writeToFile.close()

            print("[DEBUG] ENTITIES WRITTEN")
            print("[DEBUG] " + str(fileCount) + " FILES DONE")
            fileCount += 1
            continue
        else:
            continue
