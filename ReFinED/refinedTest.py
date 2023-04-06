from refined.inference.processor import Refined

filename = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/Stichprobe/results/new/L9xx12xx-TL2068_1b_pdf.txt"
refined = Refined.from_pretrained(model_name='wikipedia_model_with_numbers',
                                  entity_set="wikidata")

entities = refined.process_text(
    "Trackmania is a video game developed by Nadeo. Van Gogh painted a picutre once. Time is of the essence here. A Century ago I saw you leave Hamburg.")
print(entities)

# with open(filename, "r", encoding="utf-8") as file:
#     lines = [line.rstrip() for line in file]
#     for line in lines:
#         print("---------------------------------")
#         print(line)
#         entities = refined.process_text(line)
#         print(entities)
