# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:35:04 2015

@author: Talha
"""

import pandas as pd
from bs4 import BeautifulSoup
import os


def get_CNN_news():
    df = pd.DataFrame(columns=('fname', 'dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/cnn/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html)
            soup = BeautifulSoup(f, "lxml")
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            dt = pd.to_datetime(soup.find(class_="update-time").text[8:])
            href = soup.find(itemprop="url")['content']
            #newstxt = soup.find('section',id="body-text").text
            newstxt = '\n\n'.join([text.text.strip() for text in soup.findAll('p',{'class':'zn-body__paragraph'})])
            df.loc[len(df)]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except Exception as e:
            print(e)
            errors.append((i,html))
            print ('[ERROR]:',html)

    df['fname'] = df['fname'].str.replace('\.2$','')
    df['fname'] = df['fname'].str.replace('\.1$','')
    df['fname'] = df['fname'].str.replace('%0D$','')
    df = df.drop_duplicates()
    
    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/CNN-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_cnn.csv',index=False)
    return others
    
    
def get_NYT_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/nyt/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf8')
            soup = BeautifulSoup(f, "lxml")
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            dt = pd.to_datetime(soup.head.find('meta',{'name':'ptime'})['content'])
            href = soup.head.find('link',{'rel':'canonical'})['href']
            #newstxt = soup.find(id='story-body').text
            newstxt = '\n\n'.join([text.text.strip() for text in soup.findAll('p',{'class':"story-body-text story-content"})])
            df.loc[len(df)]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except Exception as e:
            print(e)
            errors.append((i,html))
            print ('[ERROR]:',html)

    df['fname'] = df['fname'].str.replace('\.2$','')
    df['fname'] = df['fname'].str.replace('\.1$','')
    df['fname'] = df['fname'].str.replace('%0D$','')
    df = df.drop_duplicates()
    
    others = list(zip(*errors))[1]
    #391 <- len(df[df.newstxt==''].href)
    df.to_csv("data/NYT-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_NYT.csv',index=False)
    return others


def get_ABC_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/abc/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            dt = pd.to_datetime(soup.head.find('meta',{'name':'Date'})['content'])
            href = soup.head.find('link',{'rel':'canonical'})['href']
            texts = soup.findAll('p',{'itemprop':'articleBody'})
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])
            df.loc[len(df)]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/abc-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_abc.csv',index=False)
    return others
    
    
def get_AP_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/ap/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html)
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            #dateline > span:nth-child(1)
            dt = pd.to_datetime(soup.find(id='dateline').find('span').text)
            href = soup.head.find('link',{'rel':'canonical'})['href']
            #newstxt = soup.find('section',id="body-text").text

            texts = soup.find(class_='field field-name-body field-type-text-with-summary field-label-hidden entry-content').findAll('p')[1:]
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])
            df.loc[len(df)]=[html, dt, title, href, newstxt]
            print (html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print (html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/AP-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_AP.csv',index=False)
    return others

    
def get_BBC_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/bbcworld/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            href = soup.head.find('link',{'rel':'canonical'})['href']
    
            dt = soup.find('p',{'class':'date date--v1'})
            if(dt):
                dt = pd.to_datetime(dt.find('strong').text)
                texts = soup.find(class_='map-body').findAll('p')
                newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])
            else:
                dt = soup.find('div',{'class':'date date--v2'}).text
                dt = pd.to_datetime(dt)
                texts = soup.find('div',{'property':'articleBody'}).findAll('p')
                newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])

            df.loc[len(df)]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/bbcworld-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_bbcworld.csv',index=False)


def get_FOX_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/foxnews/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            dt = pd.to_datetime(soup.head.find('meta',{'name':'dcterms.created'})['content'])
            href = soup.head.find('link',{'rel':'canonical'})['href']
            texts = soup.find('div',{'itemprop':'articleBody'}).findAll('p')
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])
            df.loc[len(df)]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)
            
    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/foxnews-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_foxnews.csv',index=False)


def get_HUFF_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/huffingtonpost/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            href = soup.head.find('link',{'rel':'canonical'})['href']
            dt = pd.to_datetime(soup.head.find('meta',{'name':'sailthru.date'})['content'])        
            texts = soup.find('div',{'id':'mainentrycontent'}).findAll('p')
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])

            df.loc[len(df)]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/huffingtonpost-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_huffingtonpost.csv',index=False)


def get_TIME_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/time/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            href = soup.head.find('link',{'rel':'canonical'})['href']
            dt = pd.to_datetime(soup.find('time',{'itemprop':'datePublished'})['datetime'])
            texts = soup.find('section',{'itemprop':'articleBody'}).findAll('p')
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])

            df.loc[len(df)]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/time-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_time.csv',index=False)


def get_WP_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/washingtonpost/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            href = soup.head.find('link',{'rel':'canonical'})['href']
            dt = pd.to_datetime(soup.find('span',{'class':'pb-timestamp'}).text)
            texts = soup.find('div',{'id':'article-body'}).findAll('p')
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])

            df.loc[len(df)]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/washingtonpost-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_washingtonpost.csv',index=False)


def get_CBS_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/CBSNews/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            href = soup.head.find('link',{'rel':'canonical'})['href']
            dt = pd.to_datetime(soup.find('span',{'class':'time'}).text)
            texts = soup.find('div',{'id':'article-entry'}).findAll('p')
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])

            df.loc[len(df)]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/CBSNews-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_CBSNews.csv',index=False)


def get_NBC_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/NBCNews/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            href = soup.head.find('link',{'rel':'canonical'})['href']
            dt = pd.to_datetime(soup.head.find('meta',{'name':'DC.date.issued'})['content'])
            texts = soup.find('div',{'class':'article-body'}).findAll('p')
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])

            df.loc[len(df)+1]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/NBCNews-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_NBCNews.csv',index=False)