from subscripts import B_TSVParserBasic
from subscripts import B_TSVParser2Overlap
from subscripts import B_TSVParserFlair
import compare_annotations_to_TSV

version = 7

outputAnnotations = "./data/evaluation/annotations/sample_annotations_inception_export_3"
outputFlair = "./HIPE-scorer-input/test process/output" + str(version) + "/output-tsv-flair-ner-german/"
outputS_T = "./HIPE-scorer-input/test process/output" + str(version) + "/output-tsv-sequence_tagging/"
outputGermaNER = "./HIPE-scorer-input/test process/output" + str(version) + "/output-tsv-germaNER/"
output2Overlap = "./HIPE-scorer-input/test process/output" + str(18) + "/output-tsv-2overlap/"
output2OverlapFoodReligion = "./FoodReligionEvaluation/output" + str(18) + "/output-tsv-2overlap/"


# # flair/ner-german-large TSV PARSER
# print("[INFO] Run flair/ner-german-large TSV Parser")
# B_TSVParserFlair.run(
#     "./data/tokenized_documents/kiefer-scholz_collection_tokenized/",
#     outputFlair,
# )

# # germaNER TSV PARSER
# print("[INFO] Run germanNER TSV Parser")
# B_TSVParserBasic.run(
#     "./data/NER-systems_output/output_germaNER/",
#     outputGermaNER,
#     ".txt",
#     "-germaNER" + "_bundle1_hipe2020_de_1",
# )

# # sequence_tagging TSV PARSER
# print("[INFO] Run sequence_tagging TSV Parser ")
# B_TSVParserBasic.run(
#     "./data/NER-systems_output/output_sequence_tagging/",
#     outputS_T,
#     ".txt",
#     "-sequenceTagging" + "_bundle1_hipe2020_de_1",
# )

# # 2 OVERLAP TSV PARSER
# print("[INFO] Run 2 Overlap TSV Parser ")
# B_TSVParser2Overlap.run(
#     [outputFlair, outputGermaNER, outputS_T],
#     "./TokenizedLetters/",  # "./TokenizedLetters/"
#     output2Overlap,
#     output2OverlapFoodReligion,
#     "./NER-german/comparisonOutput" + str(version) + ".txt",
#     False,
#     "./TokenizedLetters/",
#     95,  # food
#     90,  # religion
#     "./NER-german/extractEntitiesFromWikidata/comparisonReligionOutput" + str(version) + ".txt",
#     "./NER-german/extractEntitiesFromWikidata/comparisonFoodOutput" + str(version) + ".txt",
#     False,
# )

# COMPARISON FOR EVALUATION
compare_annotations_to_TSV.run([outputAnnotations, outputFlair, outputS_T, outputGermaNER, output2Overlap])
