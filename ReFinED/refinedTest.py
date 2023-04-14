from refined.inference.processor import Refined
import os


# refinded
refined = Refined.from_pretrained(model_name='wikipedia_model_with_numbers',
                                  entity_set="wikidata")


# separate refined printouts from my printouts
print("---------------------------------------")
print("---------------------------------------")
print("---------------------------------------")


# EL on every file in a directory
def refinedOnEveryFileInADirectory(directoryString, writeFilename):

    # the directory where the transcripts are stored
    directory = os.fsencode(directoryString)

    # keeps track of how many files haven been processed
    fileCount = 1

    # for every file in the directory which ends with .txt
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):

            # open file
            readFromFile = open(directoryString+filename,
                                "r", encoding="utf-8")

            # process file with refined
            entitiesInFile = refined.process_text(readFromFile.read())

            print("[DEBUG] " + filename + " PROCESSED")

            # save entities to txt file
            writeToFile = open(writeFilename, "a", encoding="utf-8")
            writeToFile.write("--------------------------------- \n")
            writeToFile.write("FILENAME: " + filename + "\n")

            # save list of entities as a string
            entitiesString = ''.join(str(entity) + "\n"
                                     for entity in entitiesInFile)

            # write this string to the txt file
            writeToFile.write(entitiesString)
            writeToFile.close()

            print("[DEBUG] ENTITIES WRITTEN")
            print("[DEBUG] " + str(fileCount) + " FILES DONE")
            fileCount = fileCount + 1

            continue
        else:
            continue


# test text to process
def testText(text):
    testText = refined.process_text(text)
    print(testText)


# EL on every line of a file
def refinedOnLineOfFile(filename):

    # open file
    with open(filename, "r", encoding="utf-8") as file:

        # save every line in file as list?
        lines = [line.rstrip() for line in file]

        # iterate over every line
        for line in lines:
            print("---------------------------------")
            print(line)
            entitiesInLine = refined.process_text(line)
            print(entitiesInLine)


# call functions
# testText("Obama lived in New York")
refinedOnEveryFileInADirectory(
    "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/Stichprobe - Annotationen/", "entities2.txt")
