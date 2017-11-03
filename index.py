# Python 2.7.3
# -*- coding: latin-1 -*-
import re
import os
import collections
import time

# This is the map where dictionary terms will be stored as keys and value will be posting list with position in the file
dictionary = {}
matrix = {}
# This is the map of docId to input file name
docIdMap = {}


class index:
    def __init__(self, path):
        self.path = path
        pass

    def buildIndex(self):

        docId = 1
        fileList = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        fileobj = open('frequency.txt', 'w')
        fileobj1 = open('matrix.txt', 'w')
        for eachFile in fileList:
            position = 1
            count = 0
            # docName = "Doc_Id_" + str(docId)
            # docName =  str(docId)
            docIdMap[docId] = eachFile
            lines = [line.rstrip('\n') for line in open(self.path + "/" + eachFile)]

            for eachLine in lines:
                wordList = re.split('\W+', eachLine)

                while '' in wordList:
                    wordList.remove('')
                for word in wordList:
                    if (word.lower() in dictionary):
                        postingList = dictionary[word.lower()]
                        if (docId in postingList):
                            postingList[docId].append(position)
                            position = position + 1
                        else:
                            postingList[docId] = [position]
                            position = position + 1
                    else:
                        dictionary[word.lower()] = {docId: [position]}
                        position = position + 1
            docId = docId + 1
        #lengths = {key:len(value) for key,value in dictionary.iteritems()}
        length_dict = {key: len(value) for key, value in dictionary.items()}
        for w in length_dict:
            fileobj.write(w +"   |   "+str(length_dict[w]))
            fileobj.write("\n")
        fileobj.close()


        firstLine = "          **|**   "
        for d in docIdMap:
            firstLine = firstLine + " | " +str(d)
        fileobj1.write(firstLine+"   **|** ")
        fileobj1.write('\n')
        fileobj1.write('\n')
        for t in dictionary:
            poList = dictionary[t]
            kList = []
            for keys in poList:
                kList.append(keys)
            line = "       "

            for d in docIdMap:
                if d in kList:
                    line = line + " | " + "1"
                else:
                    line = line + " | " + "0"

            fileobj1.write(t+"  **|**"+line)
            fileobj1.write('\n')

        fileobj1.close()

    def and_query(self, query_terms):
        if len(query_terms) == 1:
            resultList = self.getPostingList(query_terms[0])
            if not resultList:
                print ""
                printString = "Result for the Query : " + query_terms[0]
                print printString
                print "0 documents returned as there is no match"
                return

            else:
                print ""
                printString = "Result for the Query : " + query_terms[0]
                print printString
                print "Total documents retrieved : " + str(len(resultList))
                for items in resultList:
                    print docIdMap[items]

        else:
            resultList = []
            for i in range(1, len(query_terms)):
                if (len(resultList) == 0):
                    resultList = self.mergePostingList(self.getPostingList(query_terms[0]),
                                                       self.getPostingList(query_terms[i]))
                else:
                    resultList = self.mergePostingList(resultList, self.getPostingList(query_terms[i]))
            print ""
            printString = "Result for the Query(AND query) :"
            i = 1
            for keys in query_terms:
                if (i == len(query_terms)):
                    printString += " " + str(keys)
                else:
                    printString += " " + str(keys) + " AND"
                    i = i + 1

            print printString
            print "Total documents retrieved : " + str(len(resultList))
            for items in resultList:
                print docIdMap[items]

    def getPostingList(self, term):
        if (term in dictionary):
            postingList = dictionary[term]
            keysList = []
            for keys in postingList:
                keysList.append(keys)
            keysList.sort()
            # print keysList
            return keysList
        else:
            return None

    def mergePostingList(self, list1, list2):

        mergeResult = list(set(list1) & set(list2))
        mergeResult.sort()
        return mergeResult

    def print_dict(self):
        # function to print the terms and posting list in the index
        fileobj = open("invertedIndex.txt", 'w')
        for key in dictionary:
            print key + " --> " + str(dictionary[key])
            fileobj.write(key + " --> " + str(dictionary[key]))
            fileobj.write("\n")
        fileobj.close()

    def print_doc_list(self):
        for key in docIdMap:
            print "Doc ID: " + str(key) + " ==> " + str(docIdMap[key])


def main():
    docCollectionPath = raw_input("Enter path of text file collection : ")
    queryFile = raw_input("Enter path of query file : ")
    indexObject = index(docCollectionPath)
    indexObject.buildIndex()

    print ""
    print "Inverted Index :"
    indexObject.print_dict()

    print ""
    print "Document List :"
    indexObject.print_doc_list()
    print ""

    QueryLines = [line.rstrip('\n') for line in open(queryFile)]
    for eachLine in QueryLines:
        wordList = re.split('\W+', eachLine)

        while '' in wordList:
            wordList.remove('')

        wordsInLowerCase = []
        for word in wordList:
            wordsInLowerCase.append(word.lower())
        indexObject.and_query(wordsInLowerCase)

if __name__ == '__main__':
    main()
