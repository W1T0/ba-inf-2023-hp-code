import os


def run(boolWriteToFile=True):
    directories = [
        "./HIPE-scorer/output-tsv-flair-ner-german2/",
        "./HIPE-scorer/output-tsv-germaNER2/",
        "./HIPE-scorer/output-tsv-sequence_tagging2/",
    ]

    # output path
    outputPath = "./NER-german/comparisonOutput2.txt"

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

    # list to save filename and entities to
    entities2Overlap = []

    # check if there are the same number of files in every directory
    if len(files[0]) == len(files[1]) == len(files[2]):
        # compare the entites
        for i in range(30):
            # open files
            flairNERGermanFile = open(files[0][i], "r", encoding="utf-8")
            germaNERFile = open(files[1][i], "r", encoding="utf-8")
            sequenceTaggingFile = open(files[2][i], "r", encoding="utf-8")
            print("[INFO] Files opened")

            # append file name to entites2Overlap list
            entities2Overlap.append([files[0][i][43:65]])

            if boolWriteToFile:
                # open file to write to
                writeToFile = open(outputPath, "a", encoding="utf-8")
                writeToFile.write("FILE: " + files[0][i] + "\n")

            # stores every line of file
            flairNERGermanLines = flairNERGermanFile.readlines()
            germaNERLines = germaNERFile.readlines()
            sequenceTaggingLines = sequenceTaggingFile.readlines()

            # checks if all the files have the same number of lines
            if (
                len(flairNERGermanLines)
                == len(germaNERLines)
                == len(sequenceTaggingLines)
            ):
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
                            flairNERGermanLineSplitEntityTypeCleaned = "-1"
                            germaNERLineSplitEntityTypeCleaned = "-2"
                            sequenceTaggingLineSplitEntityTypeCleaned = "-3"

                            # checks that the entity tpye exist and get the entity type without B- or I- infront (cleaned) and with B- or I- infront
                            if flairNERGermanLineSplit[1] != "O":
                                flairNERGermanLineSplitEntityTypeCleaned = (
                                    flairNERGermanLineSplit[1].split("-")[1]
                                )
                                flairNERGermanLineSplitEntityType = (
                                    flairNERGermanLineSplit[1]
                                )

                            if germaNERLineSplit[1] != "O":
                                germaNERLineSplitEntityTypeCleaned = germaNERLineSplit[
                                    1
                                ].split("-")[1]
                                germaNERLineSplitEntityType = germaNERLineSplit[1]
                            if sequenceTaggingLineSplit[1] != "O":
                                sequenceTaggingLineSplitEntityTypeCleaned = (
                                    sequenceTaggingLineSplit[1].split("-")[1]
                                )
                                sequenceTaggingLineSplitEntityType = (
                                    sequenceTaggingLineSplit[1]
                                )

                            # checks if the entity type is the same for two
                            # checks only if the cleaned type is the same, because flair does not offer B- or I-
                            # if they are the same, it takes the "uncleaned" entity type of germanNER or sequence_tagging
                            if (
                                flairNERGermanLineSplitEntityTypeCleaned
                                == germaNERLineSplitEntityTypeCleaned
                            ):
                                if boolWriteToFile:
                                    writeToFile.write(
                                        flairNERGermanLineSplitFirstWord
                                        + " "
                                        + germaNERLineSplitEntityType
                                        + "\n"
                                    )

                                # add entities to entities2Overlap list
                                entities2Overlap[i].append(
                                    flairNERGermanLineSplitFirstWord
                                    + " "
                                    + germaNERLineSplitEntityType
                                )

                            elif (
                                flairNERGermanLineSplitEntityTypeCleaned
                                == sequenceTaggingLineSplitEntityTypeCleaned
                            ):
                                if boolWriteToFile:
                                    writeToFile.write(
                                        flairNERGermanLineSplitFirstWord
                                        + " "
                                        + sequenceTaggingLineSplitEntityType
                                        + "\n"
                                    )

                                # add entities to entities2Overlap list
                                entities2Overlap[i].append(
                                    flairNERGermanLineSplitFirstWord
                                    + " "
                                    + sequenceTaggingLineSplitEntityType
                                )

                            elif (
                                germaNERLineSplitEntityTypeCleaned
                                == sequenceTaggingLineSplitEntityTypeCleaned
                            ):
                                if boolWriteToFile:
                                    writeToFile.write(
                                        flairNERGermanLineSplitFirstWord
                                        + " "
                                        + germaNERLineSplitEntityType
                                        + "\n"
                                    )

                                # add entities to entities2Overlap list
                                entities2Overlap[i].append(
                                    flairNERGermanLineSplitFirstWord
                                    + " "
                                    + germaNERLineSplitEntityType
                                )

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
                        print(
                            "[ERROR] There is a missing line in one or multiple files."
                        )
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

            if boolWriteToFile:
                writeToFile.close()
    else:
        print("[ERROR] There are not the same number of files in every directory.")

    return entities2Overlap


# run code
run()
