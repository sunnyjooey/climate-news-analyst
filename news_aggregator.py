"""
Module intended to be run to aggregate news items into a 
pickled dataframe to be used in analysis of news.
Does some cleaning, separates text, source, date, author.
"""
import os
import re
import argparse
import pandas
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='News item aggregator into a pickled dataframe')
parser.add_argument('--output', type=str, default='news_df.pkl',
                    help='Name of the file for the pickled dataframe output')
args = parser.parse_args()

def extract_news(html, country):
    """
    Cleans and separates elements of an article.
    args:
        html: html text from news article file
        country: country code from file
    output:
        A dictionary with the text, title, authors, date of the news article file.
    """
    article_dict = {'filename': html.name, 'country': country}
    soup = BeautifulSoup(html, 'lxml')
    
    # title
    title0 = soup.find_all('div', {'class' : 'title'})
    # cleaning
    title1 = title0[0].text.replace('Hide Details', '')
    title = re.sub(r'\<.*\>', '', title1)
    article_dict['title'] = title

    # text
    body = soup.find_all('div', {'class' : 'body'})
    text0 = body[0].text.replace('\n', ' ')
    
    # take out first word if all caps (it is a location)
    text1 = re.sub(r"^([A-Z]{2,}\s?[A-Z]{2,})", "", text0)
    # take out from end
    text1 = re.sub(r'©.*$', '', text1)
    text2 = re.sub(r"\S*@\S*\s?", "ZXCVB", text1) #email
    text3 = re.sub(r"ZXCVB(.*)|Published by HT (.*)|Caption (.*)|Copyright\s\((.*)|Copyright: (.*)|Source- (.*)|Digital Content Services (.*)|Syndication with permission (.*)|www(.*)|http(.*)", "", text2)
    # take out from middle 
    text4 = re.sub(r"(STORY CAN END HERE)", "", text3)
    text5 = re.sub(r"(EDITORS: STORY CAN END HERE)", "", text4)
    text = re.sub(r"(EDITORS: )", "", text5)

    # take out all dots that are within parentheses (semantic parser dislikes that)
    def dots_in_parentheses(match):
        return re.sub(r'\.', r';', match.group())
    parens = re.compile(r'(?<=\()[^\)]*?\..[^\(]*?(?=\))')
    text = parens.sub(dots_in_parentheses, text)
    text = re.sub(r'\."', '".', text)
    article_dict['text'] = text

    # source & date
    source = soup.find_all('div', {'class' : 'source'})
    date = re.findall(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}', source[0].text)
    article_dict['date'] = date[0]
    pat2 = re.compile(r"(.*?)-\s", re.M)
    newssource = pat2.findall(source[0].text)
    article_dict['source'] = newssource[0]

    # author
    author0 = soup.find_all('span', {'class' : 'val'})
    author = re.sub(r'\<.*\>', '', author0[0].text) #Take out <>
    article_dict['author'] = author

    # section
    section0 = soup.find_all('span', {'class' : 'lbl'}, string="Section: ")
    try:
        section = section0[0].next_element.next_element.next_element.text
        article_dict['section'] = section
    except:
        article_dict['section'] = ''
    
    return article_dict

def aggregate_news_files():
    """
    Runs through the news article data files, extracts the news and 
    aggregates them into a pandas dataframe
    """
    indir = './data/'
    article_list = []
    for root, _, filenames in os.walk(indir):
        for newsfile in filenames:
            filepath = os.path.join(root, newsfile)
            with open(filepath, 'r', encoding='utf-8') as testfile:
                try:
                    article_dict = extract_news(testfile, newsfile[:2])
                    article_list.append(article_dict)
                except:
                    print(filepath)
                    raise
    return pandas.DataFrame(article_list)

df = aggregate_news_files()


# Take out duplicates
dups = pandas.read_pickle('to_delete_index.pkl')
news_sorted = df.sort_values(by=['country','title'])
news_sorted.reset_index(inplace=True)
news_sorted.drop(['index'], axis=1, inplace=True)
df = news_sorted.loc[~news_sorted.index.isin(dups)] 


df.to_pickle(args.output)

