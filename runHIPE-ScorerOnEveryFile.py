import os

directories = [
    "./HIPE-scorer/output-tsv-annotations/",
    "./HIPE-scorer/output-tsv-flair-ner-german/",
    "./HIPE-scorer/output-tsv-germaNER/",
    "./HIPE-scorer/output-tsv-sequence_tagging/",
]

outputDirectory = [
    "./HIPE-scorer/output-hipe-flair-ner-german/",
    "./HIPE-scorer/output-hipe-germaNER/",
    "./HIPE-scorer/output-hipe-sequence_tagging/",
]

# [0]: annotations, [1]:flair-ner-german, [2]:germaNER, [3]:sequence_tagging
files = [[], [], [], []]
index = 0

# save every filename in a list
for directory in directories:
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        files[index].append(directory + filename)
    index += 1

# check if there are the same number of files in every directory
if len(files[0]) == len(files[1]) == len(files[2]) == len(files[3]):
    # let the HIPE-scorer run on every NER file with the corresponding annotation
    for i in range(3):
        print(i + 1)
        count = 0
        for j in range(30):
            # get the prediction (flair-ner-german, germaNER, sequence_tagging) and the gold (annotation)
            pred = files[i + 1][j]
            gold = files[0][j]

            # get the output directory
            outdir = outputDirectory[i]

            # get only the original filename to compare
            orgFilenamePred = pred.split("/")[3][0:22]
            orgFilenameGold = gold.split("/")[3][0:22]

            # check if the filenames are the same (and consequently the files)
            if orgFilenameGold == orgFilenamePred:
                # call hipe-scorer function with pred, gold and outdir
                print(orgFilenameGold + "||||" + outdir)
                count += 1
        print("[INFO] " + str(count) + " files have been compared (should be 30)")

else:
    print("[ERROR] There are not the same number of files in every directory.")
