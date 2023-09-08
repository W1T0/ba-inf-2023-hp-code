import os
import csv


def run(directories):
    """
    Evaluates Precision, Recall and F-Measure for the linking of locations.

    directories: A list of directories that store the TSV files of the annotations,  2overlap.
    """

    # [0]:annotations, [1]: overlap
    files = [[], []]
    index = 0

    # save the overall numbers of true positive, false positive and false negativ
    overallTPLocation = 0
    overallFPLocation = 0
    overallFNLocation = 0

    # save every filename in a list
    for directory in directories:
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            files[index].append(directory + filename)
        index += 1
    print("[INFO] Files saved")

    # check if there are the same number of files in every directory
    if len(files[0]) == len(files[1]):
        # compare the entites
        for i in range(30):
            # open files
            annotationFile = open(files[0][i], "r", encoding="utf-8")
            overlap2File = open(files[1][i], "r", encoding="utf-8")
            print("[INFO] " + str(i + 1) + " Files opened: " + files[0][i] + " | " + files[1][i])

            # stores every line of file
            annotationLines = annotationFile.readlines()
            overlap2Lines = overlap2File.readlines()

            # string to print if there is an error
            printFiles = "[ERROR]: annotationFile: " + files[0][i] + " | overlap2File: " + files[1][i]

            # save the numbers of true positive, false positive and false negativ
            tpLocation = 0
            fpLocation = 0
            fnLocation = 0

            # checks if all the files have the same number of lines
            if len(annotationLines) == len(overlap2Lines):
                # split every line and compare them
                for j in range(len(annotationLines) - 1):
                    annotationLineSplit = annotationLines[j + 1].split()
                    overlap2LineSplit = overlap2Lines[j + 1].split()

                    # checks if there is a line for every file
                    if annotationLineSplit and overlap2LineSplit:
                        # get the first word (entity)
                        annotationFirstWord = annotationLineSplit[0]
                        overlap2FirstWord = overlap2LineSplit[0]

                        # checks if the first word is the same
                        if annotationFirstWord == overlap2FirstWord:
                            # get the entity type
                            annotationEntityType = annotationLineSplit[1]
                            overlap2EntityType = overlap2LineSplit[1]

                            # print to manually check the results
                            if annotationEntityType == "B-LOC" or overlap2EntityType == "B-LOC":
                                print("----------LINES----------")
                                print("actual: " + str(annotationLineSplit))
                                print("predicted: " + str(overlap2LineSplit))
                                print("--------------------")

                            # get the wikidataQID
                            annotationQID = annotationLineSplit[7]
                            overlap2QID = overlap2LineSplit[7]

                            # TRUE POSITIVE (actual: positive, predicted: Positive)
                            # checks if the entity type for both is "B-LOC"
                            if annotationEntityType == "B-LOC" and overlap2EntityType == "B-LOC":
                                # checks if the wikidataQID is the same
                                if annotationQID == overlap2QID:
                                    # increase  true positive
                                    tpLocation += 1
                                    print("tpLocation: " + str(tpLocation))

                            # FALSE POSITIVE (actual: negative, predicted: positive)
                            if overlap2EntityType == "B-LOC":
                                if annotationQID == "_" and overlap2QID != "_":
                                    # increase  false positive
                                    fpLocation += 1
                                    print("fpLocation: " + str(fpLocation))

                            # FALSE NEGATIVE (actual: positive, predicted: negative)
                            if annotationEntityType == "B-LOC":
                                if (
                                    annotationQID != "_"
                                    and overlap2QID == "_"
                                    or annotationQID != overlap2QID
                                ):
                                    # increase  false negative
                                    fnLocation += 1
                                    print("fnLocation: " + str(fnLocation))

                        else:
                            print("[ERROR] The first word is not the same.")
                            print(printFiles)
                            print("[ERROR]: " + annotationFirstWord + " | " + overlap2FirstWord)
                    else:
                        print("[ERROR] There is a missing line in one or multiple files.")
                        print(printFiles)
            else:
                print("[ERROR] The files do not have the same number of lines.")
                print(printFiles)
                print("[ERROR]: " + str(len(annotationLines)) + " | " + str(len(overlap2Lines)))

            # calculate evaluation
            print(
                "Evaluation Location: \nTP: "
                + str(tpLocation)
                + "\nFP: "
                + str(fpLocation)
                + "\nFN: "
                + str(fnLocation)
            )

            # add file evaluation to overall evaluation
            overallTPLocation += tpLocation
            overallFPLocation += fpLocation
            overallFNLocation += fnLocation

        # calculate precision, recall, f1 (add small number to prevent divison of zero)
        precisionLocation = overallTPLocation / (overallTPLocation + overallFPLocation + 0.000000000000001)
        recallLocation = overallTPLocation / (overallTPLocation + overallFNLocation + 0.000000000000001)
        f1Location = 2 * (
            (precisionLocation * recallLocation) / (precisionLocation + recallLocation + 0.000000000000001)
        )

        # open file to write into
        writeToFile = open(
            "./HIPE-results/output-locationsLinking-results.csv",
            "a",
            encoding="utf-8",
            newline="",
        )

        # create csv writer
        CSVWriter = csv.writer(writeToFile)

        # write header
        CSVWriter.writerow(["Locations"])
        CSVWriter.writerow("Pre Recall F1 TP FP FN".split(" "))

        # write food
        CSVWriter.writerow(
            (
                str(precisionLocation)
                + " "
                + str(recallLocation)
                + " "
                + str(f1Location)
                + " "
                + str(overallTPLocation)
                + " "
                + str(overallFPLocation)
                + " "
                + str(overallFNLocation)
            ).split(" ")
        )

        # write new line
        CSVWriter.writerow("\n")

    else:
        print("[ERROR] There are not the same number of files in every directory.")


run(
    [
        "HIPE-scorer-input/groundTruth/output-tsv-annotations/",
        "HIPE-scorer-input/output15/output-tsv-2overlap/",
    ]
)
