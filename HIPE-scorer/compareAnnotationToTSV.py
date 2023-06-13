import os

directories = [
    "./HIPE-scorer/output-tsv-annotations/",
    "./HIPE-scorer/output-tsv-flair-ner-german/",
    "./HIPE-scorer/output-tsv-germaNER/",
    "./HIPE-scorer/output-tsv-sequence_tagging/",
]

# [0]:flair-ner-german, [1]:germaNER, [2]:sequence_tagging
files = [[], [], [], []]
index = 0

# save every filename in a list
for directory in directories:
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        files[index].append(directory + filename)
    index += 1
print("[INFO] Files saved")

# check if there are the same number of files in every directory
if len(files[0]) == len(files[1]) == len(files[2]) == len(files[3]):
    # compare the entites
    for i in range(30):
        # open files
        annotationFile = open(files[0][i], "r", encoding="utf-8")
        flairNERGermanFile = open(files[1][i], "r", encoding="utf-8")
        germaNERFile = open(files[2][i], "r", encoding="utf-8")
        sequenceTaggingFile = open(files[3][i], "r", encoding="utf-8")
        print("[INFO] Files opened")

        # stores every line of file
        annotationLines = annotationFile.readlines()
        flairNERGermanLines = flairNERGermanFile.readlines()
        germaNERLines = germaNERFile.readlines()
        sequenceTaggingLines = sequenceTaggingFile.readlines()

        # checks if all the files have the same number of lines
        if (
            len(flairNERGermanLines)
            == len(germaNERLines)
            == len(sequenceTaggingLines)
            == len(annotationLines)
        ):
            # split every line and compare them
            for j in range(len(flairNERGermanLines) - 1):
                annotationLineSplit = annotationLines[j + 1].split()
                flairNERGermanLineSplit = flairNERGermanLines[j + 1].split()
                germaNERLineSplit = germaNERLines[j + 1].split()
                sequenceTaggingLineSplit = sequenceTaggingLines[j + 1].split()

                # checks if there is a line for every file
                if (
                    annotationLineSplit
                    and flairNERGermanLineSplit
                    and germaNERLineSplit
                    and sequenceTaggingLineSplit
                ):
                    annotationLineSplitFirstWord = annotationLineSplit[0]
                    flairNERGermanLineSplitFirstWord = flairNERGermanLineSplit[0]
                    germaNERLineSplitFirstWord = germaNERLineSplit[0]
                    sequenceTaggingLineSplitFirstWord = sequenceTaggingLineSplit[0]

                    # checks if the first word is the same
                    if (
                        annotationLineSplitFirstWord
                        == flairNERGermanLineSplitFirstWord
                        == germaNERLineSplitFirstWord
                        == sequenceTaggingLineSplitFirstWord
                    ):
                        # print("[INFO] First word is the same")
                        x = 1

                    else:
                        print("[ERROR] The first word is not the same.")
                        print(
                            "[ERROR]: annotationFile: "
                            + files[0][i]
                            + " | flairNERGermanFile: "
                            + files[1][i]
                            + " | germaNERFile: "
                            + files[2][i]
                            + " | sequenceTaggingFile: "
                            + files[3][i]
                        )
                        print(
                            "[ERROR]: "
                            + annotationLineSplitFirstWord
                            + ""
                            + flairNERGermanLineSplitFirstWord
                            + " "
                            + germaNERLineSplitFirstWord
                            + " "
                            + sequenceTaggingLineSplitFirstWord
                        )
                else:
                    print("[ERROR] There is a missing line in one or multiple files.")
                    print(
                        "[ERROR]: annotationFile: "
                        + files[0][i]
                        + " | flairNERGermanFile: "
                        + files[1][i]
                        + " | germaNERFile: "
                        + files[2][i]
                        + " | sequenceTaggingFile: "
                        + files[3][i]
                    )
        else:
            print("[ERROR] The files do not have the same number of lines.")
            print(
                "[ERROR]: annotationFile: "
                + files[0][i]
                + " | flairNERGermanFile: "
                + files[1][i]
                + " | germaNERFile: "
                + files[2][i]
                + " | sequenceTaggingFile: "
                + files[3][i]
            )
            print(
                "[ERROR]: "
                + str(len(annotationLines))
                + " "
                + str(len(flairNERGermanLines))
                + " "
                + str(len(germaNERLines))
                + " "
                + str(len(sequenceTaggingLines))
            )
else:
    print("[ERROR] There are not the same number of files in every directory.")
