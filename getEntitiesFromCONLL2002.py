import os

directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe-Annotationen-Inception-Export-2/"
outputPath = "./Annotationen/output-entities-annotations-2.txt"

# the directory where the files are stored
directory = os.fsencode(directoryPath)

# keeps track of how many files haven been processed
fileCount = 1

# for every file in the directory which ends with .conll
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".conll"):
        # stores the entities
        entities = []

        # open file
        readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

        # stores every line of file
        lines = readFromFile.readlines()

        # checks if a line ends with a specific string
        for line in lines:
            if (
                line.endswith("I-PER\n")
                or line.endswith("B-PER\n")
                or line.endswith("I-LOC\n")
                or line.endswith("B-LOC\n")
                or line.endswith("I-OTH\n")
                or line.endswith("B-OTH\n")
                or line.endswith("I-ORG\n")
                or line.endswith("B-ORG\n")
            ):
                # print(line)
                entities.append(line)

        # open file to write entities to txt file
        writeToFile = open("./Annotationen/outputEntities.txt", "a", encoding="utf-8")

        # write entities
        writeToFile.write("# --- ENTITIES OF " + filename + " ---\n")
        for entity in entities:
            allWords = entity.split()
            predicate = allWords[-1]  # like I-PER, etc,
            object = allWords[0]  # the entity
            if object != "¬":
                writeToFile.write(object + " " + predicate + "\n")

        writeToFile.write("\n")
        writeToFile.close()

        print("[DEBUG] ENTITIES WRITTEN")
        print("[DEBUG] " + str(fileCount) + " FILES DONE")

        fileCount += 1
        continue
    else:
        continue
