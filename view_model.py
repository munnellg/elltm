import sys
import logging
import gensim
from lib import tokenizer

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

def get_model_load_function(fname):
    # Model type should be stated in the first line of the file
    with open(fname, "r") as f:
        head = next(f)

    # Check to see if we've found one of the headers we expect
    if head.find("gensim.models.lsimodel") > 0:
        return gensim.models.lsimodel.LsiModel.load
    elif head.find("gensim.models.ldamodel") > 0:
        return gensim.models.ldamodel.LdaModel.load
    else:
        return None

def load_model(fname):
    load = get_model_load_function(fname)

    model = load(fname)

    return model

def process_query(query, model, dictionary):
    tokens = tokenizer.tokenize(query)    
    print dictionary.doc2bow(tokens)

if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print "Usage: view_model.py <dictionary> <model>"
        exit()

    dictionary = gensim.corpora.dictionary.Dictionary.load(sys.argv[1])
    model = load_model(sys.argv[2])

    model.print_topics(model.num_topics)

#    user_input = raw_input(">>> ")

#    process_query(user_input, model, dictionary)
