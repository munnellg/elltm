import logging
import gensim
from docs import config
from optparse import OptionParser
from lib.corpora import load_vector_corpus

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

# Build this program's option parser
def build_opt_parser():
    usage = "usage: %prog [options] <dictionary> <filename> [, <filename>, ...]"
    parser = OptionParser(usage=usage)

    parser.add_option("-c", "--corpus-out", dest="corpus_out",
                      default=config.default_corpus_out, metavar="FILE",
                      help="Output file for the corpus generated from input files"
    )

    return parser

# Parse commandline arguments using OptionParser given
def parse_arguments(parser):
    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        parser.print_help()
        exit()

    return options, args

# Main function
def main():
    parser = build_opt_parser()

    (options, args) = parse_arguments(parser)

    dictionary = gensim.corpora.Dictionary.load(args[0])

    corpus = load_vector_corpus(args[1:], dictionary)
    
    gensim.corpora.MmCorpus.serialize(options.corpus_out, corpus)

if __name__ == "__main__":
    main()
