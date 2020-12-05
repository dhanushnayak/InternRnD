import pandas as pd
import requests as r
from bs4 import BeautifulSoup as bs
from selenium import webdriver
#driver = webdriver.Firefox(executable_path="D://geckodriver.exe")
import re
import time
from pymongo import MongoClient as client
from newspaper import Article
class Firstpost():
    def __init__(self,content,limit=5,svc="mongodb://localhost:27017/",page_from=1,page_to=2):
        self.svc = svc
        self.cate=content
        self.limit=limit
        self.page_from = page_from
        self.page_to= page_to
    def fetch(self):
        j = self.page_from
        while(j<=self.page_to):
            if j==0:
                url="https://www.firstpost.com/category/{}/".format(self.cate)
            else:
                url="https://www.firstpost.com/category/"+self.cate+"/page/"+str(j)+"/"
            print(url)
            print(r.get(url).status_code)
            if r.get(url).status_code==200:
                    
                page = r.get(url)
                soup = bs(page.content,'html.parser')
                l=[]
                for i in soup.find_all("div",{"class":"big-thumb"}):
                    d={}
                    try:
                        sub_url = i.find("a",href=True)['href']
                        if sub_url.split(":")[0]=="https" and sub_url.split(".")[-1]=="html":
                            print(sub_url)
                            article = Article(sub_url)
                            article.download()
                            article.parse()
                            d['Link']=sub_url
                            #print(article.publish_date)
                            d['Date']=article.publish_date
                            #print(article.text)
                            d["Content"]=article.text
                            #print(article.title)
                            d["Title"]=article.title
                            ##print(article.top_image)
                            d['Image']=article.top_image
                            #print("\n"*3)
                            #print("#"*77)
                            
                            l.append(d)
                           

                    except:
                        pass
                if self.load_to_database(l)==True:
                    print("Inserted")

            else:
                break
            print("&&"*60)
            j+=1
    def load_to_database(self,l):
            
            connect = client(self.svc)
            if connect:
                print("Connected")
            db=connect.internrndd
            col = db['firstpost']
            col.insert_many(l)
            
            return True