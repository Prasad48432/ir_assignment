import lucene
from org.apache.pylucene.analysis import PythonAnalyzer

from java.io import StringReader
from org.apache.lucene.analysis import Analyzer
from org.apache.lucene.analysis.standard import StandardTokenizer
from org.apache.lucene.analysis.core import (
    WhitespaceTokenizer,
    LowerCaseFilter,
    StopFilter,
)
from org.apache.lucene.analysis.en import PorterStemFilter
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.lucene.analysis import CharArraySet


# Initialize Java Virtual Machine
lucene.initVM()

# Assignment input
TEXT = (
    "Today is sunny. She is a sunny girl. To be or not to be. "
    "She is in Berlin today. Sunny Berlin! Berlin is always exciting!"
)

STOPWORDS = ["was", "is", "in", "to", "be"]


def get_tokens(stream):
    """Extract tokens from a Lucene TokenStream."""
    term_attribute = stream.addAttribute(CharTermAttribute.class_)
    tokens = []

    stream.reset()

    while stream.incrementToken():
        tokens.append(str(term_attribute))

    stream.end()
    stream.close()

    return tokens


def tokenize(tokenizer):
    """Run a tokenizer on the assignment text."""
    tokenizer.setReader(StringReader(TEXT))
    return get_tokens(tokenizer)


# --------------------------------------------------
# PART (a): StandardTokenizer vs WhitespaceTokenizer
# --------------------------------------------------

standard_tokens = tokenize(StandardTokenizer())
whitespace_tokens = tokenize(WhitespaceTokenizer())

print("\nPART (a) - TOKENIZERS")

print("\nStandardTokenizer:")
print(standard_tokens)

print("\nWhitespaceTokenizer:")
print(whitespace_tokens)


# --------------------------------------------------
# PART (b): StandardTokenizer + StopFilter
# --------------------------------------------------

stop_set = CharArraySet(len(STOPWORDS), False)

for word in STOPWORDS:
    stop_set.add(word)

tokenizer = StandardTokenizer()
tokenizer.setReader(StringReader(TEXT))

stop_filter = StopFilter(tokenizer, stop_set)
part_b_tokens = get_tokens(stop_filter)

print("\nPART (b) - STOPWORD FILTER")

print("Stopwords:", STOPWORDS)
print("Output:")
print(part_b_tokens)


# --------------------------------------------------
# PART (c): Custom Lucene Analyzer
# StandardTokenizer -> LowerCaseFilter
# -> StopFilter -> PorterStemFilter
# --------------------------------------------------

class AssignmentAnalyzer(PythonAnalyzer):

    def __init__(self):
        PythonAnalyzer.__init__(self)

    def createComponents(self, fieldName):
        source = StandardTokenizer()

        token_filter = LowerCaseFilter(source)
        token_filter = StopFilter(token_filter, stop_set)
        token_filter = PorterStemFilter(token_filter)

        return Analyzer.TokenStreamComponents(source, token_filter)


analyzer = AssignmentAnalyzer()

stream = analyzer.tokenStream("content", StringReader(TEXT))
part_c_tokens = get_tokens(stream)

print("\nPART (c) - COMPLETE ANALYZER")

print("Pipeline: StandardTokenizer -> LowerCaseFilter")
print("        -> StopFilter -> PorterStemFilter")

print("Output:")
print(part_c_tokens)

analyzer.close()

print("\nP01 processing completed.")