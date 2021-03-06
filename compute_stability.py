import sys
import logging
import gensim
from optparse import OptionParser
from docs import config
from lib.models import load_model
from lib.metrics import get_model_agreement

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

# Build this program's option parser
def build_opt_parser():
    usage = "usage: %prog [options] <gold> <model> [, <model>...]"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--depth", dest="depth",
                      default=config.default_compare_depth, type="int",
                      help="The depth to which topics should be considered for similarity"
                  )

    return parser

# Parse commandline arguments using OptionParser given
def parse_arguments(parser):
    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.print_help()
        exit()

    return options, args

# Compare two models to assess how similar they are based on the
# contents of their topics
def compare_models(f1, f2, depth):
    # Load the models passed as arguments
    model1 = load_model(f1)
    model2 = load_model(f2)

#    topic_pairs = get_similar_topics(model1, model2, depth)

#    logging.info("Assigned the following topic pairs: {}".format(topic_pairs))
    # Measure their agreement
    agreement = get_model_agreement(model1, model2, depth)

    # Display the result
    logging.info("{} & {} Agreement: {}".format(f1, f2, agreement))

    return agreement

def compute_stability(gold, models, depth):
    average = 0

    for model in models:
        average += compare_models(gold, model, depth)

    return average/len(models)

# Main function. Entry point for program
def main():
    parser = build_opt_parser()
    (options, args) = parse_arguments(parser)

    stability = compute_stability(args[0], args[1:], options.depth)
    logging.info("Stability: {}".format(stability))
    sys.stdout.write("{}".format(stability))

if __name__ == "__main__":
    main()
