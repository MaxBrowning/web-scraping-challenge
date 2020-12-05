# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    ### VISIT MARS NEWS ###
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get the first news article
    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find('div', class_='article_teaser_body').text

    ### VISIT MARS SPACE IMAGES ###
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Navigate to featured image page
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()

    # HTML Object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve main image url address
    feat_img = soup.find('img', class_='main_image')['src']

    ### VISIT MARS FACTS PAGE ###
    url = 'https://space-facts.com/mars/'

    # Use Panda's 'read_html' to parse the url
    tables = pd.read_html(url)

    # Find the Mars Facts table in the list and assign it to 'mars_df'
    mars_df = tables[0]
    mars_df.columns = ['Description', 'Mars']
    mars_df.set_index('Description', inplace=True)

    # Convert dataframe to HTML
    mars_facts_table = mars_df.to_html()

    ### VISIT MARS HEMISPHERES PAGE ###
    # Create list to store dictionaries
    hemisphere_image_urls = []

    # Iterate through all images
    for x in range(4):

        # URL of page to be scraped
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

        # Retrieve page with the requests module
        browser.visit(url)

        # Navigate to featured image page
        browser.links.find_by_partial_text('Hemisphere Enhanced')[x].click()

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Scrape image URL
        hemisphere_img_url = soup.find('img', class_='wide-image')['src']
        hemisphere_title = soup.find('h2', class_='title').text
        
        # Create dictionary
        hemisphere_dictionary = {
            'title': hemisphere_title,
            'img_url': hemisphere_img_url
        }
        
        # Append list with dictionary
        hemisphere_image_urls.append(hemisphere_dictionary)

    # Store all data in the dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "feat_img": feat_img,
        "mars_facts_table": mars_facts_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict