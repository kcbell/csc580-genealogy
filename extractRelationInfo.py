'''
Pulls the knights and knaves puzzles from http://philosophy.hku.hk/think/logic/knight.php

Created on Nov 29, 2012

@author: Toshi
'''
import re, string, urllib, os

from xml.parsers import expat

#from nltk.corpus import brown
#from nltk.chunk import RegexpParser


Queries = ["daughter","son","cousin","wife","married","marrige","birth","born","father","mother","brother","syster","child","children","parent","sibling","aunt","uncle"]



def extractRelationInfo(filename):
    corefDict = {}
    texts = []
    from xml.dom import minidom
    xmldoc = minidom.parse(filename)
    itemlist = xmldoc.getElementsByTagName('s') 
    print len(itemlist)
    for s in itemlist:
        wordlist = toTuple(s.childNodes,corefDict)
        text = allToText(wordlist)
        val = isRelationship(text)
        if val:
            texts.append(wordlist)
        #texts.append(text)
        #print val,text
    return corefDict, texts

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def getName(nodelist):
    rc = []
    for node in nodelist:
        pos = node.attributes['pos'].value
        #if pos == "nnp":
        rc.append(getText(node.childNodes))
    return ' '.join(rc), pos

def solveCoref(corefDict, node):
    name,pos = getName(node.getElementsByTagName("w"))
    setid = node.attributes['set-id'].value
    if corefDict.has_key(setid):
         name = corefDict[setid]
         if pos == "prp$":
             name += "'s"
    else:
        corefDict[setid] = name
    return name, pos, corefDict

def allToText(wordlist):
    rc = []
    for word in wordlist:
        rc.append(word[0])
    return ' '.join(rc)

def toTuple(nodelist, corefDict):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            name = node.data
            #print name
            #print node
            if name != '\n':
                pos = node.parentNode.attributes['pos'].value
                rc.append((name,pos))
        else:
            if node.tagName == "coref":
                name, pos, corefDict = solveCoref(corefDict, node)
                if name != '\n':
                    rc.append((name, pos))
            else:
                rc.extend(toTuple(node.childNodes,corefDict))
    return rc
    

def isRelationship(text):
    query = '|'.join(Queries)
    match = re.findall(query,text)
    if len(match)>0:
        val = True
    else:
        val = False
    return val


def clean(html):
    sTag = '</font>'
    eTag = '<center>'
    html = html[html.find(sTag)+len(sTag):]
    html = html[:html.find(eTag)]
    
    tags = ["<p>","<i>","</i>","<blockquote>","</blockquote>"]
    for tag in tags:
        html = html.replace(tag,"")

    return html
            
def saveFile(fname, content, suffix):
    print fname
    f = fname.replace("htm",suffix)
    output_file = open(f,'w')
    output_file.write(content)
    output_file.close()
    return       

def openFile(f):
    input_file = open(f,'r')
    puz = input_file.read()
    input_file.close()
    return puz
           
def main():
    filename = "vol1ch02.xml"
    files = [f for f in os.listdir('./data/xml/')]
    #files = [filename]
    for filename in files:
        corefDict, text = extractRelationInfo("./data/xml/" + filename)
        print filename
        print text
        print corefDict

if __name__ == '__main__':
    main()
    
