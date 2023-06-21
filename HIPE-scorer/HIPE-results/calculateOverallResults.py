import os
import numpy as np

directories = [
    "./HIPE-scorer/HIPE-results/output-hipe-flair-ner-german/",
    "./HIPE-scorer/HIPE-results/output-hipe-germaNER/",
    "./HIPE-scorer/HIPE-results/output-hipe-sequence_tagging/",
]

# "./HIPE-scorer/HIPE-results/output-hipe-flair-ner-german/"
# "./output-hipe-germaNER/",
# "./output-hipe-sequence_tagging/",

# iterate over directories
for directory in directories:
    # true positive, false positive and false negative overall arrays
    # ALL LOC OTH ORG PER ALL LOC OTH ORG PER
    tpOverall = np.zeros((10))
    fpOverall = np.zeros((10))
    fnOverall = np.zeros((10))

    listsOverall = [tpOverall, fpOverall, fnOverall]
    # for every file in the directory which ends with .tsv
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".tsv"):
            # open file, store every line of file and count lines
            readFromFile = open(directory + filename, "r", encoding="utf-8")
            lines = readFromFile.readlines()
            lineLength = len(lines)
            n = int(np.round((lineLength - 1) / 2)) + 1

            # open file and store first 9 lines
            with open(directory + filename, "r", encoding="utf-8") as input_file:
                firstNLines = [next(input_file) for _ in range(n)]

            # remove first line
            firstNMinus1Lines = firstNLines[1:]

            # create temporary lists for true positive, false positive and false negative
            tpTemp = []
            fpTemp = []
            fnTemp = []

            # get values out of first 8 lines and append them to lists
            for line in firstNMinus1Lines:
                lineSplit = line.split()
                tpTemp.append([lineSplit[2], int(lineSplit[6])])
                fpTemp.append([lineSplit[2], int(lineSplit[7])])
                fnTemp.append([lineSplit[2], int(lineSplit[8])])

            # stores lists in list
            listsTemp = [tpTemp, fpTemp, fnTemp]
            # print(tpTemp)
            # print(fpTemp)
            # print(fnTemp)

            # iterate over lists in lists
            for listTemp, listOverall in list(zip(listsTemp, listsOverall)):
                halfOfList = int(len(listTemp) / 2)
                # sum the first half of the entries in the temporary list
                for entry in listTemp[:halfOfList]:
                    if entry[0] == "ALL":
                        listOverall[0] += entry[1]
                    elif entry[0] == "LOC":
                        listOverall[1] += entry[1]
                    elif entry[0] == "OTH":
                        listOverall[2] += entry[1]
                    elif entry[0] == "ORG":
                        listOverall[3] += entry[1]
                    elif entry[0] == "PER":
                        listOverall[4] += entry[1]

                # sum the second half of the entries in the temporary list
                for entry in listTemp[halfOfList:]:
                    if entry[0] == "ALL":
                        listOverall[5] += entry[1]
                    elif entry[0] == "LOC":
                        listOverall[6] += entry[1]
                    elif entry[0] == "OTH":
                        listOverall[7] += entry[1]
                    elif entry[0] == "ORG":
                        listOverall[8] += entry[1]
                    elif entry[0] == "PER":
                        listOverall[9] += entry[1]
    print(tpOverall)
    print(fpOverall)
    print(fnOverall)

    # calculate precision
    precision = tpOverall / (tpOverall + fpOverall)

    # calculate recall
    recall = tpOverall / (tpOverall + fnOverall)

    # calculate f1
    f1 = 2 * ((precision * recall) / (precision + recall))

    print("Micro Precision:" + str(precision))
    print("Micro Recall:" + str(recall))
    print("Micro F1:" + str(f1))
