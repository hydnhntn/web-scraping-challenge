def scrape():
    import pandas as pd
    from bs4 import BeautifulSoup
    import requests
    from splinter import Browser
    from webdriver_manager.chrome import ChromeDriverManager

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_data = {}


    # # NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    response = requests.get(url)
    soup = BeautifulSoup(browser.html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p

    # # JPL Mars Space Images - Featured Image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    response = requests.get(url)
    soup = BeautifulSoup(browser.html, 'html.parser')

    featured_image_url = soup.find('img', class_='headerimage fade-in')
    featured_image_url = url + featured_image_url['src']
    mars_data['featured_image_url'] = featured_image_url
    browser.quit()

    # # Mars Facts
    url = 'https://galaxyfacts-mars.com/'

    table = pd.read_html(url)[0]
    table.columns=['Description','Mars','Earth']
    table.set_index('Description', inplace=True)
    html_table = table.to_html(classes=" table-responsive table table-striped")
    mars_data['html_table'] = html_table

    # # Mars Hemispheres
    url = 'https://marshemispheres.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,  'html5lib')

    items = soup.find_all('div', class_='item')
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
        
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_data
