import B_createTSVFromFlairNERGermanOutput
import B_compareAnnotationToTSV
import B_createTSVFrom2Overlap
import B_createTSVBasic

version = 7

outputAnnotations = (
    "./HIPE-scorer-input/output" + str(version) + "/output-tsv-annotations/"
)
outputFlair = (
    "./HIPE-scorer-input/output" + str(version) + "/output-tsv-flair-ner-german/"
)
outputS_T = (
    "./HIPE-scorer-input/output" + str(version) + "/output-tsv-sequence_tagging/"
)
outputGermaNER = "./HIPE-scorer-input/output" + str(version) + "/output-tsv-germaNER/"
output2Overlap = "./HIPE-scorer-input/output" + str(6) + "/output-tsv-2overlap/"

# print("[INFO] Run Annotations TSV Parser")
# B_createTSVBasic.run(
#     "Annotationen/Stichprobe-Annotationen-Inception-Export-3/",
#     outputAnnotations,
#     ".conll",
#     "-annotations",
# )

print("[INFO] Run Flair NER German TSV Parser")
B_createTSVFromFlairNERGermanOutput.run(
    "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/Stichprobe-Annotationen-3/",
    outputFlair,
)

# print("[INFO] Run germaNER TSV Parser")
# B_createTSVBasic.run(
#     "./NER-german-output/output-germaNER/",
#     outputGermaNER,
#     ".txt",
#     "-germaNER" + "_bundle1_hipe2020_de_1",
# )

# print("[INFO] Run sequence_tagging TSV Parser")
# B_createTSVBasic.run(
#     "./NER-german-output/output-Sequence_tagging/",
#     outputS_T,
#     ".txt",
#     "-sequenceTagging" + "_bundle1_hipe2020_de_1",
# )

# print("[INFO] Run 2 Overlap TSV Parser")
# B_createTSVFrom2Overlap.run(
#     [outputFlair, outputGermaNER, outputS_T],
#     "./TokenizedLetters/",
#     output2Overlap,
# )

print("[INFO] Compare TSV")
B_compareAnnotationToTSV.run(
    [outputAnnotations, outputFlair, outputS_T, outputGermaNER, output2Overlap]
)
