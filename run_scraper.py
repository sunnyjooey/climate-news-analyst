import newsbank_scraper as ns
import logging
import pickle

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#(language='English', year='2017', country='USA', sourcetype='Newspaper',  searchterm='climate%20change', limit=None)
thing = ns.get_all_news(country='USA')
with open('news_USA.pkl', 'wb') as output:
    pickle.dump(thing, output)
