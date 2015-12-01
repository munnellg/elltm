import sys
import logging
import gensim
from optparse import OptionParser
from docs import config
from lib.models import load_model

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

# Build this program's option parser
def build_opt_parser():
    usage = "usage: %prog [options] <model>"
    parser = OptionParser(usage=usage)

    parser.add_option("-t", "--num-terms", dest="num_terms",
                      default=config.default_display_depth, type="int",
                      help="The number of terms to be displayed per topic in the model"
    )

    return parser

# Parse commandline arguments using OptionParser given
def parse_arguments(parser):
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        exit()

    return options, args

def view_model(fname, num_terms):
    model = load_model(fname)

    logging.info("{} Topics".format(model.num_topics))
    model.print_topics(model.num_topics, num_words=num_terms)

# Main function. Entry point for program
def main():
    parser = build_opt_parser()
    (options, args) = parse_arguments(parser)

    view_model(args[0], options.num_terms)

if __name__ == "__main__":
    main()
