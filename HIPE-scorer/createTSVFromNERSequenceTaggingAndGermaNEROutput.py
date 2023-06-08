# the path to the file to read (usually a NER output file)
pathList = [
    "./NER-german/germaNER/germaNER-output.txt",
    "./NER-german/sequence_tagging/sequence_tagging-output2.txt",
]

# the output path
outputPathList = [
    "./HIPE-scorer/output-tsv-germaNER/",
    "./HIPE-scorer/output-tsv-sequence_tagging/",
]

additionalFilenameList = ["-germaNER", "-sequence_tagging"]

# decide between germaNER [0] and sequence_tagging [1]
whichOne = 1
path = pathList[whichOne]
outputPath = outputPathList[whichOne]
additionalFilename = additionalFilenameList[whichOne]

outputFilenames = [
    "L9xx12xx-TL2068_1b_pdf",
    "L9xx0527-TL2027_1a_pdf",
    "L9xxxxxx-TL0234_1b_pdf",
    "L9xxxxxx-TL2026_1b_pdf",
    "L9xxxxxx-TL2055_1a_pdf",
    "L9xxxxxx-TL2082_1a_pdf",
    "L9xxxxxx-TL2112_1b_pdf",
    "L921xx17-TL0283_2b_pdf",
    "L92309xx-TL1016_2b_pdf",
    "L9110213-TL0015_1a_pdf",
    "L9120323-TL0033_1a_pdf",
    "L9120903-TL0046_1a_pdf",
    "L9130421-TL0063_1b_pdf",
    "L9140528-TL0092_1b_pdf",
    "L9150629-TL0111_1a_pdf",
    "L9151117-TL0116_1b_pdf",
    "L9170131-TL0136_2a_pdf",
    "L9190421-TL0157_1a_pdf",
    "L9191208-TL0169_2a_pdf",
    "L9200320-TL0187_1b_pdf",
    "L9200422-TL0001_1a_pdf",
    "L9200626-TL0201_2a_pdf",
    "L9200910-TL0220_1b_pdf",
    "L9201110-TL0230_1a_pdf",
    "L9210103-TL0249_1a_pdf",
    "L9210529-TL0272_1b_pdf",
    "L9220904-TL0307_1b_pdf",
    "L9221214-TL0322_1a_pdf",
    "L9260206-TL1039_3b_pdf",
    "L9300925-TL0222_1a_pdf",
]


# opens the file and reads all lines
file = open(path, "r", encoding="utf-8")
lines = file.readlines()

# counts the number of letters
counter = 0
lastCounter = 0

# # remove double lines
# firstLine = lines[0]
# previousLine = lines[0]
# print(len(lines))
# for line in lines:
#     # print("line: " + line)
#     if not line == firstLine:
#         if line == previousLine:
#             lines.remove(previousLine)
#             print(line)
#             print(previousLine)
#         previousLine = line
#         # print("new previous line: " + previousLine)
# print(len(lines))

filename = ""

# write every word
for line in lines:
    if line.startswith("#"):
        filename = outputFilenames[counter]
        counter += 1
        # print("[INFO] " + str(counter) + " Files written")

    lineSplit = line.split()

    if lineSplit:
        firstWord = lineSplit[0]

        predicate = "O"
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
            predicate = lineSplit[-1]

        # open file to write to tsv file
        writeToFile = open(
            outputPath + filename + additionalFilename + ".tsv", "a", encoding="utf-8"
        )

        if lastCounter != counter:
            # write first line
            writeToFile.write(
                "TOKEN	NE-COARSE-LIT	NE-COARSE-METO	NE-FINE-LIT	NE-FINE-METO	NE-FINE-COMP	NE-NESTED	NEL-LIT	NEL-METO	MISC"
                + "\n"
            )
            lastCounter = counter

        if firstWord != "O" and firstWord != "#":
            # write word
            writeToFile.write(firstWord + "	" + predicate + "	O	O	O	O	O	_	_	_" + "\n")

        writeToFile.close()
