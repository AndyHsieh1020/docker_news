import pymongo
import time
from datetime import datetime
import certifi
import requests
from bs4 import BeautifulSoup
import threading

#time title pic content link

ca = certifi.where()

myclient = pymongo.MongoClient('mongodb+srv://andyssvs015:7gHZ4pTmBVLUjMo8@tw-news.mbrlkzb.mongodb.net/', tlsCAFile=ca)
mydb = myclient['tw-news']
collist = mydb.list_collection_names()
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}


def LTN():

    resp_LTN = requests.get('https://news.ltn.com.tw/list/breakingnews',headers=headers)
    soup_LTN = BeautifulSoup(resp_LTN.text, 'html.parser')
    contents_LTN = soup_LTN.find('ul', class_='list')
    for i in contents_LTN.find_all('li'):
        
        try:

            col_LTN = mydb["LTN"]
            my_data = {'title':i.find('a').get('title'), 'img':i.find('img').get('data-src'), 'time':datetime.today(),'link':i.find('a').get('href')}
            col_LTN.insert_one(my_data)
        
        except Exception as e:

            print(e)
            

def CHT():

    resp_CHT = requests.get('https://www.chinatimes.com/realtimenews/?chdtv',headers=headers)
    soup_CHT = BeautifulSoup(resp_CHT.text, 'html.parser')
    contents_CHT = soup_CHT.find('ul', class_='vertical-list list-style-none')

    for i in contents_CHT.find_all('li'):

        try:
            
            h3 = i.find('h3')
            col_CHT = mydb["CHT"]
            my_data = {'title':i.find('img').get('alt'), 'img':i.find('img').get('src'), 'time':datetime.today(), 'content':i.find('p', class_='intro').string, 'link':'https://www.chinatimes.com'+h3.find('a').get('href')}
            col_CHT.insert_one(my_data)

        except Exception as e:
            
            print(e)
        

def UDN():

    resp_UDN = requests.get('https://udn.com/news/breaknews/1',headers=headers)
    soup_UDN = BeautifulSoup(resp_UDN.text, 'html.parser')
    contents_UDN = soup_UDN.find('div', class_='context-box__content story-list__holder story-list__holder--full')
    for i in contents_UDN.find_all('div', class_='story-list__news'):
        
        try:
            
            h2 = i.find('h2')
            p = i.find('p')
            col_UDN = mydb["UDN"]
            my_data = {'title':h2.find('a').get('title'), 'img':i.find('img').get('data-src'), 'time':datetime.today(), 'content':p.find('a').string, 'link':'https://udn.com'+h2.find('a').get('href')}
            col_UDN.insert_one(my_data)

        except Exception as e:
            
            print(e)
        

def CTEE():

    resp_CTEE = requests.get('https://www.ctee.com.tw/livenews/ctee',headers=headers)
    soup_CTEE = BeautifulSoup(resp_CTEE.text, 'html.parser')
    contents_CTEE = soup_CTEE.find('div', class_='newslist livenews')
    for i in contents_CTEE.find_all('div', class_='newslist__card'):
        
        try:
            
            h3 = i.find('h3')
            col_CTEE = mydb["CTEE"]
            my_data = {'title':h3.find('a').string, 'time':datetime.today(), 'link':'https://www.ctee.com.tw'+h3.find('a').get('href')}
            col_CTEE.insert_one(my_data)

        except Exception as e:
            
            print(e)
        

def Money():

    resp_Money = requests.get('https://money.udn.com/rank/newest/1001',headers=headers)
    soup_Money = BeautifulSoup(resp_Money.text, 'html.parser')
    contents_Money = soup_Money.find('ul', class_='story-list-holder')
    for i in contents_Money.find_all('li', class_='story-headline-wrapper'):
        
        try:
            
            col_Money = mydb["Money"]
            my_data = {'title':i.find('a').get('title'), 'img':i.find('img').get('src'), 'time':datetime.today(), 'content':i.find('p', class_='story__text').string, 'link':i.find('a').get('href')}
            col_Money.insert_one(my_data)

        except Exception as e:
            
            print(e)
        
def CNA():

    resp_CNA = requests.get('https://www.cna.com.tw/list/aall.aspx',headers=headers)
    soup_CNA = BeautifulSoup(resp_CNA.text, 'html.parser')
    contents_CNA = soup_CNA.find(attrs={'id':'jsMainList'})
    for i in contents_CNA.find_all('li'):
        
        try:
            
            try:
                pic = i.find('img').get('src')
            except:
                pic = ''

            col_CNA = mydb["CNA"]
            my_data = {'title':i.find('span').string, 'img':pic, 'time': datetime.today(), 'link':'https://www.cna.com.tw/'+i.find('a').get('href')}
            col_CNA.insert_one(my_data)

        except Exception as e:
            
            print(e)
        
def exp_date(col):

    now = (datetime.today()-datetime(1970, 1, 1)).total_seconds()

    # Date and Time constants
    day_ct = 24 * 60 * 60  # 86400

    query = {'time': {"$lt": datetime.fromtimestamp(now-7*day_ct)}}
    delete_ids = []
    for x in col.find(query):
        delete_ids.append(x["_id"])

    d = col.delete_many({'_id': {"$in": delete_ids}})
    
    print(d.deleted_count, "已刪除")


def app():

        
    col__CHT = mydb["CHT"]
    col_UDN = mydb["UDN"]
    col_LTN = mydb["LTN"]
    col_CTEE = mydb["CTEE"]
    col_Money = mydb["Money"]
    col_CNA = mydb["CNA"]
    exp_date(col__CHT)
    exp_date(col_UDN)
    exp_date(col_CTEE)
    exp_date(col_LTN)
    exp_date(col_Money)
    exp_date(col_CNA)

    t1 = threading.Thread(target = LTN)
    t2 = threading.Thread(target = UDN)
    t3 = threading.Thread(target = CHT)
    t4 = threading.Thread(target = CNA)
    t5 = threading.Thread(target = Money)
    t6 = threading.Thread(target = CTEE)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()



if __name__ == '__main__':
    app()



















    
    

    



    
   
    
   