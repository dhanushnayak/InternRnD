import pandas as pd
import requests as r
from bs4 import BeautifulSoup as bs
from selenium import webdriver
#driver = webdriver.Firefox(executable_path="D://geckodriver.exe")
import re
import time
from pymongo import MongoClient as client
from newspaper import Article
class times_of_india():
    def __init__(self,content,svc="mongodb://localhost:27017/",driver="D://geckodriver.exe",pagefrom=1,pageto=5):
        self.svc=svc
        self.content=content
        self.driver = webdriver.Firefox(executable_path=driver)
        self.driver.set_window_position(0, 0)
        self.pagefrom = int(pagefrom)
        self.pageto = int(pageto)
    def get_sub_links(self):
        print("Init-Sub-category")
        l=set()
        page = r.get("https://timesofindia.indiatimes.com/"+self.content)
        soup = bs(page.content,"html.parser")
        l=set()
        for i in soup.find("nav").find_all("a",href=True):
            if re.search("/"+self.content+"/*",i['href']):
                l.add("https://timesofindia.indiatimes.com"+i['href'])
        return l
    def get_full_links(self):
        print("Init-Get-Links")
        l=set()
        links = self.get_sub_links()
        for j in links:
            page = r.get(j)
            soup=bs(page.content,'html.parser')
            try:
                for i in soup.find("div",{"class":re.compile('main-content*')}).find_all("a",href=True):
                    
                    try:
                        if i['href'].split('.')[-1]=='cms':
                            if i['href'].split("/")[0]=="https:":
                                l.add(i['href'])
                            else:
                                l.add("https://timesofindia.indiatimes.com"+i['href'])
                    except:
                        pass
            except:
                pass
        return l
    def get_content(self):
        link = list(self.get_full_links())
        print("Started Fetching")
        l=[]
        for i in link[self.pagefrom:self.pageto]:
            try:
                print(i)
                d={}
                d['Link']=i
                page = r.get(i)
                d['Content'] = bs(page.content,'html.parser').find("div",{"class":re.compile("ga-headlines")}).text
                self.driver.get(i)
                time.sleep(2)
                try:
                    d['Title']=self.driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[1]/div[2]/div[1]/h1").text
                except:
                    d['Title']=self.driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[1]/div[2]/div[2]/h1").text
                try:
                    d['Time']=self.driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]").text
                except:
                    d['Time']=self.driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]").text
                try:
                    d['Image']=self.driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[1]/div[2]/div[2]/section/div/div/img").get_attribute('src')
                except:
                    d['Image']=self.driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[1]/div[2]/div[3]/section/div/div/img").get_attribute('src')
                l.append(d)
            except:
                pass
            
        return l

    def load_to_database(self):
        try:
            l=self.get_content()
            connect = client(self.svc)
            db=connect.internrndd
            col = db['timesofindia']
            col.insert_many(l)
            self.close_drive()
            return "Success"
        except:
            self.close_drive()
            return "Error Raised"
        
    def close_drive(self):
        self.driver.close()