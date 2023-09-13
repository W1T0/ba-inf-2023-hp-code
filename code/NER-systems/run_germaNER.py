import os

# path to input and output
inputPath = "./kiefer-scholz_collection_tokenized/"
outputPath = "./output-germaNER/"

# count files
count = 1

# run germaNER on every file in directory
for file in os.listdir(inputPath):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        # get the filename
        inputFile = inputPath + filename

        # create folder if it does not exist
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        # create output filename with input filename
        outputFile = outputPath + os.fsdecode(file)

        # create command to execute
        cmd = "java -Xmx4g -jar GermaNER-09-09-2015.jar -t " + inputFile + " -o " + outputFile

        # execute command
        os.system(cmd)

        print("[INFO] " + str(count) + " Files done")
        count += 1
