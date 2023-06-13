import os

directories = [
    "./HIPE-scorer/output-tsv-flair-ner-german/",
    "./HIPE-scorer/output-tsv-germaNER/",
    "./HIPE-scorer/output-tsv-sequence_tagging/",
]

# output path
outputPath = "./NER-german/comparisonOutput.txt"

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
    # compare the entites
    for i in range(30):
        # open files
        flairNERGermanFile = open(files[0][i], "r", encoding="utf-8")
        germaNERFile = open(files[1][i], "r", encoding="utf-8")
        sequenceTaggingFile = open(files[2][i], "r", encoding="utf-8")
        print("[INFO] Files opened")

        # open file to write to
        writeToFile = open(outputPath, "a", encoding="utf-8")
        writeToFile.write("FILE: " + files[0][i] + "\n")

        # stores every line of file
        flairNERGermanLines = flairNERGermanFile.readlines()
        germaNERLines = germaNERFile.readlines()
        sequenceTaggingLines = sequenceTaggingFile.readlines()

        # checks if all the files have the same number of lines
        if len(flairNERGermanLines) == len(germaNERLines) == len(sequenceTaggingLines):
            # split every line and compare them
            for j in range(len(flairNERGermanLines) - 1):
                flairNERGermanLineSplit = flairNERGermanLines[j + 1].split()
                germaNERLineSplit = germaNERLines[j + 1].split()
                sequenceTaggingLineSplit = sequenceTaggingLines[j + 1].split()

                # checks if there is a line for every file
                if (
                    flairNERGermanLineSplit
                    and germaNERLineSplit
                    and sequenceTaggingLineSplit
                ):
                    flairNERGermanLineSplitFirstWord = flairNERGermanLineSplit[0]
                    germaNERLineSplitFirstWord = germaNERLineSplit[0]
                    sequenceTaggingLineSplitFirstWord = sequenceTaggingLineSplit[0]

                    # checks if the first word is the same
                    if (
                        flairNERGermanLineSplitFirstWord
                        == germaNERLineSplitFirstWord
                        == sequenceTaggingLineSplitFirstWord
                    ):
                        # default values that won't appear
                        flairNERGermanLineSplitEntityType = "-1"
                        germaNERLineSplitEntityType = "-2"
                        sequenceTaggingLineSplitEntityType = "-3"

                        # checks that the entity tpye exist and get the entity type (without B- or I- infront)
                        if flairNERGermanLineSplit[1] != "O":
                            flairNERGermanLineSplitEntityType = flairNERGermanLineSplit[
                                1
                            ].split("-")[1]

                        if germaNERLineSplit[1] != "O":
                            germaNERLineSplitEntityType = germaNERLineSplit[1].split(
                                "-"
                            )[1]
                        if sequenceTaggingLineSplit[1] != "O":
                            sequenceTaggingLineSplitEntityType = (
                                sequenceTaggingLineSplit[1].split("-")[1]
                            )

                        # checks if the entity type is the same for two
                        if (
                            flairNERGermanLineSplitEntityType
                            == germaNERLineSplitEntityType
                            or flairNERGermanLineSplitEntityType
                            == sequenceTaggingLineSplitEntityType
                        ):
                            # write to file
                            # print("----------------------------------------")
                            # print("Word: " + flairNERGermanLineSplitFirstWord)
                            # print(
                            #     "Entity type: "
                            #     + flairNERGermanLineSplitEntityType
                            #     + sequenceTaggingLineSplitEntityType
                            #     + germaNERLineSplitEntityType
                            # )
                            # print("----------------------------------------")
                            # writeToFile.write(
                            #     "----------------------------------------\n"
                            # )
                            writeToFile.write(
                                flairNERGermanLineSplitFirstWord
                                + " "
                                + flairNERGermanLineSplitEntityType
                                + "\n"
                            )
                        elif (
                            germaNERLineSplitEntityType
                            == sequenceTaggingLineSplitEntityType
                        ):
                            writeToFile.write(
                                flairNERGermanLineSplitFirstWord
                                + " "
                                + germaNERLineSplitEntityType
                                + "\n"
                            )
                            # print("----------------------------------------")
                            # print("Word: " + flairNERGermanLineSplitFirstWord)
                            # print(
                            #     "Entity type: "
                            #     + germaNERLineSplitEntityType
                            #     + sequenceTaggingLineSplitEntityType
                            #     + germaNERLineSplitEntityType
                            # )
                        # else:
                        # print("################################")
                        # print("[INFO] Not the same or no entity")
                        # print("Word: " + flairNERGermanLineSplitFirstWord)
                        # print(
                        #     "Entity type flair-NER: "
                        #     + flairNERGermanLineSplitEntityType
                        # )
                        # print(
                        #     "Entity type germaNER: " + germaNERLineSplitEntityType
                        # )
                        # print(
                        #     "Entity type sequence_tagging: "
                        #     + sequenceTaggingLineSplitEntityType
                        # )
                        # print("################################")

                    else:
                        print("[ERROR] The first word is not the same.")
                        print(
                            "[ERROR]: flairNERGermanFile: "
                            + files[0][i]
                            + " | germaNERFile: "
                            + files[1][i]
                            + " | sequenceTaggingFile: "
                            + files[2][i]
                        )
                        print(
                            "[ERROR]: "
                            + flairNERGermanLineSplitFirstWord
                            + " "
                            + germaNERLineSplitFirstWord
                            + " "
                            + sequenceTaggingLineSplitFirstWord
                        )
                else:
                    print("[ERROR] There is a missing line in one or multiple files.")
                    print(
                        "[ERROR]: flairNERGermanFile: "
                        + files[0][i]
                        + " | germaNERFile: "
                        + files[1][i]
                        + " | sequenceTaggingFile: "
                        + files[2][i]
                    )
        else:
            print("[ERROR] The files do not have the same number of lines.")
            print(
                "[ERROR]: flairNERGermanFile: "
                + files[0][i]
                + " | germaNERFile: "
                + files[1][i]
                + " | sequenceTaggingFile: "
                + files[2][i]
            )
            print(
                "[ERROR]: "
                + str(len(flairNERGermanLines))
                + " "
                + str(len(germaNERLines))
                + " "
                + str(len(sequenceTaggingLines))
            )

        writeToFile.close()
else:
    print("[ERROR] There are not the same number of files in every directory.")
