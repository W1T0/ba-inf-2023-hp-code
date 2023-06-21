from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# print(fuzz.ratio("Deutschlä", "Deutschland"))
# print(fuzz.partial_ratio("D", "Deutschland"))

# print(fuzz.ratio("Dallas Cowboys", "cowboys"))

# choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
# # print(process.extract("new york jets", choices, limit=2))
# print(process.extractOne("cowboys", choices))


choices2 = {
    "Atlanta Falcons": 1,
    "New York Jets": 2,
    "New York Giants": 3,
    "Dallas Cowboys": 4,
}

choices3 = {}

choices3["test"] = 2

print(choices3)
