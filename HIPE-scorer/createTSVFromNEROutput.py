# the path to the file to read (usually a NER output file)
# path = "./NER-german/germaNER/germaNER-output.txt"
path = "./NER-german/sequence_tagging/sequence_tagging-output2.txt"

# the output path
outputPath = "./HIPE-scorer/output-sequence_tagging/"
# outputPath = "./HIPE-scorer/output-germaNER/"

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

# write every word
for line in lines:
    if line.startswith("#"):
        counter += 1
        print("[INFO] " + str(counter) + " Files written")

    filename = "" + str(counter)

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
        writeToFile = open(outputPath + filename + ".tsv", "a", encoding="utf-8")

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
