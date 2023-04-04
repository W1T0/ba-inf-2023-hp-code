from refined.inference.processor import Refined

filename = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Kiefer-Scholz Collection/Stichprobe/results/new/L9xx12xx-TL2068_1b_pdf.txt"
refined = Refined.from_pretrained(model_name='wikipedia_model_with_numbers',
                                  entity_set="wikidata")

# spans = refined.process_text("In Hamburg ist das weather schön")

# print(spans)

with open(filename, "r", encoding="utf-8") as file:
    lines = [line.rstrip() for line in file]
    for line in lines:
        print("---------------------------------")
        print(line)
        entities = refined.process_text(line)
        print(entities)
