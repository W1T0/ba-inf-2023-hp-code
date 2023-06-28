import extractReligionWordsFromWikidata
import extractLocationsWordsWithWikidata
import extractFoodWordsWithWikidata


def run():
    # run religion
    religion = extractReligionWordsFromWikidata.run(
        "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/",
        "./NER-german/extractEntitiesFromWikidata/comparisonReligionOutput3.txt",
        80,
        False,
    )
    print("[INFO] Religion query ran")

    # run location
    location = extractLocationsWordsWithWikidata.run(
        "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/",
        "./NER-german/extractEntitiesFromWikidata/comparisonLocationOutput2.txt",
        90,
        False,
    )
    print("[INFO] Location query ran")

    # run food
    food = extractFoodWordsWithWikidata.run(
        "D:/Hannes/Dokumente/Dokumente/Uni/Bachelorarbeit/Code/Annotationen/Stichprobe - Annotationen - Export/",
        "./NER-german/extractEntitiesFromWikidata/comparisonFoodOutput2.txt",
        90,
        False,
    )
    print("[INFO] Food query ran")

    return [religion, location, food]
