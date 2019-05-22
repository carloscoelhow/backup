import os
import bs4
import json
from time import sleep
from selenium import webdriver
import scrapy


driver = webdriver.Chrome()
url=['https://www.tripadvisor.es/Restaurant_Review-g187514-d13138415-Reviews-Restaurante_Etimo_by_Begona_Fraire-Madrid.html',
'https://www.tripadvisor.es/Restaurant_Review-g187514-d14030161-Reviews-Mr_Lupin-Madrid.html',
'https://www.tripadvisor.es/Restaurant_Review-g187514-d3418465-Reviews-or60-Fogon_Y_Candela-Madrid.html',
'https://www.tripadvisor.es/Restaurant_Review-g187514-d11741035-Reviews-Peko_Peko-Madrid.html']

data=[]
for i in url:
    driver.get(i)
    sleep(2)
    driver.find_element_by_css_selector("span.taLnk").click()
    sleep(5)
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    comments=soup.find_all('p', attrs={"class":"partial_entry"})
    comments= [j.text for j in comments]
    data.append(comments)
    sleep(1)
driver.close()

import json
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
