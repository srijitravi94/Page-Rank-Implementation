import urllib.request as ul
import re
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
BASE_URL_WIKI = "https://en.wikipedia.org/wiki/"


def getLinks(page):
    listOfLinks = []
    webPage = ul.urlopen(page)
    soup = BeautifulSoup(webPage, "html.parser")
    divData = soup.findAll('div')
    for div in divData:
        links = div.findAll('a',{'href' : re.compile('^/wiki/')})
        for link in links:
            fullURL = BASE_URL + link.get('href')
            if '#' not in fullURL and ':' not in link.get('href'):
                listOfLinks.append(fullURL)
    return listOfLinks


def getAllLinks(fileName):
    file = open(fileName, "r").read()
    links = file.splitlines()
    count = 1
    linkDictionary = {}
    for link in links:
        linkDictionary[link] = getLinks(link)
        print(count)
        count +=1
    return linkDictionary


def extractName(page):
    docID = page[len(BASE_URL_WIKI):]
    return docID


def getInLinks(page, linkDictionary):
    inLinks = []
    links = linkDictionary.keys()
    for link in links:
        if page != link:
            if page in linkDictionary[link]:
                inLinks.append(str(" ") + str(extractName(link)))
    return inLinks


def getGraphs(linkDictionary, fileName):
    file = open(fileName, "r").read()
    links = file.splitlines()
    graph = []
    for link in links:
        inLinkString = ""
        inLinks = getInLinks(link, linkDictionary)
        for inLink in inLinks:
            inLinkString = inLinkString + str(inLink)
        graph.append(str(extractName(link)) + str(inLinkString))
    return graph


def writeFile(graph, fileName):
    file = open(fileName, "w")
    for inLink in graph:
        file.write(inLink + str("\n"))
    file.close()


def main():
    BFSlinkDictionary = getAllLinks("BFSCrawledURLs.txt")
    BFSgraph = getGraphs(BFSlinkDictionary, "BFSCrawledURLs.txt")
    writeFile(BFSgraph, "G1.txt")

    DFSlinkDictionary = getAllLinks("DFSCrawledURLs.txt")
    DFSgraph = getGraphs(DFSlinkDictionary, "DFSCrawledURLs.txt")
    writeFile(DFSgraph, "G2.txt")
main()