import os


directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/Stichprobe-Annotationen-3/"  # Stichprobe-Annotationen-3 oder nergermantest

outputDirectoryPath = "./TokenizedLetters/"

count = 1

# for every file in the directory which ends with .conll
for file in os.listdir(directoryPath):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        # open file
        readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

        # create folder if it does not exist
        if not os.path.exists(outputDirectoryPath):
            os.makedirs(outputDirectoryPath)

        # open file to write into
        writeToFile = open(
            outputDirectoryPath + filename,
            "a",
            encoding="utf-8",
        )

        lines = readFromFile.readlines()

        for line in lines:
            split = line.split()

            for word in split:
                # write word to file
                writeToFile.write(word + "\n")

        writeToFile.close()
        print("[INFO] " + str(count) + " Files done")
        count += 1
