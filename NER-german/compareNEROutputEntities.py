import os

directories = [
    "./HIPE-scorer/output-tsv-flair-ner-german/",
    "./HIPE-scorer/output-tsv-germaNER/",
    "./HIPE-scorer/output-tsv-sequence_tagging/",
]

# [0]:flair-ner-german, [1]:germaNER, [2]:sequence_tagging
files = [[], [], []]
index = 0

# save every filename in a list
for directory in directories:
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        files[index].append(directory + filename)
    index += 1
print("[INFO] Files saved")

# check if there are the same number of files in every directory
if len(files[0]) == len(files[1]) == len(files[2]):
    # compare the entites TODO
    for i in range(30):
        # open files
        flairNERGermanFile = open(files[0][i], "r", encoding="utf-8")
        germaNERFile = open(files[1][i], "r", encoding="utf-8")
        sequenceTaggingFile = open(files[2][i], "r", encoding="utf-8")
        print("[INFO] Files opened")

        # stores every line of file
        flairNERGermanLines = flairNERGermanFile.readlines()
        germaNERLines = germaNERFile.readlines()
        sequenceTaggingLines = sequenceTaggingFile.readlines()

        # checks if all the files have the same number of lines
        if len(flairNERGermanLines) == len(germaNERLines) == len(sequenceTaggingLines):
            for j in range(len(flairNERGermanLines)):
                flairNERGermanLineSplit = flairNERGermanLines[j].split()
                germaNERLineSplit = germaNERLines[j].split()
                sequenceTaggingLineSplit = sequenceTaggingLines[j].split()

                # checks if there is a line for every file
                if (
                    flairNERGermanLineSplit
                    and germaNERLineSplit
                    and sequenceTaggingLineSplit
                ):
                    flairNERGermanLineSplitFirstWord = flairNERGermanLines[0]
                    germaNERLineSplitFirstWord = germaNERLines[0]
                    sequenceTaggingLineSplitFirstWord = sequenceTaggingLines[0]

                    # checks if the first word is the same
                    if (
                        flairNERGermanLineSplitFirstWord
                        == germaNERLineSplitFirstWord
                        == sequenceTaggingLineSplitFirstWord
                    ):
                        # get the entity (without B- or I- infront)
                        flairNERGermanLineSplitEntity = flairNERGermanLines[1].split(
                            "-"
                        )[1]
                        germaNERLineSplitEntity = germaNERLines[1].split("-")[1]
                        sequenceTaggingLineSplitEntity = sequenceTaggingLines[1].split(
                            "-"
                        )[1]

                        # checks if the entity (need better word) is the same
                        if (
                            flairNERGermanLineSplitEntity
                            == germaNERLineSplitEntity
                            == sequenceTaggingLineSplitEntity
                        ):
                            # write to file
                            print("----------------------------------------")
                            print("Word: " + flairNERGermanLineSplitFirstWord)
                            print("Entity: " + flairNERGermanLineSplitEntity)
                            print("----------------------------------------")
                        else:
                            print("################################")
                            print("[INFO] Not the same or no entity")
                            print("Word: " + flairNERGermanLineSplitFirstWord)
                            print("Entity flair-NER: " + flairNERGermanLineSplitEntity)
                            print("Entity germaNER: " + germaNERLineSplitEntity)
                            print(
                                "Entity sequence_tagging: "
                                + sequenceTaggingLineSplitEntity
                            )
                            print("################################")

                    else:
                        print("[ERROR] The first word is not the same.")
                else:
                    print("[ERROR] There is a missing line in one or multiple files.")
        else:
            print("[ERROR] The files do not have the same number of lines.")
else:
    print("[ERROR] There are not the same number of files in every directory.")
