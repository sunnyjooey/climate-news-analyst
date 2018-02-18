import newsbank_scraper as ns
import logging
import pickle
import os

folder = '/project2/macs60000/sunjoo-victorvt/climate-news-analyst/'
filename = 'news_USA.pkl'
filepath=os.path.join(folder,filename)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#(language='English', year='2017', country='USA', sourcetype='Newspaper',  searchterm='climate%20change', limit=None)
thing = ns.get_all_news(country='USA',limit=150)
with open(filepath, 'wb') as output:
    pickle.dump(thing, output)
