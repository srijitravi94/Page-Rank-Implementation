def generateInLinkCount(fileName):
    noInLink = []
    inLinkDict = {}
    file = open(fileName, "r").read()
    links = file.splitlines()
    for link in links:
        pages = link.split()
        inLinkDict[pages[0]] = len(pages[1:])
        if(len(pages[1:]) == 0):
            noInLink.append(pages[0])
    return noInLink, inLinkDict


G1, G1Dict = generateInLinkCount("G1.txt")
print("Number of pages with no InLinks(Sources) for G1 : " + str(len(G1)))
G2, G2Dict = generateInLinkCount("G2.txt")
print("Number of pages with no InLinks(Sources) for G2 : " + str(len(G2)))


print(sorted(G1Dict.items(), key=lambda x:x[1], reverse=True)[:10])


print(sorted(G2Dict.items(), key=lambda x:x[1], reverse=True)[:10])

