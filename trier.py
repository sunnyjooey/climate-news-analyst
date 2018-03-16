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

def set_parsed_list_or_nan(row, tokenized_sentences_col, id_col = None, error_list = None):
    from numpy import nan
    try:
        print("{} {}".format(row.name, row[id_col]))
        return [list(parsed) for parsed in stanford.parser.parse_sents(
            [nltk.word_tokenize(s) for s in nltk.sent_tokenize(row['text'])])] #row[tokenized_sentences_col])]
    except ValueError as err:
        print(row[id_col])
        print(err)
        if error_list:
            print("time: {}, {}, {}".format(time.time(), row['filename'], err), file=error_list)
            #error_list.append((row[id_col], "{}".format(err)))
        return nan
    except OSError as err:
        print(row[id_col])
        print(err)
        if error_list:
            print("time: {}, {}, {}".format(time.time(), row['filename'], err), file=error_list)
            #error_list.append((row[id_col], "{}".format(err)))
        return nan
news_df = pandas.read_pickle('../news_df.pkl')
news_df = news_df.sample(3000)

#news_df = pandas.concat([pandas.read_pickle('../news_df_norm1.pkl'), pandas.read_pickle('../news_df_norm2.pkl')])
#news_df['text'] = news_df['text'].apply(lambda x: re.sub(r'\.\s*?"\s?', '". ', x))
#news_df['text'] = news_df['text'].apply(lambda x: re.sub(r',\s*?"\s?', '", ', x))
news_df['text'] = news_df['text'].apply(lambda x: re.sub(r'\.\s*"\s?', '". ', x))
news_df['text'] = news_df['text'].apply(lambda x: re.sub(r',\s*"\s?', '", ', x))
# Substitutes .A with . A
news_df['text'] = news_df['text'].apply(lambda x: re.sub(r'\.(?=[A-Z])', '", ', x))

#news_df['tokenized_sentences'] = news_df['text'].apply(lambda x: [nltk.word_tokenize(s) for s in nltk.sent_tokenize(x)])

errors_out = []
oserrors = []
news_df['parse_sents'] = np.nan
print("About to start parsing {} items".format(len(news_df)))
with open('errors3k.txt', 'w', buffering=1) as outf:
    news_df['parse_sents'] = news_df.apply(lambda x: set_parsed_list_or_nan(x, 'tokenized_sentences',
        id_col='filename', error_list=outf), axis=1)

#with open('errors2.txt', 'w', buffering=1) as outf:
#    for ix, row in news_df.iterrows():
#        try:
#            outf.flush()
#            os.fsync(outf.fileno())
#            row['parse_sents'] = [list(parsed) for parsed in stanford.parser.parse_sents(row['tokenized_sentences'])]
#            print("time: {}, {}, {}".format(time.time(), row['filename'], 'success'))
#        except ValueError as err:
#            print("time: {}, {}, {}".format(time.time(), row['filename'], err), file=outf)
#            print("time: {}, {}, {}".format(time.time(), row['filename'], err))
#            #errors_out.append((row['filename'], "{}".format(err)))
#        except OSError as err:
#            print("time: {}, {}, {}".format(time.time(), row['filename'], err), file=outf)
#            print("time: {}, {}, {}".format(time.time(), row['filename'], err))
            #errors_out.append((row['filename'], "{}".format(err)))
#with open('errors2.txt', 'w', buffering=1) as outf:
#    for ix, err in errors_out:
#        print("time {}: {}".format(time.time(), ix)
#        outf.write("{}, {} \n".format(ix, err))

news_df.to_pickle('sampletrees3k.pkl')

