# Using readlines()
file = open("./NER german/sequence_tagger/output2.txt", "r", encoding="utf-8")
lines = file.readlines()

count = 0
entities = []
for line in lines:
    count += 1
    # string = str(line)
    # string.strip()
    # string.replace(" ", "")
    # " ".join(string.split())
    if (
        line.endswith("I-PER\n")
        or line.endswith("B-PER\n")
        or line.endswith("I-LOC\n")
        or line.endswith("B-LOC\n")
        or line.endswith("I-OTH\n")
        or line.endswith("B-OTH\n")
        or line.endswith("I-ORG\n")
        or line.endswith("B-ORG\n")
        or line.startswith("#")
    ):
        print(line)
        entities.append(line)

print(len(entities))
