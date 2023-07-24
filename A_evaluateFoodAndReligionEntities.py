import os


def run(directories):
    """
    Evaluates Precision, Recall and F-Measure for the entity type religion and food.

    directories: A list of directories that store the TSV files of the annotations,  2overlap.
    """

    # [0]:annotations, [1]: overlap
    files = [[], []]
    index = 0

    # save the overall numbers of true positive, false positive and false negativ
    overallTPFood = 0
    overallFPFood = 0
    overallFNFood = 0
    overallTPReligion = 0
    overallFPReligion = 0
    overallFNReligion = 0

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
            tpFood = 0
            fpFood = 0
            fnFood = 0
            tpReligion = 0
            fpReligion = 0
            fnReligion = 0

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

                            # get the special entity type ("FOOD" or "RELIGION")
                            annotationSpecialEntityType = annotationLineSplit[2]
                            overlap2SpecialEntityType = overlap2LineSplit[2]

                            if annotationEntityType == "B-OTH" or overlap2EntityType == "B-OTH":
                                print("----------LINES----------")
                                print("actual: " + str(annotationLineSplit))
                                print("predicted: " + str(overlap2LineSplit))
                                print("--------------------")

                            # TRUE POSITIVE (actual: positive, predicted: Positive)
                            # checks if the entity type for both is "B-OTH" (because both food and religion have this basic entity type)
                            if annotationEntityType == "B-OTH" and overlap2EntityType == "B-OTH":
                                # checks if the special entity type is the same
                                if annotationSpecialEntityType == overlap2SpecialEntityType == "FOOD":
                                    # increase food true positive
                                    tpFood += 1
                                    print("tpFood: " + str(tpFood))
                                if annotationSpecialEntityType == overlap2SpecialEntityType == "RELIGION":
                                    # increase religion true positive
                                    tpReligion += 1
                                    print("tpReligion: " + str(tpReligion))

                            # FALSE POSITIVE (actual: negative, predicted: positive)
                            if overlap2EntityType == "B-OTH":
                                if (
                                    overlap2SpecialEntityType == "FOOD"
                                    and annotationSpecialEntityType != "FOOD"
                                ):
                                    # increase food false positive
                                    fpFood += 1
                                    print("fpFood: " + str(fpFood))
                                if (
                                    overlap2SpecialEntityType == "RELIGION"
                                    and annotationSpecialEntityType != "RELIGION"
                                ):
                                    # increase religion false positive
                                    fpReligion += 1
                                    print("fpReligion: " + str(fpReligion))

                            # FALSE NEGATIVE (actual: positive, predicted: negative)
                            if annotationEntityType == "B-OTH":
                                if (
                                    overlap2SpecialEntityType != "FOOD"
                                    and annotationSpecialEntityType == "FOOD"
                                ):
                                    # increase food false negative
                                    fnFood += 1
                                    print("fnFood: " + str(fnFood))
                                if (
                                    overlap2SpecialEntityType != "RELIGION"
                                    and annotationSpecialEntityType == "RELIGION"
                                ):
                                    # increase religion false negative
                                    fnReligion += 1
                                    print("fnReligion: " + str(fnReligion))

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
            print("Evaluation Food: \nTP: " + str(tpFood) + "\nFP: " + str(fpFood) + "\nFN: " + str(fnFood))
            print(
                "Evaluation Religion: \nTP: "
                + str(tpReligion)
                + "\nFP: "
                + str(fpReligion)
                + "\nFN: "
                + str(fnReligion)
            )

        # add file evaluation to overall evaluation
        overallTPFood += tpFood
        overallFPFood += fpFood
        overallFNFood += fnFood
        overallTPReligion += tpReligion
        overallFPReligion += fpReligion
        overallFNReligion += fnReligion

        print(
            "Overall Evaluation Food: \nTP: "
            + str(overallTPFood)
            + "\nFP: "
            + str(overallFPFood)
            + "\nFN: "
            + str(overallFNFood)
        )
        print(
            "Overall Evaluation Religion: \nTP: "
            + str(overallTPReligion)
            + "\nFP: "
            + str(overallFPReligion)
            + "\nFN: "
            + str(overallFNReligion)
        )

    else:
        print("[ERROR] There are not the same number of files in every directory.")


run(
    [
        "FoodReligionEvaluation/output12/output-tsv-annotations/",
        "FoodReligionEvaluation/output12/output-tsv-2overlap/",
    ]
)
