import lucem_illud #pip install -U git+git://github.com/Computational-Content-Analysis-2018/lucem_illud.git

#All these packages need to be installed from pip
#For NLP
import nltk
import time
import numpy as np #For arrays
import pandas #Gives us DataFrames
import lucem_illud.stanford as stanford
import re
import os
from numpy import nan

def set_parsed_list_or_nan(row, tokenized_sentences_col, id_col = None, error_list = None):
    """
    Attempts to parse using stanford parser. Many articles will fail, it prints out formatted
    information that we later use to attempt to ameliorate several of the errors.
    """
    try:
        print("{} {}".format(row.name, row[id_col]))
        return [list(parsed) for parsed in stanford.parser.parse_sents(
            [nltk.word_tokenize(s) for s in nltk.sent_tokenize(row['text'])])] 
    except ValueError as err:
        print(row[id_col])
        print(err)
        if error_list:
            print("time: {}, {}, {}".format(time.time(), row['filename'], err), file=error_list)
        return nan
    except OSError as err:
        print(row[id_col])
        print(err)
        if error_list:
            print("time: {}, {}, {}".format(time.time(), row['filename'], err), file=error_list)
        return nan
news_df = pandas.read_pickle('../news_df.pkl')
news_df = news_df.sample(3000)

#Cleaning for dependency parsing: Quotations need to be closed before the sentence dot ends.
news_df['text'] = news_df['text'].apply(lambda x: re.sub(r'\.\s*"\s?', '". ', x))
news_df['text'] = news_df['text'].apply(lambda x: re.sub(r',\s*"\s?', '", ', x))
# Substitutes .A with . A
news_df['text'] = news_df['text'].apply(lambda x: re.sub(r'\.(?=[A-Z])', '", ', x))

errors_out = []
oserrors = []
news_df['parse_sents'] = np.nan
print("About to start parsing {} items".format(len(news_df)))
with open('errors3k.txt', 'w', buffering=1) as outf:
    news_df['parse_sents'] = news_df.apply(lambda x: set_parsed_list_or_nan(x, 'tokenized_sentences',
        id_col='filename', error_list=outf), axis=1)

# Creates pickle with news and dependency tree for each article's sentences
news_df.to_pickle('sampletrees3k.pkl')

