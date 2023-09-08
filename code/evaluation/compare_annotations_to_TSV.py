import os


def run(directories):
    """
    Compares the annotations in TSV format to the TSV files of flair, germaNER, sequence_tagging and 2overlap.
    Prints if something does not match up.
    Necessary because it can detect errors in the TSV parser and the HIPE-scorer requires the files to have the same number of lines, etc.

    directories: A list of directories that store the TSV files of the annotations, flair, germaNER, sequence_tagging and 2overlap.
    """

    # [0]:annotations, [1]:flair-ner-german, [2]:germaNER, [3]:sequence_tagging, [4]: overlap
    files = [[], [], [], [], []]
    index = 0

    # save every filename in a list
    for directory in directories:
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            files[index].append(directory + filename)
        index += 1
    print("[INFO] Files saved")

    # check if there are the same number of files in every directory
    if len(files[0]) == len(files[1]) == len(files[2]) == len(files[3]) == len(files[4]):
        # compare the entites
        for i in range(30):
            # open files
            annotationFile = open(files[0][i], "r", encoding="utf-8")
            flairNERGermanFile = open(files[1][i], "r", encoding="utf-8")
            germaNERFile = open(files[2][i], "r", encoding="utf-8")
            sequenceTaggingFile = open(files[3][i], "r", encoding="utf-8")
            overlap2File = open(files[4][i], "r", encoding="utf-8")
            print("[INFO] " + str(i + 1) + " Files opened")

            # stores every line of file
            annotationLines = annotationFile.readlines()
            flairNERGermanLines = flairNERGermanFile.readlines()
            germaNERLines = germaNERFile.readlines()
            sequenceTaggingLines = sequenceTaggingFile.readlines()
            overlap2Lines = overlap2File.readlines()

            # string to print if there is an error
            printFiles = (
                "[ERROR]: annotationFile: "
                + files[0][i]
                + " | flairNERGermanFile: "
                + files[1][i]
                + " | germaNERFile: "
                + files[2][i]
                + " | sequenceTaggingFile: "
                + files[3][i]
                + " | overlap2File: "
                + files[4][i]
            )

            # checks if all the files have the same number of lines
            if (
                len(flairNERGermanLines)
                == len(germaNERLines)
                == len(sequenceTaggingLines)
                == len(annotationLines)
                == len(overlap2Lines)
            ):
                # split every line and compare them
                for j in range(len(flairNERGermanLines) - 1):
                    annotationLineSplit = annotationLines[j + 1].split()
                    flairNERGermanLineSplit = flairNERGermanLines[j + 1].split()
                    germaNERLineSplit = germaNERLines[j + 1].split()
                    sequenceTaggingLineSplit = sequenceTaggingLines[j + 1].split()
                    overlap2LineSplit = overlap2Lines[j + 1].split()

                    # checks if there is a line for every file
                    if (
                        annotationLineSplit
                        and flairNERGermanLineSplit
                        and germaNERLineSplit
                        and sequenceTaggingLineSplit
                        and overlap2LineSplit
                    ):
                        annotationLineSplitFirstWord = annotationLineSplit[0]
                        flairNERGermanLineSplitFirstWord = flairNERGermanLineSplit[0]
                        germaNERLineSplitFirstWord = germaNERLineSplit[0]
                        sequenceTaggingLineSplitFirstWord = sequenceTaggingLineSplit[0]
                        overlap2FirstWord = overlap2LineSplit[0]

                        # checks if the first word is the same
                        if (
                            annotationLineSplitFirstWord
                            == flairNERGermanLineSplitFirstWord
                            == germaNERLineSplitFirstWord
                            == sequenceTaggingLineSplitFirstWord
                            == overlap2FirstWord
                        ):
                            # print("[INFO] First word is the same")
                            x = 1

                        else:
                            print("[ERROR] The first word is not the same.")
                            print(printFiles)
                            print(
                                "[ERROR]: "
                                + annotationLineSplitFirstWord
                                + " | "
                                + flairNERGermanLineSplitFirstWord
                                + " | "
                                + germaNERLineSplitFirstWord
                                + " | "
                                + sequenceTaggingLineSplitFirstWord
                                + " | "
                                + overlap2FirstWord
                            )
                    else:
                        print("[ERROR] There is a missing line in one or multiple files.")
                        print(printFiles)
            else:
                print("[ERROR] The files do not have the same number of lines.")
                print(printFiles)
                print(
                    "[ERROR]: "
                    + str(len(annotationLines))
                    + " | "
                    + str(len(flairNERGermanLines))
                    + " | "
                    + str(len(germaNERLines))
                    + " | "
                    + str(len(sequenceTaggingLines))
                    + " | "
                    + str(len(overlap2Lines))
                )
    else:
        print("[ERROR] There are not the same number of files in every directory.")
