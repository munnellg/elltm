import logging
import gensim
import math
import random
from docs import config
from optparse import OptionParser
from lib.corpora import load_subsample_vector_corpus, load_corpus

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

# Build this program's option parser
def build_opt_parser():
    usage = "usage: %prog [options] <dictionary> <filename> [, <filename>, ...]"
    parser = OptionParser(usage=usage)

    parser.add_option("-r", "--reduction-factor", dest="reduction_factor",
                      default=config.default_reduction_rate, type="float",
                      help="Subsample rate for the collection"
    )

    return parser

# Parse commandline arguments using OptionParser given
def parse_arguments(parser):
    (options, args) = parser.parse_args()
    
    if len(args) < 2:
        parser.print_help()
        exit()

    return options, args

def count_corpus_docs(files):
    corpus = load_corpus(files)

    ndocs = -1

    for ndocs, _ in enumerate(corpus):
        pass

    return ndocs + 1

def get_subsample_corpus(files, dictionary, ndocs, reduction_factor):

    nselected = int(math.ceil(ndocs*reduction_factor))

    selection_array = ([1]*nselected) + ([0]*(ndocs - nselected))
    
    random.shuffle(selection_array)

    logging.info("Adding {}/{} random docs to subsample".format(nselected, ndocs))

    corpus = load_subsample_vector_corpus(files, dictionary, selection_array)

    return corpus

# Main function
def main():

    parser = build_opt_parser()

    (options, args) = parse_arguments(parser)

    dictionary = gensim.corpora.Dictionary.load(args[0])

    ndocs = count_corpus_docs(args[1:])

    corpus = get_subsample_corpus(args[1:], dictionary, ndocs, options.reduction_factor)

    gensim.corpora.MmCorpus.serialize("subsample.mm", corpus)

if __name__ == "__main__":
    main()
