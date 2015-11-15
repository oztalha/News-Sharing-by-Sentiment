# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 14:41:42 2015

@author: Talha
"""

import pandas as pd
from glob import glob

# ==========================
# LIWC Input Preparation !!!
# Done once, doing again corrupts the files
# ==========================
dfs = []
for f in glob('data/tw-news/*.csv'):
    df = pd.read_csv(f)
    df['outlet'] = f.split('\\')[-1].split('-')[0]
    dfs.append(df)
df = pd.concat(dfs)
df.to_csv('data/tw-news/tweeted-news.csv',index=False,encoding='utf-8')

dfs = []
for f in glob('data/tweets/*.csv'):
    df = pd.read_csv(f)
    df['outlet'] = f.split('\\')[-1].split('.')[0]
    dfs.append(df)
df = pd.concat(dfs)
df.to_csv('data/tweets/tweet-texts.csv',index=False,encoding='utf-8')


# ==========================
# LIWC Results Cleaning !!!
# Done once, doing again corrupts the files
# ==========================
#25599 unique tweets
tw = pd.read_csv('data/LIWC/LIWC2015 Results (tweet-texts).csv',encoding='utf-8')
rename = dict(zip(tw.ix[0][:8].index,tw.ix[0][:8].values))
tw = tw.rename(columns=rename)
tw = tw.drop(0)
tw.to_csv('data/LIWC/LIWC2015 Results (tweet-texts).csv',index=False,encoding='utf-8')

#35930 unique news from lexis-nexis
pn = pd.read_csv('data/LIWC/LIWC2015 Results (published).csv')
pn = pn.rename(columns={'Source (A)':'dt','Source (B)':'outlet','Source (C)':'story'})
pn = pn.drop([0,1])
pn.to_csv('data/LIWC/LIWC2015 Results (published).csv',index=False,encoding='utf-8')
published = pn.drop('story',axis=1)
published.to_csv('data/pb-sp.csv',index=False)

#16376 unique news from tweets
tn = pd.read_csv('data/LIWC/LIWC2015 Results (tweeted-news).csv',encoding='utf-8')
rename = dict(zip(tn.ix[0][:6].index,tn.ix[0][:6].values))
tn = tn.rename(columns=rename)
tn = tn.drop(0)
tn.to_csv('data/LIWC/LIWC2015 Results (tweeted-news).csv',index=False,encoding='utf-8')
tweeted = tn.drop('newstxt',axis=1)
tweeted.to_csv('data/LIWC/tweeted-no-story.csv',index=False,encoding='utf-8')


# ==========================
# Combining tweets with news !!!
# Done once, doing again corrupts the files
# ==========================
tw = pd.read_csv('data/LIWC/LIWC2015 Results (tweet-texts).csv',encoding='utf-8')
tn = pd.read_csv('data/LIWC/LIWC2015 Results (tweeted-news).csv',encoding='utf-8')

#urls in tn needs to match the fname in tw
def get_url2(url):
    try:
        return url.split(' ')[1].split('/')[-1]
    except:
        return ''

def get_url1(url):
    try:
        return url.split(' ')[0].split('/')[-1]
    except:
        return ''

tw['u1'] = tw.url.apply(get_url1)
tw['u2'] = tw.url.apply(get_url2)
#merge fname with the first url
u1 = tw.merge(tn,left_on='u1',right_on='fname',suffixes=('_t',''))
#merge fname with the second url
u2 = tw.merge(tn,left_on='u2',right_on='fname',suffixes=('_t',''))
#combine them
df = pd.concat([u1,u2])
df = df.drop(['outlet_t','u1','u2'],axis=1)
df = df.drop_duplicates('twid') #3 among 16912 records: 1 cnn, 1 wapo, 1 fox
df.to_csv('data/LIWC/tweets-news-combined.csv',index=False,encoding='utf-8')
df = df.drop('newstxt',axis=1)
df.to_csv('data/tw-sp.csv',index=False,encoding='utf-8')


"""
The following code is to fix some canonical urls in foxnews hrefs
import requests
from bs4 import BeautifulSoup

df = pd.read_csv('data/LIWC/tweets-news-combined.csv',encoding='utf-8')
href= dict()
urls = {}
for url in urls:
    try:
        soup = BeautifulSoup(requests.get(url).text, "lxml")
        href[url] = soup.head.find('meta',{'property':'vr:canonical'})['content']
        print('[OK]',url)
    except:
        href[url] = 'business'
        print('[ERROR]',url)
    
to_rep = []
rep_with = []
for k,v in urls.items():
    to_rep.append(k)
    rep_with.append(href[v])
df.href = df.href.replace(to_replace=to_rep,value=rep_with)
"""
df2 = pd.read_csv('data/LIWC/tweets-news-combined.csv',encoding='utf-8')
df.ix[df.href=='business','href'] = df2.ix[df2.url.str.contains('|'.join(bs))].href
df.outlet.replace('WaPo','WPOST',inplace=True)

def getCat(x):
    pieces = [piece.lower() for piece in x.href.split('/')]
    if x.outlet == 'CNN':
        if 'golf' in pieces[-3] or 'sport' in pieces[-3]:
            return 'sports'
        if pieces[-3]=='tech':
            return 'technology'
        return pieces[-3]
    elif x.outlet == 'NYT':
        if x.href.startswith('http://www.nytimes.com/video/'):
            return pieces[-3]
        if 'blogs.nytimes.com' in x.href:
            return 'blog'
        if 'politics' in x.href:
            return 'politics'        
#        if 'business' in x.href:            
#            return 'business'
        if 'what-were-reading' in x.href:
            print(x.href)
            return 'blog'
        if pieces[-2]=='international':
            return 'world'
        if 'ball' in pieces[-2] or 'tennis' in pieces[-2] or 'golf' in pieces[-2]:
            return 'sports'
        if 'dealbook' in x.href:
            return 'deal'
        if 'oscars-2015-live-blog' in pieces[-2] or 'dance' in pieces[-2]:
            return 'entertainment'
        return pieces[-2]
    elif x.outlet == 'ABC':
        if pieces[3]=='international':
            return 'world'
        return pieces[-3]
    elif x.outlet == 'NBCNews':
        if pieces[3]=='news':
            return pieces[4] if pieces[4]!='us-news' else 'us'
        if pieces[3]=='meet-the-press':
            return 'interview'
        if pieces[3]=='tech':
            return 'technology'
        return pieces[3]
    elif x.outlet == 'CBSNews':
        return pieces[-3]
    elif x.outlet == 'FoxNews':
        if x.href.startswith('http://www.foxbusiness.com'):
            return 'business'
        if x.href.startswith('http://nation.foxnews.com'):
            return 'blog'
        if x.href.startswith('http://latino.foxnews.com'):
            return 'latino'
        if pieces[3]=='tech':
            return 'technology'
        return pieces[3]
    elif x.outlet == 'AP':
        if x.href.startswith('http://bigstory.ap.org'):
            return 'bigstory'
        return pieces[-3]
    elif x.outlet == 'WPOST':
        if x.href.startswith('http://www.washingtonpost.com/blogs/'):
            return 'blog'
        return pieces[3] if pieces[3]!='pb' else pieces[4]


df['cat'] = df.apply(getCat,axis=1)
category = pd.pivot_table(df,index=["cat"],values=["href"],aggfunc=len).sort('href',ascending=False)
bf= df[df.cat.isin(category[category.href>1].index)]
b = pd.pivot_table(bf,index=["cat"],columns=['outlet'],values=["href"],aggfunc=len)
b = b.fillna('')
b

df= df.drop('newstxt',axis=1)
df.to_csv('data/tw-sp.csv',index=False,encoding='utf-8')