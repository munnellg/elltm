Examining LSA and LDA Topic Models (ELLTM)
==========================================

These are a few scripts for the generation, examination and comparison
of LSA and LDA models. The current iteration works entirely in system
memory. This is something that we will be looking to rectify in the
near future so that these tests can be applied to large corpora such
as Wikipedia. A brief summary of the scripts provided and their
functionality are described below, although their use should be fairly
obvious from their names.

gen_model.py
------------

Takes as input one or more text files and generates either an LSA or
an LDA model from them. Command line arguments allow you to select the
type of model (LDA by default), number of topics (2 by default) and
name the output dictionary and model files (out.dict and out.model
respectively by default).

A more comprehensive range of settings are available in the
docs/config.py file. This gives you full access to the range of
options provided by the gensim API. It also has a setting for the
comparison script (described later).

view_model.py
-------------

Takes as input a dictionary and a model so that the model may be
examined. At present, just prints the top terms for each topic in the
model. Will be made more comprehensive later.

compare_models.py
-----------------

Takes as input two LSA or LDA models. At present, it identifies
pairings for each of the most similar topics between the two
models. However, in future this information will be expanded to
compute the similarity of the two models and hence give a measure for
their stability.

Similarity is measured using the average Jaccard distance, a metric
proposed by Greene, O'Callaghan and Cunningham in their paper "How
Many Topics? Stability Analysis for Topic Models"
