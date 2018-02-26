
# coding: utf-8

# ## Mission to Mars
# 
# ### Step 1 - Scraping

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd

# ### NASA Mars News

# In[2]:

def init_chrome():
    executable_path = {'executable_path': 'C:\\Users\Jagatha\Downloads\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def get_latest_news():
    
    browser = init_chrome()
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    browser.quit()

    # Get the latest news title
    results = soup.find('div', class_='content_title')
    news_title = results.text.strip()
    print(news_title)

    # Get the Paragragh Text
    news_text = soup.find('div', class_='article_teaser_body').get_text()
    print(news_text)
    return news_title, news_text

# ### JPL Mars Space Images - Featured Image

def get_featured_img():
    browser = init_chrome()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Navigate to the page 
    X = True
    while (X):
        try:
            browser.click_link_by_partial_text('FULL IMAGE')
            X = False
        except Exception as e:
            print(e)
            X = True
        
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.quit()

    result = soup.find('a', class_='button fancybox')
    base_url = 'https://www.jpl.nasa.gov'
    image_rel_path = result.get('data-fancybox-href')

    featured_image_url = base_url + image_rel_path
    print(featured_image_url)
    return featured_image_url

# ### Mars Weather

def get_mars_weather():
    browser = init_chrome()
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.quit()

    results = soup.find('div', class_='js-tweet-text-container')
    mars_weather = results.p.text.strip()
    print(mars_weather)
    return mars_weather

# ## Mars Facts

# * We can use the read_html function in Pandas to automatically scrape any tabular data from a page.
def get_mars_facts():
    facts_url = 'http://space-facts.com/mars/'
    tables = pd.read_html(facts_url)

    facts_df = tables[0]
    facts_df.columns = ['Description', 'Value']
    facts_df = facts_df.set_index("Description")
    # facts_df.to_html('table.html', index=False)
    facts_table = facts_df.to_html()
    facts_table = facts_table.replace('\n', '')
    return facts_table

# ## Mars Hemisperes

def get_hemisphere_img():
    browser = init_chrome()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.find_all('div', class_='item')
    hemisphere_image_urls = []

    for link in links:
        title = link.h3.text
        print(title)
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find('div', class_='downloads')
        img_url = results.a['href']
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        print(img_url)
        browser.back()
    
    browser.quit()
    # print(hemisphere_image_urls)

    return hemisphere_image_urls

def scrape():
    mars_data = {}
    news_title, news_text = get_latest_news()
    featured_image_url = get_featured_img()
    mars_weather = get_mars_weather()
    facts_table = get_mars_facts()
    hemisphere_image_urls = get_hemisphere_img()

    mars_data = {"latest_news": news_title,
                "news_text": news_text,
                "facts": facts_table,
                "featured_image_url": featured_image_url,
                "mars_weather": mars_weather,
                "hemisphere_image_urls": hemisphere_image_urls}

    return mars_data