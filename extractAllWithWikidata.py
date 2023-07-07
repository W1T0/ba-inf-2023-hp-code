import compareWikidataQueryWithLetterWords


def run():
    # run religion query
    queryReligion = """
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

      # timed out: { ?item wdt:P31 wd:Q16970 } # is | church building 
      """

    religion = compareWikidataQueryWithLetterWords.compare(
        "./TokenizedLetters/",
        "./NER-german/extractEntitiesFromWikidata/comparisonReligionOutput3.txt",
        queryReligion,
        80,
        False,
    )
    print("[INFO] Religion query ran")

    # # run location query
    # queryLocation = """
    # SELECT ?item ?itemLabel {
    #   {
    #   SELECT ?item ?itemLabel WHERE {
    #       { ?item wdt:P31 wd:Q6256 } # country
    #     UNION
    #       { ?item wdt:P31 wd:Q3624078 } # sovereign state
    #     UNION
    #       { ?item wdt:P31 wd:Q15974307 } # administrative unit of Germany
    #     UNION
    #       { ?item wdt:P31 wd:Q42744322 } # urban municipality of Germany (Stadt in Deutschland)
    #     UNION
    #       { ?item wdt:P31 wd:Q5119 } # capital city
    #     UNION
    #       { ?item wdt:P31 wd:Q15334 } # municipality of Poland
    #     UNION
    #       { ?item wdt:P31 wd:Q1093829 } # city in the United States

    #     SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }
    #     }
    #   }
    #   FILTER lang(?itemLabel) # removes item that have no label
    # }

    # # neustadt (prudnik) gesondert behandeln Q986984
    # """

    # location = compareWikidataQueryWithLetterWords.compare(
    #     "./TokenizedLetters/",
    #     "./NER-german/extractEntitiesFromWikidata/comparisonLocationOutput2.txt",
    #     queryLocation,
    #     90,
    #     False,
    # )
    # print("[INFO] Location query ran")

    # run food query
    queryFood = """
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

    food = compareWikidataQueryWithLetterWords.compare(
        "./TokenizedLetters/",
        "./NER-german/extractEntitiesFromWikidata/comparisonFoodOutput2.txt",
        queryFood,
        90,
        False,
    )
    print("[INFO] Food query ran")

    return [religion, food]
