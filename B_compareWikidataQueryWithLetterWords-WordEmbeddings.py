import os
from fuzzywuzzy import fuzz, process
import B_wikidataSPARQLQuery
import B_replaceSpecialCharacters
import gensim
import math
from sklearn.decomposition import PCA


# get trained model
# used KeyedVectors.load_word2vec_format instead of  Word2Vec.load_word2vec_format because of deprecation
model = gensim.models.KeyedVectors.load_word2vec_format(
    "D:\\Hannes\\Dokumente\\Dokumente\\Uni\\Bachelorarbeit\\Word Embeddings\\german.model", binary=True
)


def wordEmbeddingCompare(words, threshold):
    # print(words)

    vectors = [model[word] for word in words]

    pca = PCA(n_components=2, whiten=True)
    vectors2d = pca.fit(vectors).transform(vectors)

    for i in range(0, len(words) - 1, 2):
        a = vectors2d[i][0]
        b = vectors2d[i][1]
        c = vectors2d[i + 1][0]
        d = vectors2d[i + 1][1]

        if math.dist([a, b], [c, d]) < threshold:
            print(words[i] + " - " + words[i + 1])
            print(str(math.dist([a, b], [c, d])))


def compare(directoryPath, query, threshold, outputPath, boolWriteToFile):
    """
    Compares every result of a SPARQL query with every word in the letters.
    Letters must be tokenized.

    directoryPath: The path of the directory where the files are stored in.
    query: The Wikidata query.
    distance: the distance between the words as defined by the functionality of word embeddings
    outputPath: The path of the file where the output should be stored in.
    boolWriteToFile: A boolean value that determines if the result of this function should be written to the output file. (True or False)
    """

    # run query and save as dataframe
    data_extracter = B_wikidataSPARQLQuery.WikiDataQueryResults(query)
    queryDF = data_extracter.load_as_dataframe()

    # open file to write to
    if boolWriteToFile:
        writeToFile = open(outputPath, "a", encoding="utf-8")

    # count files
    counter = 0

    # list to save the filename and the best matches
    results = []

    # for every file in the directory which ends with .txt
    for file in os.listdir(directoryPath):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            counter += 1

            # open one letter
            letterFile = open(directoryPath + filename, "r", encoding="utf-8")
            print("[INFO] " + str(counter) + " Files opened: " + filename)

            # write filename
            if boolWriteToFile:
                writeToFile.write("FILE: " + filename + "\n")

            # store filename
            results.append([filename.replace(".txt", "").replace("_", "-")])

            # temporary storage of best matches
            tempBestMatch = []

            # stores every line of file
            lines = letterFile.readlines()

            # store every upper words
            upperWords = []

            for line in lines:
                # split the lines
                lineSplit = line.split()

                if lineSplit:
                    # get the first word
                    firstWord = B_replaceSpecialCharacters.replace(lineSplit[0])

                    # check if there is a word
                    if firstWord:
                        # check if first word is noun (upper case)
                        if firstWord[0].isupper():
                            # saves word to list
                            upperWords.append(firstWord)

            # print(upperWords)

            # add upperWords and query results to one list
            words = []

            for word in upperWords:
                for label in queryDF.itemLabel:
                    if " " not in label:
                        words.append(word.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue"))
                        words.append(label.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue"))

            wordEmbeddingCompare(words, threshold)

    # close file
    if boolWriteToFile:
        writeToFile.close()

    # return results list
    return results


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


compare(
    "./TokenizedLetters/",
    query,
    0.05,
    "./NER-german/extractEntitiesFromWikidata/comparisonLocation-1.txt",
    False,
)
