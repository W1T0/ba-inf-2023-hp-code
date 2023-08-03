import B_compareAnnotationToTSV
import B_TSVParserBasic
import B_TSVParser2Overlap
import B_TSVParserFlair
import B_evaluateFoodAndReligionEntities

version = 7

outputAnnotations = "./HIPE-scorer-input/output" + str(version) + "/output-tsv-annotations/"
outputFlair = "./HIPE-scorer-input/output" + str(version) + "/output-tsv-flair-ner-german/"
outputS_T = "./HIPE-scorer-input/output" + str(version) + "/output-tsv-sequence_tagging/"
outputGermaNER = "./HIPE-scorer-input/output" + str(version) + "/output-tsv-germaNER/"
output2Overlap = "./HIPE-scorer-input/output" + str(16) + "/output-tsv-2overlap/"
output2OverlapFoodReligion = "./FoodReligionEvaluation/output" + str(16) + "/output-tsv-2overlap/"


# ANNOTATIONS TSV PARSER
# print("[INFO] Run Annotations TSV Parser")
# B_TSVParserBasic.run(
#     "Annotationen/Stichprobe-Annotationen-Inception-Export-3/",
#     outputAnnotations,
#     ".conll",
#     "-annotations",
# )

# FLAIR TSV PARSER
# print("[INFO] Run Flair TSV Parser")
# B_TSVParserFlair.run(
#     "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/Stichprobe-Annotationen-3/",
#     outputFlair,
# )

# GERMANER TSV PARSER
# print("[INFO] Run germanNER TSV Parser")
# B_TSVParserBasic.run(
#     "./NER-german-output/output-germaNER/",
#     outputGermaNER,
#     ".txt",
#     "-germaNER" + "_bundle1_hipe2020_de_1",
# )

# SEQUENCE_TAGGING TSV PARSER
# print("[INFO] Run sequence_tagging TSV Parser ")
# B_TSVParserBasic.run(
#     "./NER-german-output/output-Sequence_tagging/",
#     outputS_T,
#     ".txt",
#     "-sequenceTagging" + "_bundle1_hipe2020_de_1",
# )

# 2 OVERLAP TSV PARSER
print("[INFO] Run 2 Overlap TSV Parser ")
B_TSVParser2Overlap.run(
    [outputFlair, outputGermaNER, outputS_T],
    "./TokenizedLetters/",  # "./TokenizedLetters/"
    output2Overlap,
    output2OverlapFoodReligion,
    "./NER-german/comparisonOutput" + str(version) + ".txt",
    False,
    "./TokenizedLetters/",
    90,  # food
    80,  # religion
    "./NER-german/extractEntitiesFromWikidata/comparisonReligionOutput" + str(version) + ".txt",
    "./NER-german/extractEntitiesFromWikidata/comparisonFoodOutput" + str(version) + ".txt",
    False,
)

# FOOD AND RELIGION EVALUATION
print("[INFO] Run Food and Religion Evaluation")
B_evaluateFoodAndReligionEntities.run(
    [
        "FoodReligionEvaluation/output12/output-tsv-annotations/",
        output2OverlapFoodReligion,  # "FoodReligionEvaluation/output13/output-tsv-2overlap/"
    ]
)

# COMPARISON
# print("[INFO] Compare TSV")
# B_compareAnnotationToTSV.run([outputAnnotations, outputFlair, outputS_T, outputGermaNER, output2Overlap])
