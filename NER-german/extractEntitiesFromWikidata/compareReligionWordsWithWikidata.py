# import os
# import testWikidataSPARQLQuery
# from fuzzywuzzy import fuzz
import compareWikidataQueryWithLetterWords

#  input path
directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/"  # Stichprobe - Annotationen - Export

# output path
outputPath = "./NER-german/extractEntitiesFromWikidata/comparisonReligionOutput3.txt"

# Levenshtein distance
levenshteinDistance = 80

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

compareWikidataQueryWithLetterWords.compare(
    directoryPath, outputPath, query, levenshteinDistance
)
