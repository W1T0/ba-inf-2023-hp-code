import os
import numpy as np
import csv
import json

version = 15

# the directories where the hipe output is stored
directories = [
    # "./HIPE-scorer/HIPE-results/HIPE-output-test/"
    # "./HIPE-results/output-hipe-" + str(version) + "/output-hipe-flair-ner-german/",
    # "./HIPE-results/output-hipe-" + str(version) + "/output-hipe-germaNER/",
    # "./HIPE-results/output-hipe-" + str(version) + "/output-hipe-sequence_tagging/",
    "./HIPE-results/output-hipe-"
    + str(version)
    + "/output-hipe-2overlap/",
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
        if filename.endswith(".json"):
            # increase file count
            fileCount += 1

            # open file
            readFromFile = open(directory + filename, "r", encoding="utf-8")

            # read data from json
            data = json.load(readFromFile)

            categoriesList = ["ALL", "LOC", "OTH", "ORG", "PER"]
            evalRegimeList = ["ent_type", "strict"]  # ent_type: fuzzy, strict: strict

            index = 0

            for evalRegime in evalRegimeList:
                for category in categoriesList:
                    if category in data["NE-COARSE-LIT"]["TIME-ALL"]["LED-ALL"]:
                        tpOverall[index] += data["NE-COARSE-LIT"]["TIME-ALL"]["LED-ALL"][category][
                            evalRegime
                        ]["TP"]
                        fpOverall[index] += data["NE-COARSE-LIT"]["TIME-ALL"]["LED-ALL"][category][
                            evalRegime
                        ]["FP"]
                        fnOverall[index] += data["NE-COARSE-LIT"]["TIME-ALL"]["LED-ALL"][category][
                            evalRegime
                        ]["FN"]
                    index += 1

    # Micro: calculate precision, recall, f1 (add small number to prevent divison of zero)
    microPrecision = tpOverall / (tpOverall + fpOverall + 0.000000000000001)
    microRecall = tpOverall / (tpOverall + fnOverall + 0.000000000000001)
    microf1 = 2 * ((microPrecision * microRecall) / (microPrecision + microRecall + 0.000000000000001))

    # open file to write into
    writeToFile = open(
        "./HIPE-results/output-hipe-" + str(version) + "-overall-results-json.csv",
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
