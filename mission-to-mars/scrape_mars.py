#dependencies
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from flask_pymongo import PyMongo

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    
    browser = init_browser()
    
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find_all("div", class_="content_title")[0].text
    news_p = soup.find_all("div", class_="article_teaser_body")[0].text

    #JPL Mars Space Images
    url = "https://spaceimages-mars.com/"
    image_url = "https://spaceimages-mars.com/image/mars/Icaria%20Fossae7.jpg"
    browser.visit(image_url)
    featured_image_url = url + image_url
    featured_image_url

    #Mars Facts
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)
    tables = pd.read_html(url)
    mars_facts = tables[0]
    mars_facts = mars_facts[[0, 1]]
    mars_facts = mars_facts.rename(columns={0:"", 1:"Mars Data"})

    #Mars Hemispheres
    hemisphere_image_urls = []

    url = "https://marshemispheres.com/"
    browser.visit(url)
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    mars_hemispheres = soup.find("div", class_="collapsible results")
    hemisphere = mars_hemispheres.find_all("div", class_="item")

    for i in hemisphere:

        #scrape title for each hemisphere 
        mars = i.find("div", class_="description")
        title = mars.h3.text

        #scrape link for each hemisphere
        link = mars.find("a") ["href"]
        browser.visit(url + link)

        html = browser.html
        soup = bs(html, 'html.parser')

        img_link = soup.find("div", class_="downloads")
        hemisphere_img = img_link.find("li").a["href"]


        image_dictionary = {}

        image_dictionary["title"] = title
        image_dictionary["image_url"] = hemisphere_img


        hemisphere_image_urls.append(image_dictionary)
        
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": str(mars_facts),
        "mars_hemispheres": hemisphere_image_urls
       }

    








