import os
import NEROutputEntities2Overlap

entities2Overlap = NEROutputEntities2Overlap.run(boolWriteToFile=False)
print(entities2Overlap)


def run(
    directory="D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/",
    output="./HIPE-scorer/output-2overlap-annotations/",
):
    # path of the directory
    directoryPath = directory

    # output path
    outputPath = output

    # the directory where the files are stored
    directory = os.fsencode(directoryPath)

    # keeps track of how many files haven been processed
    fileCount = 1

    # for every file in the directory which ends with .conll
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".conll"):
            print(1)
            # print(filename.replace(".conll", ""))

            # # open file with 2Overlap entities and read every line
            # file2Overlap = open(
            #     "./NER-german/comparison2OverlapOutput2.txt", "r", encoding="utf-8"
            # )
            # file2OverlapLines = file2Overlap.readlines()

            # for line in file2OverlapLines:
            #     if line.startswith("FILE"):
            #         print(line[49:71])

            # open file to write tinto

            # write first line

            # write every word

            # for every word in every line

            # replace special characters

            # set default predicate

            # check for entities

            # write entity and predicate to file

            # check if all entities have been mapped, errror if not
