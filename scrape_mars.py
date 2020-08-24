from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import flask_pymongo as fpm
import requests as req
import time

def scrape():
	url = {}
	#nasa
	url['nasa'] = 'https://mars.nasa.gov/news/'
	executable_path = {'executable_path': 'C:/Users/trevo/chromedriver.exe'}
	browser = Browser('chrome', **executable_path, headless=False)
	browser.visit(url['nasa'])
	time.sleep(5) 
	html = browser.html
	nasa_soup = BeautifulSoup(html, 'html.parser')
	results = nasa_soup.find('div', class_="list_text")
	news_title = results.find('div', class_='content_title').text
	news_p = results.find('div', class_='article_teaser_body').text
	#jpl
	url['jpl'] = 'https://www.jpl.nasa.gov/'
	url['jpl_query'] = 'spaceimages/?search=&category=Mars'
	browser.visit(url['jpl'] + url['jpl_query'])
	browser.click_link_by_partial_text('FULL IMAGE')
	time.sleep(5) 
	jpl_soup = BeautifulSoup(browser.html, 'html.parser')
	image = jpl_soup.find('img', class_='fancybox-image')
	featured_img_url = url['jpl'][:-1] + image['src']
	#facts
	url['mars'] = 'https://space-facts.com/mars/'
	mars_tables = pd.read_html(url['mars'])
	facts_html = mars_tables[0].to_html()
	#hemispheres
	url['hemis']= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	hemisphere_image_urls = [
		{"title": "Valles Marineris Hemisphere", "img_url": "..."},
		{"title": "Cerberus Hemisphere", "img_url": "..."},
		{"title": "Schiaparelli Hemisphere", "img_url": "..."},
		{"title": "Syrtis Major Hemisphere", "img_url": "..."},
	]
	for dct in hemisphere_image_urls:
		 
		browser.visit(url['hemis'])
		browser.click_link_by_partial_text(dct['title'].split(' ')[0])
		time.sleep(5)
		hemi_soup = BeautifulSoup(browser.html, 'html.parser')
		downlows = hemi_soup.find('div',class_='downloads')
		dct['img_url'] = downlows.find_all('a')[1]['href']
	#output
	scraped_dict = {
		'news_title':news_title,
		'news_p':news_p,
		'featured_image_url':featured_img_url,
		'facts_html':facts_html,
		'hemisphere_image_urls':hemisphere_image_urls
	}
	browser.quit()
	return scraped_dict






