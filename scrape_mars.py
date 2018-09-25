from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd

def scrape():

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_url = 'https://mars.nasa.gov/news/'
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars' 
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #def scrape():

    ##################################################################################
    # NASA Masrs News Section
    ##################################################################################

    browser.visit(mars_url)
    mars_html = browser.html
    mars_soup = bs(mars_html, 'html.parser')

    news_title = mars_soup.find('div', class_='content_title').text
    from time import sleep
    sleep(1)
    news_p = mars_soup.find('div', class_='article_teaser_body').text

    ##################################################################################
    # Mars Featured Image Section
    ##################################################################################

    browser.visit(jpl_url)

    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    article = jpl_soup.find('article')
    featured_image_url = ('https://www.jpl.nasa.gov' + article['style'][23:-3])

    ##################################################################################
    # Mars Weather Section
    ##################################################################################

    browser.visit(twitter_url)

    twitter_html =  browser.html
    twitter_soup =  bs(twitter_html, 'html.parser')

    mars_weather = twitter_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    ##################################################################################
    # Mars Facts Table
    ##################################################################################

    mars_facts = pd.read_html('https://space-facts.com/mars/')

    table = mars_facts[0]

    table.columns = ['Description', 'Value']

    table.set_index('Description', drop=True)

    table = table.to_html()

    ##################################################################################
    # Hemispheres Section
    ##################################################################################

    browser.visit(hemi_url)
    results = browser.find_by_css('div.description a.product-item')

    links = []

    for result in results:
            links.append({'title': result.text, 'img_dict': result['href']})


    hemisphere_image_urls = []

    for link in links:
            browser.visit(link['img_dict'])
            img_url = browser.find_by_css('img.wide-image')['src']
            hemisphere_image_urls.append({
                    'title': link['title'].replace(' Enhanced', ''),
                    'img_url': img_url,
            })

    scraped_data = {
    'News Title': news_title,
    'News Paragraph': news_p,
    'Featured Image': featured_image_url,
    'Mars Weather': mars_weather,
    'Hemispheres': hemisphere_image_urls,
    'Table': table
    }

    return scraped_data