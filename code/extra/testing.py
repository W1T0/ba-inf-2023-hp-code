import os
import json
from fuzzywuzzy import fuzz


# print("Test")
# for i in range(30):
#     print("Number" + str(i), end="\r")

# # open file, store every line of file and count lines
# readFromFile = open(
#     "HIPE-results\output-hipe-15\output-hipe-2overlap\L9xx12xx-TL2068-1b-pdf-2Overlap_bundle1_hipe2020_de_1_nerc_coarse.json",
#     "r",
#     encoding="utf-8",
# )

# data = json.load(readFromFile)

# print(data["NE-COARSE-LIT"]["TIME-ALL"]["LED-ALL"]["ALL"]["partial"]["TP"])

# for i in str(data.values()).split("{"):
#     print(i)


# values = [
#     [0.33, 0.81, 0.47],
#     [0.49, 0.83, 0.62],
#     [0.03, 0.62, 0.06],
#     [0.08, 0.97, 0.15],
#     [0.12, 0.88, 0.22],
#     [0.49, 0.83, 0.62],
#     [0.15, 0.81, 0.25],
#     [0.6, 0.74, 0.67],
#     [0.33, 0.81, 0.47],
#     [0.83, 0.69, 0.75],
#     [0.49, 0.73, 0.58],
#     [0.84, 0.6, 0.7],
#     [0.08, 0.85, 0.15],
#     [0.16, 0.77, 0.26],
#     [0.3, 0.69, 0.41],
#     [0.67, 0.69, 0.68],
#     [0.36, 0.62, 0.46],
#     [0.73, 0.63, 0.68],
#     [0.59, 0.62, 0.6],
#     [0.91, 0.57, 0.7],
#     [1, 0.54, 0.7],
#     [0.94, 0.49, 0.64],
# ]

# list = []

# i = 1

# for value in values:
#     sum = value[0] + value[1] + value[2]
#     avg = sum / 3
#     list.append(avg)
#     print("Eval " + str(i) + ": " + str(avg))
#     i += 1

# print(max(list))
