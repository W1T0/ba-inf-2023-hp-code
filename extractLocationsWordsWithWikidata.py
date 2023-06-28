import compareWikidataQueryWithLetterWords


def run(directoryPath, outputPath, levenshteinDistance, boolWriteToFile):
    # #  input path
    # directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/"  # Stichprobe - Annotationen - Export

    # # output path
    # outputPath = "./NER-german/extractEntitiesFromWikidata/comparisonLocationOutput2.txt"

    # # Levenshtein distance
    # levenshteinDistance = 90

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

    # call function to compare query with every word in the letters of the directory
    return compareWikidataQueryWithLetterWords.compare(
        directoryPath, outputPath, query, levenshteinDistance, boolWriteToFile
    )
