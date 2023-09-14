from subscripts import TSV_Parser_basic
from subscripts import TSV_Parser_2overlap
from subscripts import TSV_Parser_flair
from subscripts import create_KG
from datetime import datetime
import time

# current date and time
now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
start_time = time.time()

# folders where the tsv files are stored
tsv_flair = "./data/tsv_files/tsv_flair/"
tsv_sequence_tagging = "./data/tsv_files/tsv_sequence_tagging/"
tsv_germaNER = "./data/tsv_files/tsv_germaNER/"
tsv_2overlap = "./data/tsv_files/tsv_2overlap/"
tsv_2overlap_food_and_religion = "./data/tsv_files/tsv_2overlap_food_and_religion/"

# folder where the KGs are stored, full for the file with all KGs, single for every KG as its own file
KG_folder_full = "./visualization/output-kg/test-kg" + str(now) + ".txt"
KG_folder_single = "./visualization/documents/KGs/"

# flair TSV PARSER
print("[INFO] ////// RUN TSV PARSER flair //////")
TSV_Parser_flair.run(
    "./data/kiefer-scholz_collection_tokenized/",  # input path
    tsv_flair,  # output path
    False,  # debug variable, set to true if there are error and manually check the console output
    "-flair",  # ending of TSV filename
)

# germaNER TSV PARSER
print("[INFO] ////// RUN TSV PARSER germaNER //////")
TSV_Parser_basic.run(
    "./data/NER-systems_output/output-germaNER/",  # input path
    tsv_germaNER,  # output path
    ".txt",  # file ending
    "-germaNER",  # ending of TSV filename
)

# sequence_tagging TSV PARSER
print("[INFO] ////// RUN TSV PARSER sequence_tagging //////")
TSV_Parser_basic.run(
    "./data/NER-systems_output/output-sequence_tagging/",  # input path
    tsv_sequence_tagging,  # output path
    ".txt",  # file ending
    "-sequenceTagging",  # ending of TSV filename
)

# 2 OVERLAP TSV PARSER
print("[INFO] ////// RUN TSV PARSER 2 Overlap (majority voting) //////")
TSV_Parser_2overlap.run(
    [tsv_flair, tsv_germaNER, tsv_sequence_tagging],  # list of directories of NER-systems output
    "./data/kiefer-scholz_collection_tokenized/",  # input path for tokenized documents
    tsv_2overlap,  # output path
    tsv_2overlap_food_and_religion,  # output path for food and religion files
    "-2overlap",  # ending of TSV filename
    "./other/test/2overlap_entities/2overlap_entities"
    + str(now)
    + ".txt",  # path to store 2 Overlap entities in a txt file
    False,  # boolean, if 2 Overlap entities should be written to a txt file, see above
    "./data/kiefer-scholz_collection_tokenized/",  # input path for query runner
    95,  # similarity measure food
    90,  # similarity measure religion
    "./other/test/2overlap_entities/religion_entities"
    + str(now)
    + ".txt",  # path to store religion entities in a txt file
    "./other/test/2overlap_entities/food_entities"
    + str(now)
    + ".txt",  # path to store food entities in a txt file
    False,  # boolean, if food and religin entities should be written to a txt file, see above
    False,  # debug variable
)

# CREATE KG
print("[INFO] ////// RUN CREATE KG //////")
create_KG.run(tsv_2overlap_food_and_religion, KG_folder_full, KG_folder_single, False)

# print time
end_time = time.time()
duration = end_time - start_time
print("SCRIPT FINISHED IN " + str(duration) + " SECONDS")
