import B_compareAnnotationToTSV
import B_TSVParserBasic
import B_TSVParser2Overlap
import B_TSVParserFlair

version = 7

outputAnnotations = "./HIPE-scorer-input/output" + str(version) + "/output-tsv-annotations/"
outputFlair = "./HIPE-scorer-input/output" + str(version) + "/output-tsv-flair-ner-german/"
outputS_T = "./HIPE-scorer-input/output" + str(version) + "/output-tsv-sequence_tagging/"
outputGermaNER = "./HIPE-scorer-input/output" + str(version) + "/output-tsv-germaNER/"
output2Overlap = "./HIPE-scorer-input/output" + str(8) + "/output-tsv-2overlap/"

# print("[INFO] Run Annotations TSV Parser")
# B_TSVParserBasic.run(
#     "Annotationen/Stichprobe-Annotationen-Inception-Export-3/",
#     outputAnnotations,
#     ".conll",
#     "-annotations",
# )

# print("[INFO] Run TSV Parser Flair")
# B_TSVParserFlair.run(
#     "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/Stichprobe-Annotationen-3/",
#     outputFlair,
# )

# print("[INFO] Run TSV Parser germaNER")
# B_TSVParserBasic.run(
#     "./NER-german-output/output-germaNER/",
#     outputGermaNER,
#     ".txt",
#     "-germaNER" + "_bundle1_hipe2020_de_1",
# )

# print("[INFO] Run TSV Parser sequence_tagging")
# B_TSVParserBasic.run(
#     "./NER-german-output/output-Sequence_tagging/",
#     outputS_T,
#     ".txt",
#     "-sequenceTagging" + "_bundle1_hipe2020_de_1",
# )

print("[INFO] Run TSV Parser 2 Overlap")
B_TSVParser2Overlap.run(
    [outputFlair, outputGermaNER, outputS_T],
    "./TokenizedLetters/test/",  # "./TokenizedLetters/"
    output2Overlap,
)

# print("[INFO] Compare TSV")
# B_compareAnnotationToTSV.run(
#     [outputAnnotations, outputFlair, outputS_T, outputGermaNER, output2Overlap]
# )
