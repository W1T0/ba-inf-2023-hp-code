import os
from fuzzywuzzy import fuzz, process
import B_wikidataSPARQLQuery


def compare(directoryPath, outputPath, query, levenshteinDistance, boolWriteToFile):
    """
    Compares every result of a SPARQL query with every word in the letters.
    Letters must be in ??? (conll or tsv) format?

    directoryPath: The path of the directory where the files are stored in.
    outputPath: The path of the file where the output should be stored in.
    query: The Wikidata query.
    levenshteinDistance: The Levenshtein-Distance. A metric to compare the differences between two strings.
    boolWriteToFile: A boolean value that determines if the result of this function should be written to the output file. (True or False)
    """

    # run query and save as dataframe
    data_extracter = B_wikidataSPARQLQuery.WikiDataQueryResults(query)
    queryDF = data_extracter.load_as_dataframe()
    print("[INFO] Query ran")

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
            print("[INFO] " + str(counter) + " Files opened")

            # write filename
            if boolWriteToFile:
                writeToFile.write("FILE: " + filename + "\n")

            # store filename
            results.append([filename.replace(".txt", "").replace("_", "-")])

            # temporary storage of best matches
            tempBestMatch = []

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
                        # store query results with fuzz.ratio > levenshteinDistance
                        possibleMatch = []

                        # store match and link in dict
                        possibleMatchAndLink = {}

                        # iterate over labels in query result
                        for label in queryDF.itemLabel:
                            # compare firstWord and label with fuzzywuzzy
                            if fuzz.ratio(firstWord, label) > levenshteinDistance:
                                # add label to possible match list
                                possibleMatch.append(label)

                                # get wikidata link and check if there are more than one link
                                if (
                                    queryDF.loc[
                                        (queryDF.itemLabel == label)
                                    ].item.shape[0]
                                    > 1
                                ):
                                    # if there are more than one link, choose the first one
                                    wikidataLink = (
                                        queryDF.loc[(queryDF.itemLabel == label)]
                                    ).values[0, 0]
                                else:
                                    # get link from dataframe
                                    wikidataLink = queryDF.loc[
                                        (queryDF.itemLabel == label)
                                    ].item.item()

                                # add link to dict
                                possibleMatchAndLink[label] = wikidataLink

                        # make sure that there are matches in the list
                        if len(possibleMatch) > 0:
                            # print("[INFO] possibleMatch: " + str(possibleMatch))
                            # get the label with the highest fuzz.ratio
                            bestMatch = process.extractOne(firstWord, possibleMatch)
                            # print(
                            #     "[INFO] firstWord "
                            #     + firstWord
                            #     + " | bestMatch: "
                            #     + str(bestMatch)
                            # )

                            # write the best match to file
                            if boolWriteToFile:
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

                            # store best match
                            tempBestMatch.append(
                                firstWord
                                + " "
                                + str(possibleMatchAndLink[bestMatch[0]])
                            )

            # remove duplicates
            tempBestMatchDistinct = [*set(tempBestMatch)]

            # add best matches to results list
            if len(tempBestMatchDistinct) > 0:
                for bestMatch in tempBestMatchDistinct:
                    results[counter - 1].append(bestMatch)

            # add line break
            if boolWriteToFile:
                writeToFile.write("\n")

    # close file
    if boolWriteToFile:
        writeToFile.close()

    # return results list
    return results
