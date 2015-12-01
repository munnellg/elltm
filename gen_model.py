import sys
import logging
import gensim
from optparse import OptionParser
from docs import config

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

# Build this program's option parser
def build_opt_parser():
    usage = "usage: %prog [options] <filename> [, <filename>, ...]"
    parser = OptionParser(usage=usage)
    parser.add_option("-m", "--model-out", dest="model_out",
                      default=config.default_model_out, metavar="FILE",
                      help="Output file for the model generated from corpus"
                  )
    parser.add_option("-M", "--model-type", dest="model_type",
                      default=config.default_model_type,
                      help="The type of model the program should produce. Valid inputs are lsa, lsi, lda"
    )
    parser.add_option("-t", "--num-topics", dest="num_topics",
                      default=config.default_num_topics, type="int",
                      help="The number of topics under which the program should attempt to group the corpus"
    )

    return parser

# Parse commandline arguments using OptionParser given
def parse_arguments(parser):
    (options, args) = parser.parse_args()
    
    options.model_type = options.model_type.lower()

    if options.model_type not in (config.code_lsa, config.code_lsi, config.code_lda):
        logging.warning( "Invalid model type \"{}\". Reverting to default \"{}\"".format(options.model_type, config.default_model_type) )
        options.model_type = config.default_model_type

    if len(args) < 2:
        parser.print_help()
        exit()

    return options, args

# Generates and LDA model using dictionary and vectors passed as arguments. Writes model to file
def gen_lda_model(corpus, dictionary, model_out, num_topics):
    lda = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        **config.lda_settings
    )

    lda.save(model_out)

    return lda

# Generates and LSI model using dictionary and vectors passed as arguments. Writes model to file
def gen_lsi_model(corpus, dictionary, model_out, num_topics):
    lsi = gensim.models.lsimodel.LsiModel(
        corpus=corpus, 
        id2word=dictionary, 
        num_topics=num_topics,
        **config.lsi_settings
    )

    lsi.save(model_out)

    return lsi

# Generates the type of model selected using the information passed as arguments
def gen_model(model_type, corpus, dictionary, model_out, num_topics):
    if model_type == config.code_lsi or model_type == config.code_lsa:
        return gen_lsi_model(corpus, dictionary, model_out, num_topics)
    elif model_type == config.code_lda:
        return gen_lda_model(corpus, dictionary, model_out, num_topics)

# Main function
def main():
    parser = build_opt_parser()

    (options, args) = parse_arguments(parser)

    dictionary = gensim.corpora.Dictionary.load(args[0])
    corpus = gensim.corpora.MmCorpus(args[1])

    model = gen_model(options.model_type, corpus, dictionary, options.model_out, options.num_topics)

if __name__ == "__main__":
    main()
