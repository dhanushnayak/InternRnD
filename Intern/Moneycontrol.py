import pandas as pd
import requests as r
from bs4 import BeautifulSoup as bs
from selenium import webdriver
#driver = webdriver.Firefox(executable_path="D://geckodriver.exe")
import re
import time
from pymongo import MongoClient as client
from newspaper import Article
class moneycontrol():
    def __init__(self,content,limit=5,svc="mongodb://localhost:27017/",page_from=1,page_to=2):
        self.svc = svc
        self.cate=content
        self.limit=limit
        self.page_to=page_to
        self.page_from = page_from
    
    def fetch(self):
        j=self.page_from
        while(j<=self.page_to):
            if j==0:
                
                url="https://www.moneycontrol.com/news/business/{}/".format(self.cate)
            else:
                url="https://www.moneycontrol.com/news/business/"+self.cate+"/page-"+str(j)+"/"
            print(url)
            
            if r.get(url).status_code==200:
                print(r.get(url).status_code)
                page = r.get(url)
                soup = bs(page.content,'html.parser')
                l=[]
                for i in soup.find_all("li",{"class":"clearfix"}):
                    try:
                        if re.search("https://www.moneycontrol.com/news/",i.find("a",href=True)['href']):
                            d={}
                            sub_url=i.find("a",href=True)['href']
                            art=Article(sub_url)
                            art.download()
                            art.parse()
                            d["Link"]=sub_url
                            d['Title']=art.title
                            d['Content']=art.text
                            d['Image']=art.top_image
                            try:
                                d['Date']=bs(art.html,'html.parser').find("div","article_schedule").text
                            except:
                                pass
                            l.append(d)
                            
                            
                    except:
                        pass
                    
                    
                self.load_to_database(l)
                print("Inserted")

            else:
                pass
            print("&&"*66)
            j+=1
    def load_to_database(self,l):
        try:
            
            connect = client(self.svc)
            db=connect.internrndd
            col = db['moneycontrol']
            col.insert_many(l)
            return "Success"
        except:
            
            return "Error Raised"