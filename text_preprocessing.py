import re
from nltk.stem import PorterStemmer

text = ("Today is sunny. She is a sunny girl. To be or not to be. "
        "She is in Berlin today. Sunny Berlin! Berlin is always exciting!")

stopwords = {"was", "is", "in", "to", "be"}


def standard_tokenize(text):
    return re.findall(r"[A-Za-z0-9]+", text)


def whitespace_tokenize(text):
    return text.split()


def remove_stopwords(tokens):
    return [word for word in tokens if word not in stopwords]


# Part (a)
standard = standard_tokenize(text)
whitespace = whitespace_tokenize(text)

print("Part (a)")
print("StandardTokenizer:", standard)
print("WhitespaceTokenizer:", whitespace)


# Part (b)
filtered = remove_stopwords(standard)

print("\nPart (b)")
print("After StopwordFilter:", filtered)


# Part (c)
tokens = [word.lower() for word in standard]
tokens = remove_stopwords(tokens)

stemmer = PorterStemmer()
result = [stemmer.stem(word) for word in tokens]

print("\nPart (c)")
print("After Analyzer:", result)