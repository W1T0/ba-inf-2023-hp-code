import os
import numpy as np
import csv

version = 11

# the directories where the hipe output is stored
directories = [
    # "./HIPE-scorer/HIPE-results/HIPE-output-test/"
    "./HIPE-results/output-hipe-" + str(version) + "/output-hipe-flair-ner-german/",
    "./HIPE-results/output-hipe-" + str(version) + "/output-hipe-germaNER/",
    "./HIPE-results/output-hipe-" + str(version) + "/output-hipe-sequence_tagging/",
    "./HIPE-results/output-hipe-" + str(version) + "/output-hipe-2overlap/",
]

# iterate over directories
for directory in directories:
    # print(directory)

    # Micro: true positive, false positive and false negative overall arrays
    # ALL LOC OTH ORG PER ALL LOC OTH ORG PER
    tpOverall = np.zeros((10))
    fpOverall = np.zeros((10))
    fnOverall = np.zeros((10))

    # Macro: precision, recall and f1 overall arrays
    # ALL LOC OTH ORG PER ALL LOC OTH ORG PER
    pOverall = np.zeros((20))
    rOverall = np.zeros((20))
    f1Overall = np.zeros((20))

    # stores lists in list
    listsMicroOverall = [tpOverall, fpOverall, fnOverall]
    listsMacroOverall = [pOverall, rOverall, f1Overall]

    # counts the files
    fileCount = 0

    # for every file in the directory which ends with .tsv
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".tsv"):
            # increase file count
            fileCount += 1

            # open file, store every line of file and count lines
            readFromFile = open(directory + filename, "r", encoding="utf-8")
            lines = readFromFile.readlines()
            lineLength = len(lines)
            nMicro = int(np.round((lineLength - 1) / 2)) + 1
            nMacro = len(lines)

            # Micro: open file and store first n lines
            with open(directory + filename, "r", encoding="utf-8") as input_file:
                firstNMicroLines = [next(input_file) for _ in range(nMicro)]

            # Macro: open file and store first n lines
            with open(directory + filename, "r", encoding="utf-8") as input_file:
                firstNMacroLines = [next(input_file) for _ in range(nMacro)]

            # remove first line
            firstNMicroMinus1Lines = firstNMicroLines[1:]
            firstNMacroMinus1Lines = firstNMacroLines[1:]

            # Micro: create temporary lists for true positive, false positive and false negative
            tpTemp = []
            fpTemp = []
            fnTemp = []

            # Macro: create  temporary lists for precision, recall, f1
            # pTemp = []
            # rTemp = []
            # f1Temp = []

            # Micro: get values out of first 8 lines and append them to lists. First the category (ALL, LOC, etc.) and then the tp, fp or fn value
            for line in firstNMicroMinus1Lines:
                lineSplit = line.split()
                tpTemp.append([lineSplit[2], int(lineSplit[6])])
                fpTemp.append([lineSplit[2], int(lineSplit[7])])
                fnTemp.append([lineSplit[2], int(lineSplit[8])])

            # Macro: get values out of p, r and f1 columns and append them to lists
            # TODO account for missing values
            # for line in firstNMacroMinus1Lines:
            #     lineSplit = line.split()
            #     print(lineSplit)
            #     pTemp.append([lineSplit[2], float(lineSplit[3])])
            #     rTemp.append([lineSplit[2], float(lineSplit[4])])
            #     f1Temp.append([lineSplit[2], float(lineSplit[5])])

            # print(pTemp)
            # print(rTemp)
            # print(f1Temp)

            # Micro: stores lists in list
            listsMicroTemp = [tpTemp, fpTemp, fnTemp]
            # listsMacroTemp = [pTemp, rTemp, f1Temp]

            # Micro: iterate over lists in lists
            for listTemp, listOverall in list(zip(listsMicroTemp, listsMicroOverall)):
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

            # # Macro: iterate over lists in lists
            # for i in range(4):
            #     for listTemp, listOverall in list(
            #         zip(listsMacroTemp, listsMacroOverall)
            #     ):
            #         quarterOfList = int(len(listTemp) / 4)
            #         # sum the first quarter of the entries in the temporary list
            #         for entry in listTemp[quarterOfList * i : quarterOfList * (i + 1)]:
            #             if entry[0] == "ALL":
            #                 listOverall[(5 * i) + 0] += entry[1]
            #             # elif entry[0] == "LOC":
            #             #     listOverall[(5 * i) + 1] += entry[1]
            #             # elif entry[0] == "OTH":
            #             #     listOverall[(5 * i) + 2] += entry[1]
            #             # elif entry[0] == "ORG":
            #             #     listOverall[(5 * i) + 3] += entry[1]
            #             # elif entry[0] == "PER":
            #             #     listOverall[(5 * i) + 4] += entry[1]

    # print(tpOverall)
    # print(fpOverall)
    # print(fnOverall)

    # print("fileCount: " + str(fileCount))
    # # Macro: calculate precision, recall, f1
    # macroPrecision = pOverall / fileCount
    # macroRecall = rOverall / fileCount
    # microf1 = f1Overall / fileCount

    # print("Macro Precision: " + str(macroPrecision))
    # print("Macro Recall: " + str(macroRecall))
    # print("Macro F1: " + str(microf1))

    # Micro: calculate precision, recall, f1 (add small number to prevent divison of zero)
    microPrecision = tpOverall / (tpOverall + fpOverall + 0.000000000000001)
    microRecall = tpOverall / (tpOverall + fnOverall + 0.000000000000001)
    microf1 = 2 * ((microPrecision * microRecall) / (microPrecision + microRecall + 0.000000000000001))

    # open file to write into
    writeToFile = open(
        "./HIPE-results/output-hipe-" + str(version) + "-overall-results.csv",
        "a",
        encoding="utf-8",
        newline="",
    )

    # create csv writer
    CSVWriter = csv.writer(writeToFile)

    # write directory name
    CSVWriter.writerow([directory])

    # write header
    CSVWriter.writerow("Micro-Precision Micro-Recall Micro-F1 TP FP FN".split(" "))

    # write data
    for i in range(10):
        CSVWriter.writerow(
            (
                str(microPrecision[i])
                + " "
                + str(microRecall[i])
                + " "
                + str(microf1[i])
                + " "
                + str(tpOverall[i])
                + " "
                + str(fpOverall[i])
                + " "
                + str(fnOverall[i])
            ).split(" ")
        )

    # write new line
    CSVWriter.writerow("\n")

    # print("TP: " + str(tpOverall))
    # print("FP: " + str(fpOverall))
    # print("FN: " + str(fnOverall))
    # print("Micro Precision: " + str(microPrecision))
    # print("Micro Recall: " + str(microRecall))
    # print("Micro F1: " + str(microf1))
