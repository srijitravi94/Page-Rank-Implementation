# Importing required libraries
import math
import os

# Declaring Global Variables

# P is the set of all pages |p| = N
P = []

# S is the set of sink nodes, i.e., pages that have no outlinks
S = []

# M(p) is the set (without duplicates) of pages that link to page p (pages and their inlinks)
M = {}

# L(q) is the number of outlinks (without duplicates) from page q
L = {}

# d is the PageRank damping/teleportation factor; d= 0.85 is a fairly typical value
d = 0.85

# PR is the set of pages and their respective page ranks
PR = {}

# newPR is the buffer set of pages and their respective page ranks
newPR = {}


# Function to extract pages and their inLinks
def generateInLinksDictionary(lines):
    for line in lines:
        listOfInLinks = line.split()
        page = listOfInLinks[0]
        inLinks = listOfInLinks[1:]
        M[page] = inLinks
    return M


# Function to extract graph content from a file
def parseFile(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    return lines


# Function to generate outLink count for a page
def generateOutLinkCount(page,M):
    L[page] = 0
    for q in M.keys():
        if page in M[q]:
            L[page] +=1
    return L


# Function to generate pages and their outLink counts
def generateOutLinksDictionary(M):
    for page in M.keys():
        L = generateOutLinkCount(page,M)
    return L


# Function to generate Sink Nodes i.e Pages with no outLinks
def generateSinkNodes(L):
    for page in L.keys():
        if L[page] == 0:
            S.append(page)
    return S


# Function to find Initial Page Rank
def findInitialRank(P):
    for page in P:
        PR[page] = 1/len(P)
    return PR


# Function to find the Shannon Entropy
def findShannonEntropy(PR):
    SE = 0
    for page in PR.keys():
         SE += (PR[page]*math.log2(PR[page]))
    return -1*SE


# Function to find perplexity which is 2 raised to the Shannon entropy
def findPerplexity(SE):
    perplexity = 2**(SE)
    return perplexity


# Function to check if the perplexity has converged
def hasConverged(prevPerplexity, currPerplexity):
    return abs(currPerplexity - prevPerplexity) < 1


# Function to calculate Page Rank
def calculatePageRank(M, P, L, S):
    PR = findInitialRank(P)
    N = len(P)
    initialSE = findShannonEntropy(PR)
    prevP = 0
    currP = findPerplexity(initialSE)
    converged = False
    count = 1
    perplexity = []
    while not converged:
        sinkPR = 0
        for page in S:									# calculate total sink PR
            sinkPR += PR[page]
        for p in P:
            newPR[p] = (1-d)/N  						# teleportation
            newPR[p] += d*sinkPR/N 						# spread remaining sink PR evenly
            for q in M[p]:								# pages pointing to p
                newPR[p] += d*PR[q]/L[q]				# add share of Page Rank from inLinks
        for p in P:
            PR[p] = newPR[p]
        prevP = currP
        currP = findPerplexity(findShannonEntropy(PR))	# finding the new perplexity
        count += 1
        if count >=4 and hasConverged(prevP, currP):	# checking if perplexity has converged
            converged = True
        else:
            converged = False
        perplexity.append(currP)
    return PR, perplexity


# Function to write Page Rank and Perplexity values to a file
def writeFile(PR, perplexity, fileName):
    PRfile = open(fileName[:-4] + "_PAGE_RANK_FOR_TOP_50_PAGES.txt", "w")
    PRCount = 0
    while PRCount<50:
        PRfile.write(str(PR[PRCount]) + "\n")
        PRCount += 1
    PRfile.close()
    perplexityFile = open(fileName[:-4] + "_PERPLEXITY_VALUES.txt", "w")
    for p in perplexity:
        perplexityFile.write(str(p) + "\n")
    perplexityFile.close()


# Function to generate Page Rank for a given graph
def generatePageRank(fileName):
    M = generateInLinksDictionary(parseFile(fileName))
    P = M.keys()
    L = generateOutLinksDictionary(M)
    S = generateSinkNodes(L)
    PR, perplexity = calculatePageRank(M, P, L, S)
    sortedPR = sorted(PR.items(), key=lambda x:x[1], reverse=True)
    writeFile(sortedPR, perplexity, fileName)


# Main function
def main():
    fileName = input("Enter File Path : ")				# In this case, G1.txt or G2.txt
    if os.path.exists(fileName):
        generatePageRank(fileName) 
        print("Number of pages with no OutLinks(Sinks) for " + fileName + " : " + str(len(S)))
    else:
        print("File not found") 
main()