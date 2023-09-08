import os
import spacy
import turcy
from turcy import pattern_builder

directoryPath = (
    "./turCy/Stichprobe - Annotationen/"
)
outputPath = "./RE-german/"

# the directory where the files are stored
directory = os.fsencode(directoryPath)

# keeps track of how many files haven been processed
fileCount = 1

# build pattern?
# text = ""
# triple = ["", "", ""]

# pattern = pattern_builder.find(text, triple)
# pattern_builder.add(pattern)


def example(string):
    nlp = spacy.load("de_core_news_lg", exclude=["ner"])
    nlp.max_length = 2096700
    turcy.add_to_pipe(nlp)  # apply/use current patterns in list
    pipeline_params = {"attach_triple2sentence": {"pattern_list": "small"}}
    doc = nlp(string, component_cfg=pipeline_params)     
    for sent in doc.sents:
        # print(sent)
        for triple in sent._.triples:
            (subj, pred, obj) = triple["triple"]
            print(f"subject:'{subj}', predicate:'{pred}' and object: '{obj}'")

# for every file in the directory which ends with
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        # open file
        readFromFile = open(directoryPath + filename, "r", encoding="utf-8")

        letterOrLine = 1

        if letterOrLine == 0:
            wholeLetter = readFromFile.read()
            # print(wholeLetter)
            example(wholeLetter)
        elif letterOrLine == 1:
            # stores every line of file
            lines = readFromFile.readlines()
            for line in lines:
                example(line)

        print("[DEBUG] " + str(fileCount) + " FILES DONE")
        fileCount += 1
    else:
        continue
