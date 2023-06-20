import os
import testWikidataSPARQLQuery
from fuzzywuzzy import fuzz

#  input path
directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/"  # Stichprobe - Annotationen - Export

# output path
outputPath = "./NER-german/extractEntitiesFromWikidata/comparisonFoodOutput.txt"

# sparql query to get food out of wikidata
query = """
SELECT ?item ?itemLabel {
  {
    SELECT ?item ?itemLabel WHERE {
  { ?item wdt:P31 wd:Q2095 } # is food (Nahrung)
  UNION
  { ?item wdt:P279 wd:Q2095 } # subclass food (Nahrung)
  UNION
  { ?item wdt:P31 wd:Q951964 } # is food product (Nahrungsmittel)
  UNION
  { ?item wdt:P31 wd:Q25403900 } # is food ingredient (Lebensmittelzutat)
  UNION
  { ?item wdt:P31 wd:Q19861951 } # is type of food or dish (Art eines Lebensmittels oder Gerichts)
  UNION
  { ?item wdt:P31 wd:Q736427 } # is staple food (Grundnahrungsmittel)
  UNION
  { ?item wdt:P31 wd:Q185217 } # is dairy product (Milcherzeugnis)
  UNION
  { ?item wdt:P31 wd:Q26856857 } # is products of the meat, dairy, fish, flour and cereal, feed and microbiological industries
  UNION
  { ?item wdt:P279 wd:Q27908772 } # is margarine and similar edible fats (Margarine und ähnliche Speisefette)
  UNION
  { ?item wdt:P279 wd:Q3314483 } # is fruit (Obst)
  UNION
  { ?item wdt:P31 wd:Q1364} # is fruit (Frucht)
        SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }
}
  }
  FILTER lang(?itemLabel) # removes item that have no label 
}
"""
# run query and save as dataframe
data_extracter = testWikidataSPARQLQuery.WikiDataQueryResults(query)
foodDF = data_extracter.load_as_dataframe()
print("[INFO] Query ran")

# open file to write to
writeToFile = open(outputPath, "a", encoding="utf-8")


# for every file in the directory which ends with .txt
for file in os.listdir(directoryPath):
    filename = os.fsdecode(file)
    if filename.endswith(".conll"):
        # open one letter
        letterFile = open(directoryPath + filename, "r", encoding="utf-8")
        print("[INFO] File opened")

        writeToFile.write("FILE: " + filename + "\n")

        # stores every line of file
        lines = letterFile.readlines()

        for line in lines:
            # split the lines
            lineSplit = line.split()

            if lineSplit:
                firstWord = lineSplit[0]

                if firstWord[0].isupper():
                    # print(firstWord)
                    for label in foodDF.itemLabel:
                        if fuzz.ratio(firstWord, label) > 90:
                            # print(firstWord, label)
                            writeToFile.write(
                                "Word: "
                                + firstWord
                                + " | Label: "
                                + label
                                + " | "
                                + str(fuzz.ratio(firstWord, label))
                                + "\n"
                            )

        # add line break
        writeToFile.write("\n")

# close file
writeToFile.close()
