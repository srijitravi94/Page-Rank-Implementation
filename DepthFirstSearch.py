
import urllib.request as ul
import re
from bs4 import BeautifulSoup
import time


BASE_URL = "https://en.wikipedia.org"
SEED_URL = "https://en.wikipedia.org/wiki/Tropical_cyclone"
GIVEN_DEPTH = 6
NO_OF_PAGES_TO_CRAWL = 1000
MAIN_PAGE = "https://en.wikipedia.org/wiki/Main_Page"


def getLinks(page, depth):
    listOfLinks = []
    webPage = ul.urlopen(page)                                        
    soup = BeautifulSoup(webPage, "html.parser")                      
    divData = soup.findAll('div')                                     
    header = soup.find('h1', { 'id' : 'firstHeading'}).text           
    for div in divData:
        links = div.findAll('a',{'href' : re.compile('^/wiki/')})     
        for link in links:
            fullURL = BASE_URL + link.get('href')
            if '#' not in fullURL and ':' not in link.get('href'):   
                listOfLinks.append(fullURL + str(depth))
    return listOfLinks, header


def addToList(mainset, subset):
    for i in range(len(subset)):
        mainset.insert(i, subset[i])


ddef crawler(seedURL):
    depth = 0
    seedURLString = str(seedURL) + str(depth)
    pagesToCrawl = [seedURLString]
    pagesCrawled = []
    linkHeadings = []
    count = 1
    while pagesToCrawl and len(pagesCrawled) < NO_OF_PAGES_TO_CRAWL:
        pageWithDepth = pagesToCrawl.pop(0)
        page = pageWithDepth[:len(pageWithDepth)-1]
        depth = int(pageWithDepth[-1])
        if page not in pagesCrawled:
            if depth < GIVEN_DEPTH:
                time.sleep(1)
                depth = depth + 1
                links, header = getLinks(page, depth)                            
                if header not in linkHeadings:                            
                    linkHeadings.append(header)
                    addToList(pagesToCrawl, links)
                    if page != MAIN_PAGE:
                        pagesCrawled.append(page)
                        print(str(count) + ". " + page + " : " + str(depth))
                        count +=1
    return pagesCrawled


def generateFile(listOfLinks):
    file = open("DFSCrawledURLs.txt", "w")
    for link in listOfLinks:
        file.write(link + "\n")
    file.close()


def main():
    listOfLinks = crawler(SEED_URL)
    generateFile(listOfLinks)
main()

