# function that replaces special characters
def replace(word):
    newWord = (
        word.replace(",", "")
        .replace(".", "")
        .replace("¬", "")
        .replace("?", "")
        .replace(":", "")
        .replace(";", "")
        .replace("-", "")
        .replace("!", "")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "")
    )

    return newWord
