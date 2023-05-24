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
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')


headers = {
        'authority': 'www.amazon.com',
          'pragma': 'no-cache',
          'cache-control': 'no-cache',
          'dnt': '1',
          'upgrade-insecure-requests': '1',
          'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
          'sec-fetch-site': 'none',
          'sec-fetch-mode': 'navigate',
          'sec-fetch-dest': 'document',
          'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}


def parser_flip(url):
  nextpage = requests.get(url, headers=headers)
  nextsoup = BeautifulSoup(nextpage.content, 'html.parser')
  if not (nextsoup.find_all('a', {"class":"IRpwTa"})):
    next = nextsoup.find_all('a', {"class":"s1Q9rs"})  
  elif not (nextsoup.find_all('a', {"class":"s1Q9rs"})):
    next = (nextsoup.find_all('a', {"class":"IRpwTa"}))
  elif not (nextsoup.find_all('a', {"class":"a-truncate-cut"})):
    next = nextsoup.find_all('a', {"class":"_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"})
  else:
    next = (nextsoup.find_all('span', {"class":"a-truncate-cut"}))

  # next = nextsoup.find_all('a', {"class":"IRpwTa"})
  name = []
  for i in next:
    name.append(i.text)
  return name



def page_visit_flip(url_flip):
  # url = "https://www.amazon.in/s?k=skewb&page=4&qid=1675945882&ref=sr_pg_4"
  source_code = requests.get(url_flip, headers=headers)
  soup = BeautifulSoup(source_code.content, "html.parser")
  visit=[]
  try:
    for i in soup.find_all('a',{'class':'ge-49M'}):
      visit.append(i.text)
    last_page = (visit[-1])
  except:
    last_page = 1
  return last_page




def search_flip(key):
  key = re.sub(r'[^a-zA-Z0-9]',' ',key)
  key = re.sub(' +',' ',key)
  # key = (key.replace(' ','-')).lower()
  print(key)
  url_flip = 'https://www.flipkart.com/search?q=' + str(
      key) + '&marketplace=FLIPKART&otracker=start&as-show=on&as=off'


  source_code = requests.get(url_flip, headers=headers)
  plain_text = source_code.text
  soup = BeautifulSoup(plain_text, "html.parser") 

  home = 'https://www.flipkart.com'

  page = int(page_visit_flip(url_flip))
  print('page_visit : ',page)

  flip_name = []
  try:
    link = soup.find_all('a',{'class' : "ge-49M"})[0]['href']
    full_link = home+link[:-1]
    class_1 = "ge-49M"
    for i in range(1, page+1):
      url = full_link+str(i)
      # print(url)
      items = parser_flip(url)
      for j in items:
        flip_name.append((j))
    # len(flip_name)
  except:
    items = parser_flip(url_flip)
    for j in items:
      flip_name.append((j))
    # len(flip_name)


  print(len(list(itertools.chain(flip_name))))
  flip = list(set(itertools.chain(flip_name)))

  search = model.encode(flip)
  d1 = {'Product_Name_flip':0,'Similarity_flip':0}

  try:
    x = model.encode(key)
    scores = cosine_similarity([x], search)[0]

    top_score = np.sort(scores)[::-1][:10]             #cosine_Similarity sorting by asc
    top_scores_id = np.argsort(scores)[::-1][:10]  
    a1,b1=[],[]

    for i, j in zip(top_scores_id,top_score):
      a1.append(flip[i])
      b1.append(str(j))
    d1 = {'Product_Name_flip':a1,'Similarity_flip':b1}
    data1 = pd.DataFrame(d1)
  except:
    data1 = d1
  return data1



