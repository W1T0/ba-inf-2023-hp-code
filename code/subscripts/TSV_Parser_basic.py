import os
from subscripts import replace_special_characters


def run(directoryPath: str, outputPath: str, fileEnding: str, hipeFileAdd: str):
    """
    Creates a TSV-file for the annotations, the germaNER output and the sequence_tagging output
    in a format the HIPE-scorer accepts.

    directoryPath: The path of the directory where the files are stored in.
    outputPath: The path of the directory where the output should be stored in.
    fileEnding: The ending of the file (".conll" or ".txt").
    hipeFileAdd: An addition to the filename to conform with the HIPE-scorer format and identify the file.
    """

    # keeps track of how many files haven been processed
    fileCount = 1

    # for every file in the directory which ends with .conll
    for file in os.listdir(directoryPath):
        filename = os.fsdecode(file)
        if filename.endswith(fileEnding):
            # open file
            readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

            # stores every line of file
            lines = readFromFile.readlines()

            # create folder if it does not exist
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)

            # open file to write to tsv file
            # edit the filename to conform with the HIPE-scorer format
            writeToFile = open(
                outputPath + filename.replace(fileEnding, "").replace("_", "-") + hipeFileAdd + ".tsv",
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
                # split the lines
                lineSplit = line.split()

                # checks that there is a line and that the first line of sequence_tagging files are not read
                if lineSplit and not lineSplit[0].startswith("<"):
                    # save first word of line
                    firstWord = lineSplit[0]

                    # set the default predicate
                    predicate = "O"

                    # checks if line ends with an entity type
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
                        firstWordReplaced = replace_special_characters.replace(firstWord)

                        # write entity and entity type to file
                        writeToFile.write(firstWordReplaced + "	" + predicate + "	O	O	O	O	O	_	_	_" + "\n")

            writeToFile.close()

            print("[INFO] " + str(fileCount) + " FILES DONE (createTSVBasic)")
            fileCount += 1
            continue
        else:
            continue
