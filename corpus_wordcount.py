import logging
import gensim
from docs import config
from optparse import OptionParser
from lib.corpora import corpus_word_count

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

# Build this program's option parser
def build_opt_parser():
    usage = "usage: %prog [options] <dictionary> <filename> [, <filename>, ...]"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--dictionary", dest="dictionary",
                      default=None,
                      help="Optional dictionary parameter for parsing MM corpus files"
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
    
    dictionary = gensim.corpora.Dictionary.load(options.dictionary) if options.dictionary else options.dictionary

    word_count = corpus_word_count(args, dictionary)

    logging.info("Word Count: {}".format(word_count))

if __name__ == "__main__":
    main()
