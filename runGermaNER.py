import os

# path to directory
directoryPath = "./TokenizedLetters/"

#output path 
outputPath = "./output-germaNER/"

# count files
count = 1

# run germaNER on every file in directory 
for file in os.listdir(directoryPath):

    # get the filename
    inputFile = directoryPath + os.fsdecode(file)

    # create output filename with input filename
    outputFile = outputPath + os.fsdecode(file)

    # create command to execute
    cmd = "java -Xmx4g -jar GermaNER-09-09-2015.jar -t " + inputFile + " -o " + outputFile

    # execute command
    os.system(cmd)

    print("[INFO] " + str(count) + " Files done")
    count += 1