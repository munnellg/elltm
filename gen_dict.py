import logging
from docs import config
from optparse import OptionParser
from lib.corpora import gen_dictionary, load_corpus

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

# Build this program's option parser
def build_opt_parser():
    usage = "usage: %prog [options] <filename> [, <filename>, ...]"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--dictionary-out", dest="dict_out",
                      default=config.default_dictionary_out, metavar="FILE",
                      help="Output file for the dictionary generated from input files"
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

    corpus = load_corpus(args)
    
    dictionary = gen_dictionary(corpus)

    dictionary.save(options.dict_out)

if __name__ == "__main__":
    main()
