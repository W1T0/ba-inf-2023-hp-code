from subscripts import TSV_Parser_basic
from subscripts import TSV_Parser_2overlap
from subscripts import TSV_Parser_flair
from datetime import datetime

# current date and time
now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

# folders where the tsv files are stored
tsv_flair = "./data/tsv_files/tsv_flair/"
tsv_sequence_tagging = "./data/tsv_files/tsv_sequence_tagging/"
tsv_germaNER = "./data/tsv_files/tsv_germaNER/"
tsv_2overlap = "./data/tsv_files/tsv_2overlap/"
tsv_2overlap_food_and_religion = "./data/tsv_files/tsv_2overlap_food_and_religion/"

# flair TSV PARSER
print("[INFO] Run flair TSV Parser")
TSV_Parser_flair.run(
    "./data/tokenized_documents/sample/",  # kiefer-scholz_collection_tokenized/
    tsv_flair,
    False,  # debug variable, set to true if there are error and manually check the console output
)

# # germaNER TSV PARSER
# print("[INFO] Run germanNER TSV Parser")
# TSV_Parser_basic.run(
#     "./data/NER-systems_output/output_germaNER/",
#     tsv_germaNER,
#     ".txt",
#     "-germaNER",
# )

# # sequence_tagging TSV PARSER
# print("[INFO] Run sequence_tagging TSV Parser ")
# TSV_Parser_basic.run(
#     "./data/NER-systems_output/output_sequence_tagging/",
#     tsv_sequence_tagging,
#     ".txt",
#     "-sequenceTagging",
# )

# # 2 OVERLAP TSV PARSER
# print("[INFO] Run 2 Overlap TSV Parser ")
# TSV_Parser_2overlap.run(
#     [tsv_flair, tsv_germaNER, tsv_sequence_tagging],
#     "./data/tokenized_documents/kiefer-scholz_collection_tokenized/",
#     tsv_2overlap,
#     tsv_2overlap_food_and_religion,
#     "./other/test/2overlap_entities/2overlap_entities" + str(now) + ".txt",
#     False,
#     "./data/tokenized_documents/kiefer-scholz_collection_tokenized/",
#     95,  # food similarity measure
#     90,  # religion similarity measure
#     "./other/test/2overlap_entities/religion_entities" + str(now) + ".txt",
#     "./other/test/2overlap_entities/food_entities" + str(now) + ".txt",
#     False,
# )
