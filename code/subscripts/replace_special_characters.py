# function that replaces special characters
def replace(word):
    """
    Replaces special characters of a word.
    These are:
    ,
    .
    ¬
    ?
    :
    ;
    -
    !
    (
    )
    /
    """

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
