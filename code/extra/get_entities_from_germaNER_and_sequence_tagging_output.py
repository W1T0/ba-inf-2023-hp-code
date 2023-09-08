# the path to the file to read (usually a NER output file)
path = "./NER german/germaNER/germaNER-briefe16-30-output3.txt"
# path = "./NER german/sequence_tagging/sequence_tagging-output2.txt"

# the output path
outputPath = "./NER german/outputTest.txt"
# outputPath = "./NER german/germaNER/germaNER-entities3-withoutIOTH.txt"
# outputPath = "./NER german/sequence_tagging/sequence_tagging-entities3.txt"

# opens the file and reads all lines
file = open(path, "r", encoding="utf-8")
lines = file.readlines()

# saves the extracted entities
entities = []

# gets every entity of a NER output file
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
        # print(line.replace("\n", ""))
        entities.append(line)

    # character that I use to differentiate between letters/documents
    elif line.startswith("#"):
        entities.append("\n------------------- \n \n")

# open file to write entities to txt file
writeToFile = open(outputPath, "a", encoding="utf-8")
writeToFile.write("READ FILE: " + path + "\n\n")

# write all entities in a file
for entity in entities:
    writeToFile.write(
        " ".join(entity.split()) + "\n"
    )  # removes all whitespaces, tabs, etc.

print("[DEBUG] Entities written")
writeToFile.close()
