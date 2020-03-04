from __future__ import division
import sys
import re
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx


def main():
    cmd = sys.argv
    textFile = None
    
    if len(cmd) == 1 and "project1.py" in cmd:
        print("'-preprocess': Reads the text file provided in the command line and\
returns the output.csv file of names and frequency. Text file must be provided as a command argument.")
        print()
        print("'-top n': Returns the top n number of names and their occurrences from the output.csv file. If output.csv\
does not exist or preprocess isn't being ran an error will occur.")
        print()
        print("'-graph10': For every pair of the top 10 characters, it will\
find the number of occurrences on the same line for each pair. Then these pair frequencies will be\
divided by the largest frequency among the pairs. For every pair, a graph connecting the pairs will be created\
and every pair that has a weight under 0.5 the connection will be dashed, and if over will be solid. The text file must\
also be provided in the command line.")
        print()
        
    if not check_pre_csv():
        raise Exception("Preprocess needs to be ran first.")

    for e in cmd:
        if ".txt" in e:
            textFile = cmd[cmd.index(e)]
    
    if "-preprocess" in cmd: 
        if textFile == None:
            raise Exception("Please enter the name of the text file.")
        preProcess(textFile)
     
    if "-top" in cmd:
        if check_pre_csv():
            topIndex = cmd.index("-top")
            topMax = int(cmd[topIndex+1])
            top(topMax)
        else:
            print("Preprocess needs to be ran first.")
    
    if "-graph10" in cmd: 
        if textFile == None:
            raise Exception("Please enter the name of the text file.")
        if check_pre_csv():
            graph10(textFile)
        else:
            print("Preprocess needs to be ran first.")
    
#process command   
def preProcess(wordFile):
    
    try:
        inFile = open(wordFile, "r", encoding='utf-8')
        stopFile = open("stopwords.txt", "r", encoding='utf-8')
        
        line = inFile.readline()
        stopWords = stopFile.read()
        
        names = {}
        
        while line != "":
            p = re.compile(r"!|@|#|\$|%|\^|&|\*|\(|\)|-|\+|=|{|}|\[|\]|:|;|\'|\"|<|>|,|\.|\?|\/|`|~|('s)|\n|\t")
            line2 = p.sub("", line)
            preList = re.split(r'[\W]+', line2)
            
            wordList = list(filter(lambda a: a != "", preList))
            
            i = 0
            while i < len(wordList):
                
                if wordList[i].istitle() and re.search(wordList[i],stopWords,re.IGNORECASE) == None:
                    if i < len(wordList)-1:
                        if wordList[i+1].istitle() and re.search(wordList[i+1],stopWords,re.IGNORECASE) == None:
                            
                            if (wordList[i]+" "+wordList[i+1]).lower().title() not in names.keys():
                                names[(wordList[i]+" "+wordList[i+1]).lower().title()] = 1
                                i += 2
                                    
                            else:   
                                names[(wordList[i]+" "+wordList[i+1]).lower().title()] += 1
                                i += 2
                                
                        else:
                            
                            if wordList[i].lower().title() not in names.keys():
                                names[wordList[i].lower().title()] = 1
                                i += 1
                                
                            else:
                                names[wordList[i].lower().title()] += 1
                                i += 1
                    else:
                        if wordList[i].lower().title() not in names.keys():
                            names[wordList[i].lower().title()] = 1
                            i += 1   
                        else:
                            names[wordList[i].lower().title()] += 1
                            i += 1
                else:
                    i += 1
            
               
            line = inFile.readline()
        
        extraKeys = []
        for e in names.keys():
            if len(e.split()) == 2 and names[e] > 5:
                for i in names.keys():
                    if i in e.split() and i != e:
                        extraKeys.append(i)
                        names[e] += names[i]
        
        for i in extraKeys:
            if i in names.keys():
                names.pop(i)
        
        reList = list(names.items())
        sortedList = sorted(reList, key = lambda x: x[1] if type(x[1])==int else x[2], 
                         reverse = True)
        
        writeCSV(sortedList, "output.csv")
        
    except IOError:
        print("Input file not found")
        
    finally:
        inFile.close()
        stopFile.close()

#Top Command
def top(num):
    
    with open("output.csv", "r") as csvFile:
        readFile = csv.reader(csvFile)
        maxNum = num
        count = 0
        
        for row in readFile:
            if count < maxNum:
                print(row[0]+", "+row[1])
                count += 1

#Graph Command
def graph10(wordFile):
    
    with open("output.csv", "r") as csvFile:
        readFile = csv.reader(csvFile)
        topDict = {}
        i = 0
        for row in readFile:
            if i < 10:
                topDict[row[0]] = row[1]
                i += 1
                
    pairList = pairs(topDict)
    pairDict = {}
    
    try:
        inFile = open(wordFile, "r", encoding = "utf-8")
        text = inFile.read()
        q = re.compile(r"\?|!")
        wordText = q.sub(".", text)
        sentenceList = list(filter(lambda a: a != "", wordText.split(".")))
        
        
        for line in sentenceList:
            p = re.compile(r"0|!|@|#|\$|%|\^|&|\*|\(|\)|-|\+|=|{|}|\[|\]|:|;|\'|\"|<|>|,|\.|\?|\/|`|~|('s)|\n|\t")
            line2 = p.sub("", line)

            
            for e in pairList:
                
                bothWords = len(e[0].split()) == 2 and len(e[1].split()) == 2
                firstWord = len(e[0].split()) == 2 and len(e[1].split()) == 1
                secondWord = len(e[0].split()) == 1 and len(e[1].split()) == 2
                
                if bothWords:
                    if (re.search(e[0],line2,re.IGNORECASE) != None or re.search(e[0].split()[1],line2,re.IGNORECASE)) != None and \
                        (re.search(e[1],line2,re.IGNORECASE) != None or re.search(e[1].split()[1],line2,re.IGNORECASE) != None):
                        if (e[0]+", "+e[1]) not in pairDict.keys():
                            pairDict[e[0]+", "+e[1]] = 1
                        else:
                            pairDict[e[0]+", "+e[1]] += 1
                
                elif firstWord:
                    if (re.search(e[0],line2,re.IGNORECASE) != None or re.search(e[0].split()[1],line2,re.IGNORECASE) != None) and \
                        re.search(e[1],line2,re.IGNORECASE) != None:
                        if (e[0]+", "+e[1]) not in pairDict.keys():
                            pairDict[e[0]+", "+e[1]] = 1
                        else:
                            pairDict[e[0]+", "+e[1]] += 1
                
                elif secondWord:
                    if re.search(e[0],line2,re.IGNORECASE) != None and \
                        (re.search(e[1],line2,re.IGNORECASE) != None or re.search(e[1].split()[1],line2,re.IGNORECASE) != None):
                        if (e[0]+", "+e[1]) not in pairDict.keys():
                            pairDict[e[0]+", "+e[1]] = 1
                        else:
                            pairDict[e[0]+", "+e[1]] += 1
                
                else:
                
                    if re.search(e[0],line2,re.IGNORECASE) != None and re.search(e[1],line2,re.IGNORECASE) != None:
                        if (e[0]+", "+e[1]) not in pairDict.keys():
                            pairDict[e[0]+", "+e[1]] = 1
                        else:
                            pairDict[e[0]+", "+e[1]] += 1        
        
           
        maxFreq = max(pairDict.values())

        for e in pairDict.keys():
            pairDict[e] /= maxFreq
        
        reList = list(pairDict.items())
        sortedList = sorted(reList, key = lambda x: x[1], reverse = True)
        for e in sortedList[0:3]:
            print(e)
        
        writeCSV(pairDict.items(), "weights.csv")
        
        
        G = nx.Graph()
        
        for names in pairDict.keys():
            chars = names.split(", ")
            G.add_edge(chars[0], chars[1], weight = pairDict[names])
        
          
        solidList = [(name1, name2) for (name1, name2, w) in G.edges(data = True) if w['weight'] >= 0.5]
        dashedList = [(name1, name2) for (name1, name2, w) in G.edges(data = True) if w['weight'] < 0.5]
        
        pos = nx.spring_layout(G)
         
        nx.draw_networkx_nodes(G,pos)
        nx.draw_networkx_edges(G,pos,edgelist= solidList, width=6)
        nx.draw_networkx_edges(G,pos,edgelist= dashedList, width=2.5, style='dashed', edge_color = 'b')
        nx.draw_networkx_labels(G,pos, font_size = 8)
        
        
        ax = plt.gca()
        ax.set_axis_off()
        
        plt.savefig("charactergraph.jpg")
        plt.show()
        
        
    except IOError:
        print("Text input file does not exist.")
        
    finally:
        inFile.close()



#Helper Functions
def writeCSV(data, fileName):
    try:
        outFile = open(fileName, "w", newline="")
        csvWriter = csv.writer(outFile)
        for e in data:
            csvWriter.writerow(e)
            
    except IOError:
        print("Error writing to csv file")
        
    finally:
        
        outFile.close()
        
def check_csv_file():
    try:
        testFile = open("output.csv","r")
        return True
    except IOError:
        return False
    finally:
        testFile.close()

def check_pre_process():
    cmd = sys.argv
    if "-preprocess" in cmd:
        return True
    return False

def check_pre_csv():
    if check_pre_process() or check_csv_file():
        return True
    return False
       
def pairs(dic):
    pairList = []
    keys = list(dic.keys())
    
    i = 0
    k = 1
    while i < len(keys):
        m = k
        while  m < len(keys):
            pairList.append([keys[i], keys[m]])
            m += 1
        i += 1
        k += 1
    
    return pairList
    
main()



