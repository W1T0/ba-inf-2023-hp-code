import os
import testWikidataSPARQLQuery
from fuzzywuzzy import fuzz

#  input path
directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/"  # Stichprobe - Annotationen - Export

# output path
outputPath = "./NER-german/extractEntitiesFromWikidata/comparisonLocationOutput.txt"

# sparql query to get food out of wikidata
query = """
SELECT ?item ?itemLabel {
  {
  SELECT ?item ?itemLabel WHERE {
      { ?item wdt:P31 wd:Q6256 } # country 
    UNION
      { ?item wdt:P31 wd:Q3624078 } # sovereign state 
    UNION
      { ?item wdt:P31 wd:Q15974307 } # administrative unit of Germany 
    UNION
      { ?item wdt:P31 wd:Q42744322 } # urban municipality of Germany (Stadt in Deutschland)
    UNION
      { ?item wdt:P31 wd:Q5119 } # capital city 
    UNION
      { ?item wdt:P31 wd:Q15334 } # municipality of Poland 
    UNION
      { ?item wdt:P31 wd:Q1093829 } # city in the United States 

    SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }
    }
  }
  FILTER lang(?itemLabel) # removes item that have no label 
}

# neustadt (prudnik) gesondert behandeln Q986984
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
