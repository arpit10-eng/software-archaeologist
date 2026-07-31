import nltk

paragraph = """
Natural Language Processing is a branch of artificial intelligence.
It helps computers understand human language and analyze text efficiently.
"""

# Tokenize words
words = nltk.word_tokenize(paragraph)

# Perform POS tagging
pos_tags = nltk.pos_tag(words)

print("POS Tags:")
print(pos_tags)




# import spacy

# # Load the English language model
# nlp = spacy.load("en_core_web_sm")

# sentence = "The students are learning Python and building machine learning models."

# # Process the sentence
# doc = nlp(sentence)

# # Extract verbs
# verbs = []

# for token in doc:
#     if token.pos_ == "VERB" or token.pos_ == "AUX":
#         verbs.append(token.text)

# print("Verbs found:")
# print(verbs)