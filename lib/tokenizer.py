import nltk
import re
from docs import config

# tokenize input string into words and remove stopwords
def tokenize(text):
    aposeq = r"[`='\(\)_]+|[!.\?\*:,]"

    no_mark = re.sub(aposeq, '', text)
    stopwords = set(nltk.corpus.stopwords.words(config.stop_word_list)) if config.use_stop_word_list else []
    return [word.lower().encode('utf-8') for word in nltk.tokenize.word_tokenize(no_mark.decode('utf-8')) if word.lower().encode('utf-8') not in stopwords ]
