import os
import testWikidataSPARQLQuery
from fuzzywuzzy import fuzz

#  input path
directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/"  # Stichprobe - Annotationen - Export

# output path
outputPath = "./NER-german/extractEntitiesFromWikidata/comparisonReligionOutput.txt"

# sparql query to get food out of wikidata
query = """
SELECT ?item ?itemLabel ?offName {
  {
  SELECT ?item ?itemLabel WHERE {
      { ?item wdt:P463 wd:Q34651 } # member of | christian church
    UNION
      { ?item wdt:P361 wd:Q5043 } # part of | christianity
    UNION
      { ?item wdt:P31 wd:Q63187345 } # is | religious occupation
    UNION
      { ?item wdt:P31 wd:Q34651 } # is | Christian Church 
    UNION
      { ?item wdt:P31 wd:Q23847174 } # is | religious concept 
    UNION
      { ?item wdt:P361 wd:Q9174 } # part of | religion 
    UNION
      { ?item wdt:P31 wd:Q1530022 } # is | religious organization (Glaubensgemeinschaft)
    UNION
      { ?item wdt:P1269 wd:Q9174 } # facet of | religion 
    UNION
      { ?item wdt:P31 wd:Q24398318 } # is | religious  building 
    UNION
      { ?item wdt:P31 wd:Q21029893 } # is | religious object 
    UNION
      { ?item wdt:P31 wd:Q1370598 } # is | structure of worship
    UNION
      { ?item wdt:P31 wd:Q105889895 } # is | religious site
    UNION
      { ?item wdt:P361 wd:Q1539016 } # part of | Christian worship

    SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }
    }
  }
  FILTER lang(?itemLabel) # removes item that have no label 
}

# timed out: { ?item wdt:P31 wd:Q16970 } # is | church building 
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
                        if fuzz.ratio(firstWord, label) > 79:
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
