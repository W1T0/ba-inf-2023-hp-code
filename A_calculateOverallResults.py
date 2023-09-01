import os
import numpy as np
import csv
import json

name = "old-transcription-sequence_tagging"

# the directories where the hipe output is stored
directories = [
    # "./HIPE-scorer/HIPE-results/HIPE-output-test/"
    # "./HIPE-results/output-hipe-" + str(version) + "/output-hipe-flair-ner-german/",
    # "./HIPE-results/output-hipe-" + str(version) + "/output-hipe-germaNER/",
    # "./HIPE-results/output-hipe-" + str(version) + "/output-hipe-sequence_tagging/",
    "./HIPE-results/test process/output-hipe-4/output-hipe-sequence_tagging/"
]

# iterate over directories
for directory in directories:
    # MICRO: true positive, false positive and false negative overall arrays
    # ALL LOC OTH ORG PER ALL LOC OTH ORG PER
    tpOverall = np.zeros((10))
    fpOverall = np.zeros((10))
    fnOverall = np.zeros((10))

    # MACRO: precision, recall and f1 overall arrays
    # ALL LOC OTH ORG PER ALL LOC OTH ORG PER
    pOverall = np.zeros((10))
    rOverall = np.zeros((10))
    f1Overall = np.zeros((10))

    # count of categories for macro calculation
    countCategories = np.zeros((10))

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

            # list of all categories and all evaluation regimes
            categoriesList = ["ALL", "LOC", "OTH", "ORG", "PER"]
            evalRegimeList = ["ent_type", "strict"]  # ent_type: fuzzy, strict: strict

            # index to access correct position in array
            index = 0

            # MICRO: sum tp, fp and fn of all categories and all evaluation regimes
            for evalRegime in evalRegimeList:
                for category in categoriesList:
                    # check if category exists
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

            # index to access correct position in array (used again for next loop)
            index = 0

            # MACRO: sum tp, fp and fn of all categories and all evaluation regimes
            # eigentlich P_micro, R_micro, F1_micro
            for evalRegime in evalRegimeList:
                for category in categoriesList:
                    # check if category exists
                    if category in data["NE-COARSE-LIT"]["TIME-ALL"]["LED-ALL"]:
                        pOverall[index] += data["NE-COARSE-LIT"]["TIME-ALL"]["LED-ALL"][category][evalRegime][
                            "P_micro"
                        ]
                        rOverall[index] += data["NE-COARSE-LIT"]["TIME-ALL"]["LED-ALL"][category][evalRegime][
                            "R_micro"
                        ]
                        f1Overall[index] += data["NE-COARSE-LIT"]["TIME-ALL"]["LED-ALL"][category][
                            evalRegime
                        ]["F1_micro"]

                        countCategories[index] += 1

                    index += 1

    # MICRO: calculate precision, recall, f1 (add small number to prevent divison of zero)
    microPrecision = tpOverall / (tpOverall + fpOverall + 0.000000000000001)
    microRecall = tpOverall / (tpOverall + fnOverall + 0.000000000000001)
    microf1 = 2 * ((microPrecision * microRecall) / (microPrecision + microRecall + 0.000000000000001))

    # MACRO: divide the sum of P, R and F1 by how much their categories came up
    pOverall = pOverall / countCategories
    rOverall = rOverall / countCategories
    f1Overall = f1Overall / countCategories

    # open file to write into
    writeToFile = open(
        "./HIPE-results/output-hipe-" + name + "-final-results-json.csv",
        "a",
        encoding="utf-8",
        newline="",
    )

    # create csv writer
    CSVWriter = csv.writer(writeToFile)

    # write directory name
    CSVWriter.writerow([directory])

    # MICRO: write header and data
    CSVWriter.writerow("Micro-Precision Micro-Recall Micro-F1 TP FP FN".split(" "))
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

    # MACRO: write header and data
    CSVWriter.writerow("Macro-Precision Macro-Recall Macro-F1".split(" "))
    for i in range(10):
        CSVWriter.writerow((str(pOverall[i]) + " " + str(rOverall[i]) + " " + str(f1Overall[i])).split(" "))

    # print("TP: " + str(tpOverall))
    # print("FP: " + str(fpOverall))
    # print("FN: " + str(fnOverall))
    # print("Micro Precision: " + str(microPrecision))
    # print("Micro Recall: " + str(microRecall))
    # print("Micro F1: " + str(microf1))

    # print("P: " + str(pOverall))
    # print("R: " + str(rOverall))
    # print("F1: " + str(f1Overall))
