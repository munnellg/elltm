import nltk
import re
import nltk.data
from docs import config

# tokenize input string into words and remove stopwords
def tokenize(text):
    aposeq = r"[`='\(\)_]+|[\"\;\-!.\?\*:,]"

    no_mark = re.sub(aposeq, '', text)
    stopwords = set(nltk.corpus.stopwords.words(config.stop_word_list)) if config.use_stop_word_list else []
    return [word.lower().encode('utf-8') for word in nltk.tokenize.word_tokenize(no_mark.decode('utf-8')) if word.lower().encode('utf-8') not in stopwords ]

def text_to_sentences(text):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    raw_sentences = tokenizer.tokenize(text.strip().decode('utf-8'))
    sentences = [sentence.encode('utf-8') for sentence in raw_sentences if len(sentence) > 0]
    return sentences
