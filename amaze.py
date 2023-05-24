from bs4 import BeautifulSoup
import requests
from difflib import get_close_matches
import webbrowser
from collections import defaultdict
import random
import itertools
import re 
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')  #'msmarco-distilbert-base-v4'
# model = SentenceTransformer('msmarco-distilbert-base-v4')
link, name ,d = 0,0,0



# Faking the visit from a browser
headers = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'Connection': 'keep-alive',
    'upgrade-insecure-requests': '1',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}


home = 'https://www.amazon.in'

proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80","116.66.191.134:80","103.199.139.186:83","44.211.86.71:999","18.207.142.24:3128",
                    "128.199.200.112:138", "107.173.209.227:3128","149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80","122.166.193.145:3127","44.202.32.102:3128","54.157.150.36:3128",
                    "134.213.29.202:4444","5.161.121.151:3128","45.77.120.39:3128","24.249.199.12:4145","103.174.81.66:8080","103.242.119.88:80","44.204.200.4:9999","44.204.218.108:9999",
                     "44.211.82.82:3128","3.226.168.144:80","54.210.239.35:80","75.101.218.120:80","3.235.126.194:8088","54.86.198.153:80","34.239.204.118:80","44.204.212.148:9999","3.239.106.71:999",
                    "44.211.55.93:8088","3.233.210.25:3128","52.91.125.47:3128","3.238.32.243:999","52.87.254.169:3128","18.209.241.179:80","3.235.126.194:9999","3.230.169.197:9999",
                    "52.23.240.115:3128","3.239.55.42:9999","50.16.74.164:80","34.207.221.227:9999","3.239.253.209:8088","52.201.211.145:3128","34.236.43.123:80","179.1.192.11:999","165.154.236.174:80",
                    "70.177.15.10:8080","192.3.134.6:8099","102.38.5.233:8080","103.243.114.206:8080","188.132.221.3:8080","91.107.253.172:3128","88.150.15.30:80","93.177.126.79:8088","190.104.245.86:8080"]




def parser(soup,class_1):
  link = "https://www.amazon.in"+str(soup.find_all('a', {"class":class_1})[0]['href'])
  nextpage = requests.get(link, headers=headers)
  nextsoup = BeautifulSoup(nextpage.content, 'html.parser')

  if not (nextsoup.find_all('span', {"class":"a-size-medium a-color-base a-text-normal"})):
    y = nextsoup.find_all('span', {"class":"a-size-base-plus a-color-base a-text-normal"})  
  elif not (nextsoup.find_all('span', {"class":"a-size-base-plus a-color-base a-text-normal"})):
    y = (nextsoup.find_all('span', {"class":"a-size-medium a-color-base a-text-normal"}))
  elif not (nextsoup.find_all('span', {"class":"a-truncate-cut"})):
    y = nextsoup.find_all('span', {"class":"_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"})
  else:
    y = (nextsoup.find_all('span', {"class":"a-truncate-cut"}))

  name = []
  for i in y:
    name.append(i.text)
  return name, nextpage, link




def page_visit(url_amzn):
  source_code = requests.get(url_amzn, headers=headers)
  soup = BeautifulSoup(source_code.content, "html.parser")

  y = soup.find_all('a',{'class':'s-pagination-item s-pagination-button'})
  try :t1 = int(y[-1].text) 
  except : t1 = 0
  p = soup.find_all('span', {'class':'s-pagination-item s-pagination-disabled'})
  try:    t2 = int(p[0].text)
  except: t2 = 0

  if t1>t2:page_range = t1  
  elif t2>t1:page_range = t2
  else:page_range = 1
  return page_range



def search(key):
  key = re.sub(r'[^a-zA-Z0-9]',' ',key)
  key = re.sub(' +',' ',key)
  # key = (key.replace(' ','-')).lower()
  print(key)

  url_amzn = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)

  proxies = {'https': random.choice(proxies_list)}
  print(proxies)

  source_code = requests.get(url_amzn, headers=headers)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser")

  page_range = page_visit(url_amzn)



  name = []
  for i in range(1,page_range+1):           #"a-size-base-plus a-color-base a-text-normal", "a-size-medium a-color-base a-text-normal",  '_cDEzb_p13n-sc-css-line-clamp-3_g3dy1','a-truncate-cut',"a-size-base-plus a-color-base a-text-normal",
    soup = BeautifulSoup(plain_text, "html.parser")

    if not (soup.find_all('span', {"class":"a-size-medium a-color-base a-text-normal"})):
        y = soup.find_all('span', {"class":"a-size-base-plus a-color-base a-text-normal"})  
    elif not (soup.find_all('span', {"class":"a-size-base-plus a-color-base a-text-normal"})):
        y = (soup.find_all('span', {"class":"a-size-medium a-color-base a-text-normal"}))
    elif not (soup.find_all('span', {"class":"a-truncate-cut"})):
        y = soup.find_all('span', {"class":"_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"})
    else:
        y = (soup.find_all('span', {"class":"a-truncate-cut"}))

    for i in y:  
        name.append(i.text)

    class_1 = "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"
    if soup.find_all('a', {"class":class_1}):
        items , arg, link = parser(soup, class_1)
        plain_text = arg.content
        for j in items:
            name.append((j))
        print(link)

  try:
    n = 0
    for i in str(page_range):n+=1
    last = link
    link = last[:-n]+str(page_range)
    print(link)
    lastsoup = requests.get(link, headers=headers)
    next_sop = BeautifulSoup(lastsoup.content, 'html.parser')
    if not (next_sop.find_all('span', {"class":"a-size-medium a-color-base a-text-normal"})):
        next = next_sop.find_all('span', {"class":"a-size-base-plus a-color-base a-text-normal"})  
    elif not (next_sop.find_all('span', {"class":"a-size-base-plus a-color-base a-text-normal"})):
        next = (next_sop.find_all('span', {"class":"a-size-medium a-color-base a-text-normal"}))
    elif not (next_sop.find_all('span', {"class":"a-truncate-cut"})):
        next = next_sop.find_all('span', {"class":"_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"})
    else:
        next = (next_sop.find_all('span', {"class":"a-truncate-cut"}))

    for i in next:
        name.append(i.text)
  except:
    pass


  print(len(list(itertools.chain(name))))
  final = list(set(itertools.chain(name)))
  search = model.encode(final)
  d = {'Product_Name':0,'Similarity':0}
  try:
    x = model.encode(key)
    print(x.shape)
    scores = cosine_similarity([x], search)[0]

    top_score = np.sort(scores)[::-1][:10]             #cosine_Similarity sorting by asc
    print(top_score)
    top_scores_id = np.argsort(scores)[::-1][:10]  
    print(top_scores_id)           #getting index 
    a,b=[],[]

    for i, j in zip(top_scores_id,top_score):
      a.append(final[i])
      b.append(str(j))
    

    d = {'Product_Name':a,'Similarity':b}
    # data = pd.DataFrame(d)
    data = d
  except:
    data = d
          
  return data
  
# print(search('multigrain bread'))