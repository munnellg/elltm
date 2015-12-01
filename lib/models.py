import gensim

# Determine the type of model contained in a file by checking the head
# of the file. Returns None if unable to determine file
# type. Otherwise returns a pointer to the appropriate function to
# load the model
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

# Load a model from a file into memory using the appropriate load
# function
def load_model(fname):
    # Determine the load function required
    load = get_model_load_function(fname)

    # Load and return the model
    return load(fname)
