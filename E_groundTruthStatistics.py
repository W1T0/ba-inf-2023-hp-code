import os
import numpy as np

directoryPath = "HIPE-scorer-input/groundTruth/output-tsv-annotations/"

count = 0
filecount = 0

list = []

lineslength = 0

# for every file in the directory which ends with .conll
for file in os.listdir(directoryPath):
    filename = os.fsdecode(file)
    if filename.endswith(".tsv"):
        print(filename)
        filecount += 1

        fileEntityCount = 0

        # open file
        readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

        lines = readFromFile.readlines()
        print("lenght lines: " + str(len(lines)))
        lineslength += len(lines)

        for line in lines:
            split = line.split()

            if split[1] != "O" and split[1] != "NE-COARSE-LIT":
                #  print(split)
                count += 1
                fileEntityCount += 1
        print("File entity count: " + str(fileEntityCount))
        list.append(fileEntityCount)

print("Entity count: " + str(count))
print("File count: " + str(filecount))
print("Average entities:" + str(count / filecount))
print("Average entities:" + str(np.average(np.array(list))))
print("Average length lines" + str(lineslength / filecount))
