import createTSVFromAnnotations
import createTSVFromFlairNERGermanOutput
import createTSVFromNERSequenceTaggingAndGermaNEROutput
import compareAnnotationToTSV
import createTSVFrom2Overlap

outputAnnotations = "./HIPE-scorer-output/output3/output-tsv-annotations/"
outputFlair = "./HIPE-scorer-output/output3/output-tsv-flair-ner-german/"
outputS_T = "./HIPE-scorer-output/output3/output-tsv-sequence_tagging/"
outputGermaNER = "./HIPE-scorer-output/output3/output-tsv-germaNER/"
output2Overlap = "./HIPE-scorer-output/output4/output-tsv-2overlap/"

# print("[INFO] Run Annotations TSV Parser")
# createTSVFromAnnotations.run(
#     "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/",
#     outputAnnotations,
# )

# print("[INFO] Run Flair NER German TSV Parser")
# createTSVFromFlairNERGermanOutput.run(
#     "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/Stichprobe - Annotationen/",
#     outputFlair,
# )

# print("[INFO] Run NER sequence_tagging and germaNER TSV Parser")
# createTSVFromNERSequenceTaggingAndGermaNEROutput.run(
#     [
#         "./NER-german/germaNER-output/germaNER-output.txt",
#         "./NER-german/sequence_tagging-output/sequence_tagging-output2.txt",
#     ],
#     [
#         outputGermaNER,
#         outputS_T,
#     ],
# )

# print("[INFO] Run 2 Overlap TSV Parser")
# createTSVFrom2Overlap.run(
#     [outputFlair, outputGermaNER, outputS_T],
#     "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/",  # Stichprobe - Annotationen - Export
#     output2Overlap,
# )

print("[INFO] Compare TSV")
compareAnnotationToTSV.run(
    [outputAnnotations, outputFlair, outputS_T, outputGermaNER, output2Overlap]
)
