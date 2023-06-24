import os
import NEROutputEntities2Overlap

# generate 2 Overlap entities and save them
entities2Overlap = NEROutputEntities2Overlap.run(boolWriteToFile=False)
print(entities2Overlap)


def run(
    directory="D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/test/",  # Stichprobe - Annotationen - Export
    output="./NER-german/output-2overlap-annotations/",
):
    # path of the directory
    directoryPath = directory

    # output path
    outputPath = output

    # the directory where the files are stored
    directory = os.fsencode(directoryPath)

    # keeps track of how many files haven been processed
    fileCount = 1

    # maybe relevant for later
    # filenamesFile2Overlap = []

    # # open file with 2Overlap entities and read every line
    # file2Overlap = open(
    #     "./NER-german/comparison2OverlapOutput2.txt", "r", encoding="utf-8"
    # )
    # file2OverlapLines = file2Overlap.readlines()

    # # save the filenames
    # for line in file2OverlapLines:
    #     if line.startswith("FILE"):
    #         filenamesFile2Overlap.append(line[49:71])

    # for every file in the directory which ends with .conll
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".conll"):
            # save the filename without .conll and with _ instead of - to conform with filenames from 2 Overlap
            filenameClean = filename.replace(".conll", "").replace("_", "-")

            # open file
            readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

            # read every line
            lines = readFromFile.readlines()
            print("[INFO] read lines")

            # open file to write into
            writeToFile = open(
                outputPath
                + filename.replace(".txt", "").replace("_", "-")
                + "-2Overlap"
                + "_bundle1_hipe2020_de_1"
                + ".tsv",
                "a",
                encoding="utf-8",
            )
            print("[INFO] opened output file")

            # write first line
            writeToFile.write(
                "TOKEN	NE-COARSE-LIT	NE-COARSE-METO	NE-FINE-LIT	NE-FINE-METO	NE-FINE-COMP	NE-NESTED	NEL-LIT	NEL-METO	MISC"
                + "\n"
            )

            # keeps track of the number of entities added and the index of the entities list
            index = 0
            count = 0

            # write every word
            for line in lines:
                lineSplit = line.split()
                # print("[INFO] lineSplit: " + str(lineSplit))
                if lineSplit:
                    # save first word of line
                    firstWord = lineSplit[0]

                    # set default predicate
                    predicate = "O"

                    # ignore special characters
                    if (
                        firstWord != ","
                        and firstWord != "."
                        and firstWord != "¬"
                        and firstWord != "?"
                        and firstWord != ":"
                        and firstWord != ";"
                        and firstWord != "-"
                        and firstWord != " "
                        and firstWord != "	"
                    ):
                        firstWord.replace(",", "").replace(".", "").replace(
                            "¬", ""
                        ).replace("?", "").replace(":", "").replace(";", "").replace(
                            "-", ""
                        )

                        # TODO for now it just compares the entityName with one firstWord but needs to compare with every
                        for entities in entities2Overlap:
                            if len(entities) > 0:
                                if entities[0] == filenameClean:
                                    print("EQUAL FILENAME")
                                    print(entities[0], filenameClean)

                                    # delete filename from list
                                    del entities[0]

                                    for entity in entities:
                                        # split entity
                                        entityName = entity.split()[0]

                                        print(firstWord, entityName)

                                        # check for every word if it is an entity
                                        if firstWord == entityName:
                                            # set the predicate, if word is an entity
                                            predicate = entity.split()[1]

                        # write entity and predicate to file
                        writeToFile.write(
                            firstWord + "	" + predicate + "	O	O	O	O	O	_	_	_" + "\n"
                        )

            # check if all entities have been mapped, errror if not


run()
