from requestium import Session, Keys
import time
from numpy.random import normal
from math import floor
import codecs
import os

urls_b = [
'http://infoweb.newsbank.com.proxy.uchicago.edu/resources/search/nb?p=WORLDNEWS&t=country%3AKenya%21Kenya%2Fyear%3A2017%212017%2Fstp%3ANewspaper%21Newspaper',
'http://infoweb.newsbank.com.proxy.uchicago.edu/resources/search/nb?p=WORLDNEWS&t=country%3AEngland%7CNorthern%2BIreland%7CScotland%7CWales%21Multiple%2BCountries%2Fyear%3A2017%212017%2Fstp%3ANewspaper%21Newspaper%2Flanguage%3AEnglish%21English',
'http://infoweb.newsbank.com.proxy.uchicago.edu/resources/search/nb?p=WORLDNEWS&t=country%3AIndia%21India%2Fyear%3A2017%212017%2Fstp%3ANewspaper%21Newspaper',
'http://infoweb.newsbank.com.proxy.uchicago.edu/resources/search/nb?p=WORLDNEWS&t=country%3AChina%21China%2Fyear%3A2017%212017%2Fstp%3ANewspaper%21Newspaper'
]

urls_a = [
    'http://infoweb.newsbank.com.proxy.uchicago.edu/resources/search/nb?p=WORLDNEWS&t=country%3ANigeria%21Nigeria%2Fyear%3A2017%212017%2Fstp%3ANewspaper%21Newspaper',
    'http://infoweb.newsbank.com.proxy.uchicago.edu/resources/search/nb?p=WORLDNEWS&t=country%3AUSA%21USA%2Fyear%3A2017%212017%2Fstp%3ANewspaper%21Newspaper%2Flanguage%3AEnglish%21English',
    'http://infoweb.newsbank.com.proxy.uchicago.edu/resources/search/nb?p=WORLDNEWS&t=country%3AAustralia%21Australia%2Fyear%3A2017%212017%2Fstp%3ANewspaper%21Newspaper',
    'http://infoweb.newsbank.com.proxy.uchicago.edu/resources/search/nb?p=WORLDNEWS&t=country%3AEgypt%7CSaudi%2BArabia%7CUnited%2BArab%2BEmirates%21Multiple%2BCountries%2Fyear%3A2017%212017%2Fstp%3ANewspaper%21Newspaper'
]

def chill(amount):
    translator = {'low':1, 'mild':4, 'long':13}
    time.sleep(translator[amount] + normal(loc=1.0, scale=0.5))

def get_to_page(page_no, s):
    #assuming page 0 of search results
    if page_no<10:
        #print(" no links")
        s.driver.find_element_by_link_text(u"{}".format(page_no)).click()
        chill('mild')
    else:
        num_times = floor((page_no-10)/4) + 1
        num = 9
        for i in range(num_times):
            s.driver.find_element_by_link_text(u"{}".format(num)).click()
            chill('mild')
            num += 4
        s.driver.find_element_by_link_text(u"{}".format(page_no)).click()
        chill('mild')
        print("num_times {}".format(num_times))

# If you want requestium to type your username in the browser for you, write it in here:
def get_news_from_url(target_url, max_articles, file_prefix, page):
    s = Session('./chromedriver', browser='chrome', default_timeout=15)#, webdriver_options = wdoptions)
    base_url = 'http://infoweb.newsbank.com.proxy.uchicago.edu'#"http://guides.lib.uchicago.edu/"
    s.driver.implicitly_wait(30)
    s.driver.get(target_url)#base_url + "/resources/?p=WORLDNEWS")#"/resources/search/nb?p=WORLDNEWS&t=continent%3AAfrica!Africa%2Fcountry%3AKenya!Kenya%2Fstp%3ANewspaper!Newspaper%2Fyear%3A2017!2017")
    chill('mild')
    s.driver.find_element_by_id("nbplatform-basic-search-val0").clear()
    chill('low')
    s.driver.find_element_by_id("nbplatform-basic-search-val0").send_keys("'climate change'")#'"el bronco" candidato independiente trump')
    chill('low')
    s.driver.find_element_by_id("nbplatform-basic-search-submit").click()
    chill('mild')
    if page > 1:
        get_to_page(page, s)
    links = s.driver.find_elements_by_css_selector("a.nb-doc-link")
    print("{} links on the page".format(links))
    master_counter = 0
    while master_counter < max_articles:
        per_page = len(links)
        for i in range(per_page):
            s.driver.find_elements_by_css_selector("a.nb-doc-link")[i].click()
            chill('long')
            file_name = '{}_{}.html'.format(file_prefix, master_counter)
            #save_path = os.path.expanduser()
            complete_name = os.path.join('./data/', file_name)
            file_object = codecs.open(complete_name, "w", "utf-8")
            html = s.driver.page_source
            file_object.write(html)
            ## Save file here
            master_counter += 1
            s.driver.back()
            chill('mild')
        s.driver.find_element_by_link_text(u"next ›").click()


#############################CHANGE FILE PREFIX IN EVERY RUN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#get_news_from_url(urls_a[0], 100, 'NG9_10', 41)
#get_news_from_url(urls_a[1], 200, 'US9_10', 81)
#get_news_from_url(urls_a[2], 100, 'AU10', 91)
get_news_from_url(urls_a[3], 100, 'ME10', 91)