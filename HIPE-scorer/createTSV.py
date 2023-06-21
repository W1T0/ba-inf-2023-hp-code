import createTSVFromAnnotations
import createTSVFromFlairNERGermanOutput
import createTSVFromNERSequenceTaggingAndGermaNEROutput
import compareAnnotationToTSV

# print("[INFO] Run Annotations TSV Parser")
# createTSVFromAnnotations.run(
#     "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/",  # Stichprobe - Annotationen - Export
#     "./HIPE-scorer/output-tsv-annotations2/",
# )

# print("[INFO] Run Flair NER German TSV Parser")
# createTSVFromFlairNERGermanOutput.run(
#     "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/Stichprobe - Annotationen/",
#     "./HIPE-scorer/output-tsv-flair-ner-german2/",
# )

# print("[INFO] Run NER sequence_tagging and germaNER TSV Parser")
# createTSVFromNERSequenceTaggingAndGermaNEROutput.run(
#     [
#         "./NER-german/germaNER/germaNER-output.txt",
#         "./NER-german/sequence_tagging/sequence_tagging-output2.txt",
#     ],
#     [
#         "./HIPE-scorer/output-tsv-germaNER2/",
#         "./HIPE-scorer/output-tsv-sequence_tagging2/",
#     ],
# )

print("[INFO] Compare TSV")
compareAnnotationToTSV.run(
    [
        "./HIPE-scorer/output-tsv-annotations2/",
        "./HIPE-scorer/output-tsv-flair-ner-german2/",
        "./HIPE-scorer/output-tsv-germaNER2/",
        "./HIPE-scorer/output-tsv-sequence_tagging2/",
    ]
)
