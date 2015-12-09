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

    parser.add_option("-m", "--min-reduction-factor", dest="min_reduction_factor",
                      default=config.default_min_reduction_rate, type="float",
                      help="Subsample rate for the collection"
    )

    parser.add_option("-M", "--max-reduction-factor", dest="max_reduction_factor",
                      default=config.default_max_reduction_rate, type="float",
                      help="Subsample rate for the collection"
    )

    parser.add_option("-s", "--step", dest="step",
                      default=config.default_reduction_step, type="float",
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

def drange(start, stop, step):
    r = start
    while r< stop:
        yield r
        r += step

# Main function
def main():

    parser = build_opt_parser()

    (options, args) = parse_arguments(parser)

    dictionary = gensim.corpora.Dictionary.load(args[0])

    ndocs = count_corpus_docs(args[1:])

    for i in drange(options.min_reduction_factor, options.max_reduction_factor, options.step):
        for j in range(0, options.num_subsamples):
            corpus = gen_random_subsample_corpus(args[1:], dictionary, ndocs, i)
            gensim.corpora.MmCorpus.serialize("{}_{}_{}.mm".format(options.prefix, i, j), corpus)

if __name__ == "__main__":
    main()
