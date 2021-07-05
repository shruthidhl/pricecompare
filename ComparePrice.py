import requests
import time
from pathlib import Path
from bs4 import BeautifulSoup
import threading
import configparser

searchwoolset = ["DMC Natura XL", "drops Saffron", "Drops Baby Merino Mix",
                 "Rooster Alpacca Speciale", "Stylecraft Special double knit requirements"]

# searchwoolset = ["DMC Natura XL", "drops Saffron"]

woolDictionary = {}


def crawl_html_content(eachWool, woolDictionary):
    woolDictionary[eachWool] = {}
    baseUrl = "https://www.wollplatz.de/wolle/"
    eachWoolElements = eachWool.split(" ")
    urlWoolTypeCore = eachWoolElements[0] + '/'
    urlWoolTypePart = ''
    for eachWoolElement in eachWoolElements:
        urlWoolTypePart += eachWoolElement + '-'
    toCallUrl = baseUrl + urlWoolTypeCore + urlWoolTypePart
    toCallUrl = toCallUrl[:-1]
    
    config = configparser.ConfigParser()
    config.read('ConfigFile.properties')
 

    page = requests.get(toCallUrl)
    #print(toCallUrl)
    if page.content.decode('utf-8').find("Oops! 404") == -1:
        soup = BeautifulSoup(page.content, "html.parser")
        zusammenStellung = soup.find(
            "td", text="Zusammenstellung").find_next_sibling("td").text
        
        woolDictionary[eachWool]["Zusammenstellung"] = zusammenStellung
        badges = soup.body.find('div', attrs={'id': 'ContentPlaceHolder1_upPricePanel'})
        print(badges)
        price=badges.find('span', itemprop = 'price').get_text()
        woolDictionary[eachWool]["price"] = price
        print(price)
        Nadelstärke = soup.find(
            "td", text="Nadelstärke").find_next_sibling("td").text
        print(Nadelstärke)
    else:
        woolDictionary[eachWool]["Zusammenstellung"] = "could not retrieve"


allThreads = []
for eachWool in searchwoolset:
    thread = threading.Thread(
        target=crawl_html_content, args=(eachWool, woolDictionary))
    thread.start()
    allThreads.append(thread)
    # crawl_html_content(eachWool)

for eachThread in allThreads:
    eachThread.join()

print(woolDictionary)




