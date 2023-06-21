import os
from fuzzywuzzy import fuzz, process
import testWikidataSPARQLQuery


# function to compare results of a SPARQL query (queryDF) with every word in the letters located in the directoryPath, letters must be in conll format
def compare(directoryPath, outputPath, query):
    # run query and save as dataframe
    data_extracter = testWikidataSPARQLQuery.WikiDataQueryResults(query)
    queryDF = data_extracter.load_as_dataframe()
    print("[INFO] Query ran")

    # print(queryDF)

    # print(queryDF.loc[(queryDF.itemLabel == "Gurke")].item.shape[0])
    # print((queryDF.loc[(queryDF.itemLabel == "Gurke")]).values[2, 0])

    # open file to write to
    writeToFile = open(outputPath, "a", encoding="utf-8")

    # count files
    counter = 0

    # for every file in the directory which ends with .txt
    for file in os.listdir(directoryPath):
        filename = os.fsdecode(file)
        if filename.endswith(".conll"):
            counter += 1

            # open one letter
            letterFile = open(directoryPath + filename, "r", encoding="utf-8")
            print("[INFO] " + str(counter) + " Files opened")

            # write filename
            writeToFile.write("FILE: " + filename + "\n")

            # stores every line of file
            lines = letterFile.readlines()

            for line in lines:
                # split the lines
                lineSplit = line.split()

                if lineSplit:
                    # get the first word
                    firstWord = lineSplit[0]

                    # check if first word is noun (upper case)
                    if firstWord[0].isupper():
                        # store query results with fuzz.ratio > 90
                        possibleMatch = []
                        possibleMatchAndLink = {}

                        # iterate over labels in query result
                        for label in queryDF.itemLabel:
                            # compare firstWord and label with fuzzywuzzy
                            if fuzz.ratio(firstWord, label) > 90:
                                possibleMatch.append(label)
                                # get wikidata link
                                if (
                                    queryDF.loc[
                                        (queryDF.itemLabel == label)
                                    ].item.shape[0]
                                    > 1
                                ):
                                    wikidataLink = (
                                        queryDF.loc[(queryDF.itemLabel == label)]
                                    ).values[0, 0]
                                else:
                                    wikidataLink = queryDF.loc[
                                        (queryDF.itemLabel == label)
                                    ].item.item()
                                possibleMatchAndLink[label] = wikidataLink

                        # make sure that there are matches in the list
                        if len(possibleMatch) > 0:
                            print("[INFO] possibleMatch: " + str(possibleMatch))
                            # get the label with the highest fuzz.ratio
                            bestMatch = process.extractOne(firstWord, possibleMatch)
                            print(
                                "[INFO] firstWord "
                                + firstWord
                                + " | bestMatch: "
                                + str(bestMatch)
                            )

                            # write the best match to file
                            writeToFile.write(
                                "Word: "
                                + firstWord
                                + " | Label: "
                                + str(bestMatch[0])
                                + " | Link: "
                                + str(possibleMatchAndLink[bestMatch[0]])
                                + " | "
                                + str(fuzz.ratio(firstWord, bestMatch[0]))
                                + "\n"
                            )

            # add line break
            writeToFile.write("\n")

    # close file
    writeToFile.close()
