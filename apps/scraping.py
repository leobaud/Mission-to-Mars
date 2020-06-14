# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup

import pandas as pd
import requests
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver.exe", headless=True)
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres":hemispheres(browser),

        # "hemi_dict":hemi_dict,
        # "title1":title1,
        # "img1":img1,
        # "title2":title2,
        # "img2":img2,
        # "title3":title3,
        # "img3":img3,
        # "title4":title4,
        # "img4":img4,
        "last_modified":dt.datetime.now()
        }
   
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
   
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    try:
       slide_elem = news_soup.select_one('ul.item_list li.slide')
       # Use the parent element to find the first <a> tag and save it as `news_title`
       news_title = slide_elem.find("div", class_='content_title').get_text()
       # Use the parent element to find the paragraph text
       news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
       return None, None
    
    return news_title, news_p
    

# "### Featured Images"

def featured_image(browser):
    # Visit URL
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    # Use browser.links.find_by_partial_text instead

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        img_url_rel
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url
 
def mars_facts():
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    # pd.read_html scrapes entire table. automatically parse the table.[0] says to pull the first table it sees.
    # pd can covert DF back to html-ready code
    
    return df.to_html()


def hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser').find_all("a",class_ = "itemLink product-item")
    hemi_titles = []
    for i in soup:
        title = i.find("h3").text
        # link= i["href"]
        # or i.a["href"]
        hemi_titles.append(title)
    print(hemi_titles)
    # Visit hemispheres image URL
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    mars_hemis = []


    for x in range(len(hemi_titles)):
        try:
            browser.click_link_by_partial_text(hemi_titles[x])
            
        except:
            browser.find_link_by_text('2').first.click()
            browser.click_link_by_partial_text(hemi_titles[x])
        
        
        html = browser.html
        soup2 = BeautifulSoup(html, 'html.parser')
        hemi_soup = soup2.find('div', 'downloads')
        hemi_url = hemi_soup.a['href']
        hemi_title = soup2.find('h2', class_='title').text
        mars_hemis.append({'title':hemi_title,'img_url':hemi_url}) 
  

    
    return mars_hemis


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

    