import createTSVFromAnnotations
import createTSVFromFlairNERGermanOutput
import createTSVFromNERSequenceTaggingAndGermaNEROutput
import compareAnnotationToTSV
import createTSVFrom2Overlap
import createTSVFromGermaNEROutput
import createTSVFromSequenceTaggingOutput

version = 5

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
output2Overlap = "./HIPE-scorer-input/output" + str(version) + "/output-tsv-2overlap/"

# print("[INFO] Run Annotations TSV Parser")
# createTSVFromAnnotations.run(
#     "Annotationen/Stichprobe-Annotationen-Inception-Export-2/",
#     outputAnnotations,
# )

# print("[INFO] Run Flair NER German TSV Parser")
# createTSVFromFlairNERGermanOutput.run(
#     "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/Stichprobe-Annotationen-3/",
#     outputFlair,
# )

# print("[INFO] Run germaNER TSV Parser")
# createTSVFromGermaNEROutput.run("./NER-german-output/output-germaNER/", outputGermaNER)

# print("[INFO] Run sequence_tagging TSV Parser")
# createTSVFromSequenceTaggingOutput.run("./NER-german-output/output-Sequence_tagging/", outputS_T)

print("[INFO] Run 2 Overlap TSV Parser")
createTSVFrom2Overlap.run(
    [outputFlair, outputGermaNER, outputS_T],
    "./TokenizedLetters/",
    output2Overlap,
)

# print("[INFO] Compare TSV")
# compareAnnotationToTSV.run(
#     [outputAnnotations, outputFlair, outputS_T, outputGermaNER, output2Overlap]
# )
