import nltk
import re
import sys
import logging
import gensim
from optparse import OptionParser

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

code_lda = "lda"
code_lsa = "lsa"
code_lsi = "lsi"

default_num_topics = 2
default_dictionary_out = "out.dict"
default_model_out = "out.model"
default_model_type = code_lda

def build_opt_parser():
    usage = "usage: %prog [options] <filename> [, <filename>, ...]"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--dictionary-out", dest="dict_out",
                      default=default_dictionary_out, metavar="FILE",
                      help="Output file for the dictionary generated from corpus"
                  )
    parser.add_option("-m", "--model-out", dest="model_out",
                      default=default_model_out, metavar="FILE",
                      help="Output file for the model generated from corpus"
                  )
    parser.add_option("-M", "--model-type", dest="model_type",
                      default=default_model_type,
                      help="The type of model the program should produce. Valid inputs are lsa, lsi, lda"
    )
    parser.add_option("-t", "--num-topics", dest="num_topics",
                      default=default_num_topics,
                      help="The number of topics under which the program should attempt to group the corpus"
    )

    return parser

def parse_arguments(parser):
    (options, args) = parser.parse_args()

    if options.model_type not in (code_lsa, code_lsi, code_lda):
        print ( "Invalid model type \"{}\". Reverting to default {}".format(options.model_type, default_model_type) )
        options.model_type = default_model_type

    if len(args) < 1:
        parser.print_help()
        exit()

    return options, args

# Load file contents and return as array of lines
def load_line_corpus(fname):
    contents = [line.strip() for line in open(fname, "r") if len(line.strip()) > 0]
    return contents

def load_file(fname):
    with open(fname, "r") as f:
        return f.read()

def load_corpus(fnames):
    if len(fnames) == 1:
        corpus = load_line_corpus(fnames[0])
    else:
        corpus = [load_file(fname) for fname in fnames]

    return corpus

# tokenize input string into words and remove stopwords
def tokenize(text):
    aposeq = r"[`='\(\)_]+|[!.\?\*:,]"

    no_mark = re.sub(aposeq, '', text)
    stopwords = set(nltk.corpus.stopwords.words('english'))
    return [word.lower().encode('utf-8') for word in nltk.tokenize.word_tokenize(no_mark.decode('utf-8')) if word.lower().encode('utf-8') not in stopwords ]

# Tokenize an array of strings that represents our corpus
def tokenize_corpus(corpus):
    return [tokenize(document) for document in corpus]

# Generate and return a dictionary. Also saves dictionary to file
def gen_dictionary(tokens, dict_out):

    dictionary = gensim.corpora.dictionary.Dictionary()
    dictionary.add_documents(tokens)
    dictionary.save(dict_out)

    return dictionary

# Convert tokenized corpus to vector format using dictionary
def vectorize_corpus(corpus, dictionary):
    return [ dictionary.doc2bow(document) for document in corpus ]
   
def gen_lda_model(vectors, dictionary, model_out, num_topics):
    lda = gensim.models.ldamodel.LdaModel(
        corpus=vectors,
        id2word=dictionary,
        num_topics=num_topics,
        update_every=0,
        passes=20
    )

    lda.save(model_out)

    return lda

def gen_lsi_model(vectors, dictionary, model_out, num_topics):
    lsi = gensim.models.lsimodel.LsiModel(
        vectors, 
        id2word=dictionary, 
        num_topics=num_topics
    )

    lsi.save(model_out)

    return lsi

def gen_model(model_type, vectors, dictionary, model_out, num_topics):
    if model_type == code_lsi or model_type == code_lsa:
        return gen_lsi_model(vectors, dictionary, model_out, num_topics)
    elif model_type == code_lda:
        return gen_lda_model(vectors, dictionary, model_out, num_topics)

if __name__ == "__main__":

    parser = build_opt_parser()

    (options, args) = parse_arguments(parser)
    
    corpus = load_corpus(args)
    tokens = tokenize_corpus(corpus)
    
    dictionary = gen_dictionary(tokens, options.dict_out)

    vectors = vectorize_corpus(tokens, dictionary)

    model = gen_model(options.model_type, vectors, dictionary, options.model_out, options.num_topics)