from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    app_info = {}
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
 
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    slide_elem.find("div", class_="content_title")
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    app_info['headline'] = news_title
    app_info['paragraph'] = news_p

    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_url_rel = img_soup.find('img', class_='fancybox-image')['src']
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    app_info['image'] = img_url


    df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace = True)
    app_info['table'] = df.to_html()

    url = 'https://marshemispheres.com/'

    browser.visit(url)
    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item img')
    for i in range(len(links)):
        href_dict = {}
        browser.find_by_css('a.product-item img')[i].click()
        sample = browser.find_by_text('Sample').first
        href_dict["url"]= sample['href']    
        href_dict['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(href_dict)
        browser.back()
    
    app_info['hemi_info'] = hemisphere_image_urls
    browser.quit()
    return app_info