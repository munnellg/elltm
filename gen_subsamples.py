import logging
import gensim
from docs import config
from optparse import OptionParser
from lib.corpora import gen_random_subsample_corpus, count_corpus_docs

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

# Build this program's option parser
def build_opt_parser():
    usage = "usage: %prog [options] <dictionary> <filename> [, <filename>, ...]"
    parser = OptionParser(usage=usage)

    parser.add_option("-r", "--reduction-factor", dest="reduction_factor",
                      default=config.default_reduction_rate, type="float",
                      help="Subsample rate for the collection"
    )

    parser.add_option("-n", "--num-subsamples", dest="num_subsamples",
                      default=config.default_num_subsamples, type="int",
                      help="The number of subsample collections to generate"
    )

    parser.add_option("-p", "--prefix", dest="prefix",
                      default=config.default_sample_prefix, type="string",
                      help="The prefix of the output files"
    )

    return parser

# Parse commandline arguments using OptionParser given
def parse_arguments(parser):
    (options, args) = parser.parse_args()
    
    if len(args) < 2:
        parser.print_help()
        exit()

    return options, args

# Main function
def main():

    parser = build_opt_parser()

    (options, args) = parse_arguments(parser)

    dictionary = gensim.corpora.Dictionary.load(args[0])

    ndocs = count_corpus_docs(args[1:])

    for i in range(0, options.num_subsamples):
        corpus = gen_random_subsample_corpus(args[1:], dictionary, ndocs, options.reduction_factor)
        gensim.corpora.MmCorpus.serialize("{}_{}_{}.mm".format(options.prefix, options.reduction_factor, i), corpus)

if __name__ == "__main__":
    main()
