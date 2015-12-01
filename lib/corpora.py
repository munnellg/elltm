import gensim 
import logging
import random
import bz2
from lib import tokenizer

class LineCorpus(object):

    def __init__(self, ifile):
        self.ifile = ifile

    def __iter__(self):
        for line in open(self.ifile, "r"):
            yield tokenizer.tokenize(line)

class DocumentCorpus(object):

    def __init__(self, ifiles):
        self.ifiles = ifiles

    def __iter__(self):
        for f in self.ifiles:
            with open(f, "r") as document:
                yield tokenizer.tokenize(document.read())

class CompressedCorpus(object):

    def __init__(self, ifile):
        self.ifile = ifile

    def __iter__(self):
        for line in bz2.BZ2File(self.ifile, 'r'):
            yield tokenizer.tokenize(line)

class SubsampleCorpus(object):

    def __init__(self, corpus_reader, selection_factor):
        self.corpus_reader = corpus_reader
        self.selection_factor = selection_factor
        self.idx = -1

    def __iter__(self):
        for doc in self.corpus_reader:
            self.idx += 1
            if self.selection_factor[self.idx] == 0:
                continue
            yield doc

class VectorCorpus(object):

    def __init__(self, corpus_reader, dictionary):
        self.corpus_reader = corpus_reader
        self.dictionary = dictionary

    def __iter__(self):
        for doc in self.corpus_reader:
            yield self.dictionary.doc2bow(doc)

def load_subsample_corpus(fnames, selection_factor):
    reader = load_corpus(fnames)

    return SubsampleCorpus(reader, selection_factor)

def load_subsample_vector_corpus(fnames, dictionary, selection_factor):
    subsample = load_subsample_corpus(fnames, selection_factor)
    return VectorCorpus(subsample, dictionary)

def load_vector_corpus(fnames, dictionary):
    reader = load_corpus(fnames)

    return VectorCorpus(reader, dictionary)

# Loads corpus as line corpus if fnames has one element, otherwise as
# document corpus
def load_corpus(fnames):
    if len(fnames) == 1:
        if fnames[0].lower().endswith(".bz2"):
            logging.info("Loading as compressed line corpus")
            corpus = CompressedCorpus(fnames[0])
        else:
            logging.info("Loading as line corpus")
            corpus = LineCorpus(fnames[0])
    else:
        logging.info("Loading as document corpus")
        corpus = DocumentCorpus(fnames)

    return corpus

# Generate and return a dictionary. Also saves dictionary to file
def gen_dictionary(corpus):
    dictionary = gensim.corpora.dictionary.Dictionary(corpus)
    return dictionary
