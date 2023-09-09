import os


def run(
    directories,
    outputPathTXT,
    boolWriteToFile,
    debug,
):
    """
    Returns the entities that are in the output of at least 2 of the three NER-systems (flair, germaNER, sequence_tagging).

    directoriesList: A list of the directories that store the output of the NER-systems.
    outputPathTXT: The path of the file where the output, in this case only the 2Overlap entities, should be stored in.
    boolWriteToFile: A boolean value that determines if the result of this function should be written to the output file. (True or False)
    debug:  A boolean that enables debug prints if set to true.
    """
    if debug:
        print("[DEBUG]#######################################################")
        print("[DEBUG] SCRIPT: get_2overlap_entities_from_NER_output.py")
        print("[DEBUG] 2Overlap writeToFile?: " + str(boolWriteToFile))

    # [0]:flair-ner-german, [1]:germaNER, [2]:sequence_tagging
    files = [[], [], []]
    index = 0

    # save every filename in a list
    for directory in directories:
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            files[index].append(directory + filename)
        index += 1

    # list to save filename and entities to
    entities2Overlap = []

    # check if there are the same number of files in every directory
    if len(files[0]) == len(files[1]) == len(files[2]):
        # compare the entites
        for i in range(30):
            # open files
            flairFile = open(files[0][i], "r", encoding="utf-8")
            germaNERFile = open(files[1][i], "r", encoding="utf-8")
            s_TFile = open(files[2][i], "r", encoding="utf-8")

            # append file name to entites2Overlap list
            entities2Overlap.append([files[0][i].split("/")[4][0:22]])

            if boolWriteToFile:
                # open file to write to
                writeToFile = open(outputPathTXT, "a", encoding="utf-8")
                writeToFile.write("FILE: " + files[0][i] + "\n")

            # stores every line of file
            flairLines = flairFile.readlines()
            germaNERLines = germaNERFile.readlines()
            s_TLines = s_TFile.readlines()

            # checks if all the files have the same number of lines
            if len(flairLines) == len(germaNERLines) == len(s_TLines):
                # split every line and compare them
                for j in range(len(flairLines) - 1):
                    # split the lines
                    # ignore the first line, because of HIPE-scorer headlines (j+1)
                    flairLineSplit = flairLines[j + 1].split()
                    germaNERLineSplit = germaNERLines[j + 1].split()
                    s_TLineSplit = s_TLines[j + 1].split()

                    # checks if there is a line for every file
                    if flairLineSplit and germaNERLineSplit and s_TLineSplit:
                        # get the first word of the line
                        flairFirstWord = flairLineSplit[0]
                        germaNERFirstWord = germaNERLineSplit[0]
                        s_TFirstWord = s_TLineSplit[0]

                        # checks if the first word is the same
                        if flairFirstWord == germaNERFirstWord == s_TFirstWord:
                            # default values that won't appear, used for comparison
                            germaNEREntityType = "-2"
                            s_TEntityType = "-3"
                            flairEntityTypeCleaned = "-1"
                            germaNEREntityTypeCleaned = "-2"
                            s_TEntityTypeCleaned = "-3"

                            # flair: checks that the entity tpye exist and get the entity type
                            # without B- or I- infront (cleaned) and with B- or I- infront
                            if flairLineSplit[1] != "O":
                                flairEntityTypeCleaned = flairLineSplit[1].split("-")[1]

                            # germaNER: checks that the entity tpye exist and get the entity type
                            # without B- or I- infront (cleaned) and with B- or I- infront
                            if germaNERLineSplit[1] != "O":
                                germaNEREntityTypeCleaned = germaNERLineSplit[1].split("-")[1]
                                germaNEREntityType = germaNERLineSplit[1]

                            # sequence_tagging: checks that the entity tpye exist and get the entity type
                            # without B- or I- infront (cleaned) and with B- or I- infront
                            if s_TLineSplit[1] != "O":
                                s_TEntityTypeCleaned = s_TLineSplit[1].split("-")[1]
                                s_TEntityType = s_TLineSplit[1]

                            """ 
                            checks if the entity type is the same for two
                            checks only if the cleaned type is the same, because flair does not offer B- or I-
                            if they are the same, it takes the "uncleaned" entity type of germanNER or sequence_tagging
                            ignore all I-OTH entity types, because they are false most of the time
                            """

                            # create a boolean that checks if both entity types are I-OTH
                            IOTH = False
                            if germaNEREntityType == "I-OTH" or s_TEntityType == "I-OTH":
                                IOTH = True

                            # checks if entity type of flair and germaNER is the same
                            if flairEntityTypeCleaned == germaNEREntityTypeCleaned and not IOTH:
                                if boolWriteToFile:
                                    # write entity and entity type to file
                                    writeToFile.write(flairFirstWord + " " + germaNEREntityType + "\n")

                                # add entities to entities2Overlap list
                                entities2Overlap[i].append(flairFirstWord + " " + germaNEREntityType)

                            # checks if entity type of flair and sequence_tagging is the same
                            elif flairEntityTypeCleaned == s_TEntityTypeCleaned and not IOTH:
                                if boolWriteToFile:
                                    # write entity and entity type to file
                                    writeToFile.write(flairFirstWord + " " + s_TEntityType + "\n")

                                # add entities to entities2Overlap list
                                entities2Overlap[i].append(flairFirstWord + " " + s_TEntityType)

                            # checks if entity type of germaNER and sequence_tagging is the same
                            elif germaNEREntityTypeCleaned == s_TEntityTypeCleaned and not IOTH:
                                if boolWriteToFile:
                                    # write entity and entity type to file
                                    writeToFile.write(flairFirstWord + " " + germaNEREntityType + "\n")

                                # add entities to entities2Overlap list
                                entities2Overlap[i].append(flairFirstWord + " " + germaNEREntityType)

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
                            print("[ERROR]: " + flairFirstWord + " " + germaNERFirstWord + " " + s_TFirstWord)
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
                    + str(len(flairLines))
                    + " "
                    + str(len(germaNERLines))
                    + " "
                    + str(len(s_TLines))
                )

            if boolWriteToFile:
                writeToFile.close()
    else:
        print("[ERROR] There are not the same number of files in every directory.")

    return entities2Overlap
