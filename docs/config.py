# Codes for the different models that the script can generate
code_lda = "lda"
code_lsa = "lsa"
code_lsi = "lsi"

# Default values used by the script
default_num_topics = 2
default_dictionary_out = "out.dict"
default_model_out = "out.model"
default_model_type = code_lda

# Settings for stopword list
stop_word_list = 'english'
use_stop_word_list = True

# Settings for building the LDA model
lda_settings = {
    "distributed" : False, 
    "chunksize" : 2000, 
    "passes" : 1, 
    "update_every" : 1, 
    "alpha" : 'symmetric', 
    "eta" : None, 
    "decay" : 0.5, 
    "offset" : 1.0, 
    "eval_every" : 10, 
    "iterations" : 50, 
    "gamma_threshold" : 0.001, 
    "minimum_probability" : 0.01
}

# Settings for building an LSI model
lsi_settings = {
    "chunksize" : 20000,
    "decay" : 1.0,
    "distributed" : False,
    "onepass" : True, 
    "power_iters" : 2, 
    "extra_samples" : 100
}