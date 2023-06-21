import compareWikidataQueryWithLetterWords

#  input path
directoryPath = "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/"  # Stichprobe - Annotationen - Export

# output path
outputPath = "./NER-german/extractEntitiesFromWikidata/comparisonFoodOutput2.txt"

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

compareWikidataQueryWithLetterWords.compare(directoryPath, outputPath, query)
