import nltk
import sys
import os
import string
from collections import Counter
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    return_dict = {}
    for file in os.listdir(directory):
        filename = file.split('.')[0]
        with open(f"corpus/{file}" , encoding="utf8") as myfile:
            contents = myfile.read()
            return_dict[filename] = contents

    return return_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    new_document = document.translate(str.maketrans('', '', string.punctuation))
    list = nltk.word_tokenize(new_document)
    stop_words = nltk.corpus.stopwords.words("english")

    finallist = [x.lower() for x in list if x not in stop_words]

    return finallist


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Recall that the inverse document frequency of a word is defined by taking the natural logarithm of the number of documents divided by the number of documents in which the word appears.
    word_list = []
    return_dict = {}

    for document in documents:
        word_list.append(list(set(documents[document])))
    
    counter = Counter(word_list[0])

    for word in counter:
        return_dict[word] = math.log(len(documents)) / counter[word]

    return return_dict

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
#     Files should be ranked according to the sum of tf-idf values for any word in the query that also appears in the file. Words in the query that do not appear in the file should not contribute to the file’s score.
# Recall that tf-idf for a term is computed by multiplying the number of times the term appears in the document by the IDF value for that term.
    score_dict = {}
    for file in files:
        total_score = 0
        for word in query:
            total_score += file.count(word)* idfs[word]
        score_dict[file] = total_score
    
    sorted_list = [k for k in sorted(score_dict.items(), key=lambda item: item[1])]

    return sorted_list[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    score_dict = {}
    for sentence in sentences:
        total_score = 0
        for word in query:
            total_score += sentence.count(word)* idfs[word]
        score_dict[sentence] = total_score
    
    sorted_list = [k for k in sorted(score_dict.items(), key=lambda item: item[1])]

    return sorted_list[:n]


if __name__ == "__main__":
    main()
