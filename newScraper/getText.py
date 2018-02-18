import os
import pandas
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import re
import urllib
import math


def extract_news(html, country):
    
    article_dict = {'country': country}
    soup = BeautifulSoup(html, 'lxml')
    #testing 
    
    
    # title
    title0 = soup.find_all('div', {'class' : 'title'})
    title1 = title0[0].text.replace('Hide Details', '') #cleaning
    title = re.sub(r'\<.*\>', '', title1)
    article_dict['title'] = title

    # text
    body = soup.find_all('div', {'class' : 'body'})
    text0 = "".join([t for t in body[0].contents if type(t)==NavigableString]) #get text only from content, not children
    text1 = re.sub(r"Source- .+","", text0) #cleaning
    text2 = re.sub(r"© .+","", text1) #cleaning
    text3 = re.sub(r"(STORY CAN END HERE)","", text2) #cleaning 
    text4 = re.sub(r"(EDITORS: STORY CAN END HERE)","", text3) #cleaning
    text5 = re.sub(r"(EDITORS: )","", text4) #cleaning
    text = re.sub(r"^([A-Z]{2,}\s?[A-Z]{2,})", "", text5) #take out first word if all caps (it is a location)
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


def getText():
    indir = './data/'
    articleList = []
    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            filepath = os.path.join(root,f)
            with open(filepath, 'r', encoding='latin1') as testfile:
                try:
                    articleDict = extract_news(testfile, f[:2])
                    articleList.append(articleDict)
                except:
                    print(filepath)
                    raise
    return pandas.DataFrame(articleList)


df = getText()
df.to_csv('news_df.csv')