import pandas as pd
import requests as r
from bs4 import BeautifulSoup as bs
from selenium import webdriver
#driver = webdriver.Firefox(executable_path="D://geckodriver.exe")
import re
import time
from pymongo import MongoClient as client
from newspaper import Article
class indianexpress():
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
                
                url="https://indianexpress.com/section/{}/".format(self.cate)
            else:
                url="https://indianexpress.com/section/"+self.cate+"/page/"+str(j)+"/"
            print(url)
            
            if r.get(url).status_code==200:
                print(r.get(url).status_code)
                page = r.get(url)
                soup = bs(page.content,'html.parser')
                l=[]
                for i in soup.find_all("div",{"class":re.compile("articles")}):
                    d={}
                    try: 
                        sub_url = i.find("a",href=True)['href']
                        print(sub_url)
                        if sub_url.split(":")[0]=="https":
                            
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
                    
                self.load_to_database(l)
                print("Inserted")

            else:
                break
            print("&&"*66)
            j+=1
    def load_to_database(self,l):
        try:
            
            connect = client(self.svc)
            db=connect.internrndd
            col = db['indianexpress']
            col.insert_many(l)
            return "Success"
        except:
            
            return "Error Raised"