# Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests


# Start Web Browser
def startBrowser():
    # executable path to driver 
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


# global container for Mars MongoDB
marsInfo = {}


# Mars News
def scrapeMarsNews():
    try:
        #Start browser
        browser = startBrowser()

        # Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML
        html = browser.html

        # Parse Beautiful Soup
        soup = BeautifulSoup(html, 'lxml')

        # latest news title and article paragraph
        newsTitle = soup.find('div', class_='content_title').find('a').text
        newsP = soup.find('div', class_='article_teaser_body').text

        # Push data to the Mars MongoDB
        marsInfo['newsTitle'] = newsTitle
        marsInfo['newsParagraph'] = newsP

        return marsInfo

    finally:

        browser.quit()

# Mars Images
def scrapeMarsImage():
    try:
        # Start browser
        browser = startBrowser()
        
        # Mars Space Images through splinter module
        featuredImageUrl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(featuredImageUrl)

        # HTML
        htmlImage = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(htmlImage, 'lxml')

        # Retrieve background-image url and remove the leading and trailing information
        featuredImageUrl  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        mainUrl = 'https://www.jpl.nasa.gov'

        # Create Web Link
        featuredImageUrl = mainUrl + featuredImageUrl

        # link of fullsize image
        # featuredImageUrl

        # Push data to the Mars MongoDB
        marsInfo['featuredImageUrl'] = featuredImageUrl

        return marsInfo

    finally:

        browser.quit()

# Mars Weather
def scrapeMarsWeather():
    try:
        # Start browser
        browser = startBrowser()

        # Mars Weather Twitter 
        weatherUrl = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weatherUrl)

        # HTML 
        htmlWeather = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(htmlWeather, 'lxml')

        # Find all elements that contain tweets
        latestTweet = soup.find_all('div', class_='js-tweet-text-container')

        # loop through tweets only use if contain weather info
        for tweet in latestTweet: 
            weatherTweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weatherTweet:
                # print(weatherTweet)
                break
            else: 
                pass

        # Push data to the Mars MongoDB
        marsInfo['weatherTweet'] = weatherTweet

        return marsInfo

    finally:

        browser.quit()

# Mars Facts
def scrapeMarsFacts():
    try:
        # Start browser
        browser = startBrowser()

        # Mars facts
        factsUrl = 'http://space-facts.com/mars/'

        # Pandas read_html
        marsFacts = pd.read_html(factsUrl)

        # Find the mars facts DataFrame
        marsDf = marsFacts[0]

        # Assign the columns
        marsDf.columns = ['Description','Value']

        # Save html code to folder Assets
        marsDf.to_html('Mars_Data.html', index=False)

        data = marsDf.to_dict(orient='records') 

        # Display
        # marsDf

        # Push data to the Mars MongoDB
        marsInfo['marsFacts'] = data

        return marsInfo
    
    finally:

        browser.quit()


# Mars hemisphere
def scrapeMarsHemispheres():
    try:
        # Start browser
        browser = startBrowser()

        # hemispheres website through splinter module 
        hemispheresUrl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheresUrl)

        # HTML Object
        htmlHemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(htmlHemispheres, 'lxml')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list 
        hemisphereImageUrls = []

        # main_ul 
        hemispheresMainUrl = 'https://astrogeology.usgs.gov'

        # Loop through
        for img in items: 
            # title
            title = img.find('h3').text
            
            # full image links
            partialUrl = img.find('a', class_='itemLink product-item')['href']
            
            # go to full image website 
            browser.visit(hemispheresMainUrl + partialUrl)
            
            # HTML Object of individual hemisphere
            partialImgHtml = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup(partialImgHtml, 'lxml')
            
            # Retrieve full image source 
            imgUrl = hemispheresMainUrl + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemisphereImageUrls.append({"title" : title, "img_url" : imgUrl})
            
        # Display hemisphere_image_urls
        # hemisphereImageUrls

        # Push data to the Mars MongoDB
        marsInfo['marsHemisphere'] = hemisphereImageUrls

        return marsInfo
    
    finally:

        browser.quit()



