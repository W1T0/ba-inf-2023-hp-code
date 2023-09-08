import os

inputDirectoryPath = "./data/kiefer-scholz_collection_transcriptions/"

outputDirectoryPath = "./data/tokenized_documents/kiefer-scholz_collection_tokenized/"

count = 1

# for every file in the directory which ends with .txt
for file in os.listdir(inputDirectoryPath):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        # open file
        readFromFile = open(inputDirectoryPath + filename, "r", encoding="utf-8")

        # create folder if it does not exist
        if not os.path.exists(outputDirectoryPath):
            os.makedirs(outputDirectoryPath)

        # open file to write into
        writeToFile = open(
            outputDirectoryPath + filename,
            "a",
            encoding="utf-8",
        )

        # read every line
        lines = readFromFile.readlines()

        # split every line and write the single words
        for line in lines:
            split = line.split()

            for word in split:
                # write word to file
                writeToFile.write(word + "\n")

        writeToFile.close()
        print("[INFO] " + str(count) + " Files done")
        count += 1
