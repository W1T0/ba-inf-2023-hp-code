import os
import clef_evaluation

# maybe before run compareAnnotationToTSV

directories = [
    "./HIPE-scorer-output/output3/output-tsv-annotations/",
    "./HIPE-scorer-output/output3/output-tsv-flair-ner-german/",
    "./HIPE-scorer-output/output3/output-tsv-germaNER/",
    "./HIPE-scorer-output/output3/output-tsv-sequence_tagging/",
    "./HIPE-scorer-output/output3/output-tsv-2overlap/",
]

outputDirectory = [
    "./HIPE-results/output-hipe-flair-ner-german/",
    "./HIPE-results/output-hipe-germaNER/",
    "./HIPE-results/output-hipe-sequence_tagging/",
    "./HIPE-results/output-hipe-2overlap/",
]

# [0]: annotations, [1]:flair-ner-german, [2]:germaNER, [3]:sequence_tagging, [4]:2overlap
files = [[], [], [], [], []]
index = 0

# save every filename in a list
for directory in directories:
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        files[index].append(directory + filename)
    index += 1

# sort the lists
files[0].sort()
files[1].sort()
files[2].sort()
files[3].sort()
files[4].sort()

# check if there are the same number of files in every directory
if len(files[0]) == len(files[1]) == len(files[2]) == len(files[3]) == len(files[4]):
    # let the HIPE-scorer run on every NER file with the corresponding annotation
    for i in range(4):
        count = 0
        for j in range(30):
            # get the prediction (flair-ner-german, germaNER, sequence_tagging, 2overlap) and the gold (annotation)
            pred = files[i + 1][j]
            gold = files[0][j]

            # get the output directory
            outdir = outputDirectory[i]

            # create folder if it does not exist
            if not os.path.exists(outdir):
                os.makedirs(outdir)

            # get only the original filename to compare
            orgFilenamePred = pred.split("/")[3][0:22]
            orgFilenameGold = gold.split("/")[3][0:22]

            # check if the filenames are the same (and consequently the files)
            if orgFilenameGold == orgFilenamePred:
                # call hipe-scorer function with pred, gold and outdir
                # print(orgFilenameGold + "||||" + outdir)
                # print(pred, gold, outdir)

                clef_evaluation.ownMain(
                    {
                        "--glue": None,
                        "--help": False,
                        "--hipe_edition": "hipe-2022",
                        "--log": "log.txt",
                        "--n_best": "1",
                        "--noise-level": None,
                        "--original_nel": False,
                        "--outdir": outdir,
                        "--pred": pred,
                        "--ref": gold,
                        "--skip-check": False,
                        "--suffix": None,
                        "--tagset": None,
                        "--task": "nerc_coarse",
                        "--time-period": None,
                    }
                )

                count += 1
            else:
                print("[ERROR]: " + orgFilenameGold + " | " + orgFilenamePred)

        print("[INFO] " + str(count) + " files have been compared (should be 30)")

else:
    print("[ERROR] There are not the same number of files in every directory.")
