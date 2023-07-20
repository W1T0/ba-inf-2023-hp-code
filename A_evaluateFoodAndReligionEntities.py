import os


def run(directories):
    """
    ...

    directories: A list of directories that store the TSV files of the annotations,  2overlap.
    """

    # [0]:annotations, [1]: overlap
    files = [[], []]
    index = 0

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
            print("[INFO] " + str(i + 1) + " Files opened")

            # stores every line of file
            annotationLines = annotationFile.readlines()
            overlap2Lines = overlap2File.readlines()

            # string to print if there is an error
            printFiles = "[ERROR]: annotationFile: " + files[0][i] + " | overlap2File: " + files[1][i]

            # checks if all the files have the same number of lines
            if len(annotationLines) == len(overlap2Lines):
                # split every line and compare them
                for j in range(len(annotationLines) - 1):
                    annotationLineSplit = annotationLines[j + 1].split()
                    overlap2LineSplit = overlap2Lines[j + 1].split()

                    # checks if there is a line for every file
                    if annotationLineSplit and overlap2LineSplit:
                        # get the first word (entity)
                        annotationSplitFirstWord = annotationLineSplit[0]
                        overlap2FirstWord = overlap2LineSplit[0]

                        # checks if the first word is the same
                        if annotationSplitFirstWord == overlap2FirstWord:
                            # get the entity type
                            annotationSplitEntityType = annotationLineSplit[1]
                            overlap2EntityType = overlap2LineSplit[1]

                            # checks if the entity type for both is "B-OTH" (because both food and religion have this basic entity type)
                            if annotationSplitEntityType == "B-OTH" and overlap2EntityType == "B-OTH":
                                print(annotationSplitEntityType, overlap2EntityType)

                                # get the special entity type ("FOOD" or "RELIGION")
                                annotationSplitSpecialEntityType = annotationLineSplit[2]
                                overlap2SpecialEntityType = overlap2LineSplit[2]

                                # checks if the special entity type is the same
                                if annotationSplitSpecialEntityType == overlap2SpecialEntityType:
                                    print(annotationSplitSpecialEntityType, overlap2SpecialEntityType)
                                    print(annotationLineSplit[7])

                                    # gucken wie tp fp fn funktionieren

                        else:
                            print("[ERROR] The first word is not the same.")
                            print(printFiles)
                            print("[ERROR]: " + annotationSplitFirstWord + " | " + overlap2FirstWord)
                    else:
                        print("[ERROR] There is a missing line in one or multiple files.")
                        print(printFiles)
            else:
                print("[ERROR] The files do not have the same number of lines.")
                print(printFiles)
                print("[ERROR]: " + str(len(annotationLines)) + " | " + str(len(overlap2Lines)))
    else:
        print("[ERROR] There are not the same number of files in every directory.")


run(
    [
        "FoodReligionEvaluation/output12/output-tsv-annotations/",
        "FoodReligionEvaluation/output12/output-tsv-2overlap/",
    ]
)
