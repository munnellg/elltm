import sys
import logging
import gensim
from docs import config
from lib.metrics import build_similarity_matrix

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

if __name__ == "__main__":
    
    matches = []

    if len(sys.argv) < 3:
        print "Usage: compare_models.py <model1> <model2>"
        exit()

    model1 = load_model(sys.argv[1])
    model2 = load_model(sys.argv[2])

    matrix = build_similarity_matrix(model1, model2, config.similarity_depth)

    for i in matrix:
        matches.append(i.index(max(i)))

    for i in range(0, len(matches)):
        print("Topic M1 {} | Topic M2 {} | Score: {}".format(i, matches[i], matrix[i][matches[i]]))
    
