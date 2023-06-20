from fuzzywuzzy import fuzz
from fuzzywuzzy import process

print(fuzz.ratio("Deutschlä", "Deutschland"))
print(fuzz.partial_ratio("D", "Deutschland"))


choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
print(process.extract("new york jets", choices, limit=2))
print(process.extractOne("cowboys", choices))
