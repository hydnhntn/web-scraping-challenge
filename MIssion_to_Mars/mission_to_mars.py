#!/usr/bin/env python
# coding: utf-8

# In[144]:


import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[145]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

mars_data = {}


# # NASA Mars News

# In[146]:


# URL of page to be scraped
url = 'https://redplanetscience.com/'
browser.visit(url)

# retrieve page with the reqests module
response = requests.get(url)
# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(browser.html, 'html.parser')


# In[147]:


news_title = soup.find('div', class_='content_title').text
news_p = soup.find('div', class_='article_teaser_body').text
print(news_title)
print(news_p)
mars_data['news_title'] = news_title
mars_data['news_p'] = news_p
print(f"mars_data = {mars_data}")
#browser.quit()


# # JPL Mars Space Images - Featured Image

# In[148]:


# URL of page to be scraped
url = 'https://spaceimages-mars.com/'
browser.visit(url)

# retrieve page with the reqests module
response = requests.get(url)
# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(browser.html, 'html.parser')


# In[149]:


featured_image_url = soup.find('img', class_='headerimage fade-in')
featured_image_url = url + featured_image_url['src']
print(featured_image_url)
mars_data['featured_image_url'] = featured_image_url
print(f"mars_data = {mars_data}")
browser.quit()


# # Mars Facts

# In[150]:


url = 'https://galaxyfacts-mars.com/'

table = pd.read_html(url)[1]
table.columns=['Attribute','Value']
table


# In[151]:


html_table = table.to_html()
html_table
mars_data['html_table'] = html_table
print(f"mars_data = {mars_data}")


# # Mars Hemispheres

# In[152]:


# URL of page to be scraped
url = 'https://marshemispheres.com/'
#browser.visit(url)

# retrieve page with the reqests module
response = requests.get(url)

# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text,  'html5lib')


# In[153]:


items = soup.find_all('div', class_='item')
titles = []
img_urls = []
hemisphere_image_urls = []
for item in items:
    dict = {}
    desc = item.find('div', class_='description')
    
    title = desc.find('a').text.strip().strip(' Enhanced')
    dict['title']= title
    
    img = item.find('img', class_='thumb')
    img_url = url + img['src']
    dict['img_url']= img_url
    
    hemisphere_image_urls.append(dict)
    
print(hemisphere_image_urls)
mars_data['hemisphere_image_urls'] = hemisphere_image_urls
print(f"mars_data = {mars_data}")


# In[154]:


import pymongo


# In[155]:


conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.marsMission
col = db.mars


# In[160]:


col.update_one({}, {"$set": mars_data}, upsert=True)


# In[ ]:




