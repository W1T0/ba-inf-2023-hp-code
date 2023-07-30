import B_compareWikidataQueryWithLetterWords


def run(
    directoryPath,
    levenshteinDistanceFood,
    levenshteinDistanceReligion,
    outputPathFood,
    outputPathReligion,
    boolWriteToFile,
):
    """
    Has the Wikidata queries saved as strings and calls a function to process them.

    directoryPath: The path of the directory where the files are stored in.
    levenshteinDistance(-Food, -Religion): The Levenshtein-Distance. A metric to compare the differences between two strings.
    outputPath(-Food, -Religion): The path of the file where the output should be stored in.
    boolWriteToFile: A boolean value that determines if the result of this function should be written to the output file. (True or False)
    """

    # religion query
    queryReligionNew = """
    SELECT ?item ?itemLabel {
      {
      SELECT ?item ?itemLabel WHERE {
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q63187345 }   # subclass of | is | facet of | part of | member of : religious occupation
        UNION
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q23847174 }   # -""- : religious concept 
        UNION
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q1530022 }    # -""- : religious organization
        UNION
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q24398318 }   # -""- : religious  building 
        UNION
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q21029893 }   # -""- : religious object 
        UNION
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q1370598 }    # -""- : structure of worship
        UNION
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q105889895 }  # -""- : religious site
        UNION
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q60075825 }   # -""- : christian worship
        UNION
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q63188683 }   # -""- : christian religious occupation
        UNION 
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q2349219 }    # -""- : Ecphonesis 
        UNION 
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q9174 }       # -""- : religion
        UNION 
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q1539016 }    # -""- : christian worship
        UNION 
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q34651 }      # -""- : christian church
        UNION 
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q5043 }       # -""- : christianity

        SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }
        }
      }
      FILTER lang(?itemLabel) # removes items that have no label 
    }
    """

    queryReligionOld = """
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
          { ?item wdt:P279 wd:Q24398318 } # subclass of | religious  building 
        UNION
          { ?item wdt:P31 wd:Q21029893 } # is | religious object 
        UNION
          { ?item wdt:P279 wd:Q21029893 } # subclass of | religious object 
        UNION
          { ?item wdt:P31 wd:Q1370598 } # is | structure of worship
        UNION
          { ?item wdt:P31 wd:Q105889895 } # is | religious site
        UNION
          { ?item wdt:P361 wd:Q1539016 } # part of | Christian worship
        UNION
          { ?item wdt:P31 wd:Q60075825 } # is | Christian worship

        SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }
        }
      }
      FILTER lang(?itemLabel) # removes item that have no label 
    }
    """

    # food query
    queryFoodNew = """
    SELECT ?item ?itemLabel {
      {
      SELECT ?item ?itemLabel WHERE {
          { ?item wdt:P31*|wdt:P279* wd:Q2095 }       # subclass of | is : food 
        UNION
          { ?item wdt:P31*|wdt:P279* wd:Q951964 }     # -""- : food product 
        UNION
          { ?item wdt:P31*|wdt:P279* wd:Q25403900 }   # -""- : food ingredient 
        UNION
          { ?item wdt:P31*|wdt:P279* wd:Q19861951 }   # -""- : type of food or dish 
        UNION
          { ?item wdt:P31*|wdt:P279* wd:Q736427 }     # -""- : staple food 
        UNION
          { ?item wdt:P31*|wdt:P279* wd:Q185217 }     # -""- : dairy product 
        UNION
          { ?item wdt:P31*|wdt:P279* wd:Q26856857 }   # -""- : products of the meat, dairy, fish, flour and cereal, feed and microbiological industries
        UNION
          { ?item wdt:P31*|wdt:P279* wd:Q27908772 }   # -""- : margarine and similar edible fats 
        UNION
          { ?item wdt:P31*|wdt:P279* wd:Q3314483 }    # -""- : fruit (Obst)
        UNION
          { ?item wdt:P31*|wdt:P279* wd:Q1364}        # -""- : fruit (Frucht)
      
        SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }
        }
      }
      FILTER lang(?itemLabel) # removes item that have no label 
    }
    """

    queryFoodOld = """
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

    religion = B_compareWikidataQueryWithLetterWords.compare(
        directoryPath, queryReligionNew, levenshteinDistanceReligion, outputPathReligion, boolWriteToFile
    )

    food = B_compareWikidataQueryWithLetterWords.compare(
        directoryPath, queryFoodOld, levenshteinDistanceFood, outputPathFood, boolWriteToFile
    )

    # religion = B_compareWikidataQueryWithLetterWords.compare(
    #     "./TokenizedLetters/",
    #     "./NER-german/extractEntitiesFromWikidata/comparisonReligionOutput3.txt",
    #     queryReligion2,
    #     80,
    #     False,
    # )
    print("[INFO] Religion query ran")

    # food = B_compareWikidataQueryWithLetterWords.compare(
    #     "./TokenizedLetters/",
    #     "./NER-german/extractEntitiesFromWikidata/comparisonFoodOutput2.txt",
    #     queryFood2,
    #     90,
    #     False,
    # )
    print("[INFO] Food query ran")

    return [religion, food]
