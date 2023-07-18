import B_compareWikidataQueryWithLetterWords


def run():
    """
    Has the Wikidata queries saved as strings and calls a function to process them.
    """

    # religion query
    queryReligion = """
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
        UNION
          { ?item wdt:P31*|wdt:P279*|wdt:P1269*|wdt:P361*|wdt:P463* wd:Q34651 }      # -""- : christian Church 

        SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }
        }
      }
      FILTER lang(?itemLabel) # removes items that have no label 
    }
    """

    # food query
    queryFood = """
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

    religion = B_compareWikidataQueryWithLetterWords.compare(
        "./TokenizedLetters/",
        "./NER-german/extractEntitiesFromWikidata/comparisonReligionOutput3.txt",
        queryReligion,
        80,
        False,
    )
    print("[INFO] Religion query ran")

    food = B_compareWikidataQueryWithLetterWords.compare(
        "./TokenizedLetters/",
        "./NER-german/extractEntitiesFromWikidata/comparisonFoodOutput2.txt",
        queryFood,
        90,
        False,
    )
    print("[INFO] Food query ran")

    return [religion, food]
