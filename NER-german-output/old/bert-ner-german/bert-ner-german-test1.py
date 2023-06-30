from transformers import pipeline

classifier = pipeline("ner", model="fhswf/bert_de_ner")
classifier(
    "Von der Organisation „medico international“ hieß es, die EU entziehe sich seit vielen Jahren der Verantwortung für die Menschen an ihren Außengrenzen."
)
