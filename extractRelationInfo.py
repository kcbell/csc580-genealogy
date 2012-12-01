'''
Pulls the knights and knaves puzzles from http://philosophy.hku.hk/think/logic/knight.php

Created on Nov 29, 2012

@author: Toshi
'''
import re, string, urllib, os

from xml.parsers import expat

#from nltk.corpus import brown
#from nltk.chunk import RegexpParser


Queries = ["father","mother","brother","syster","child","children","parent","sibling","aunt","uncle"]



def extractRelationInfo(filename):
    corefDict = {}
    texts = []
    from xml.dom import minidom
    xmldoc = minidom.parse(filename)
    itemlist = xmldoc.getElementsByTagName('s') 
    print len(itemlist)
    for s in itemlist:
        #print s.getElementsByTagName("w")
        for w in s.getElementsByTagName("coref"):
            #name = ""
            name,pos = getName(w.getElementsByTagName("w"))
            #if pos == "nnp":
            setid = w.attributes['set-id'].value
            if not corefDict.has_key(setid):
                corefDict[setid] = name
        text = allToText(s.childNodes,corefDict)
        val = isRelationship(text)
        if val:
            texts.append(text)
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
    return ''.join(rc), pos

def allToText(nodelist,mydict):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
        else:
            if node.tagName == "coref":
                setid = node.attributes['set-id'].value
                rc.append(mydict[setid])
            else:
                rc.append(allToText(node.childNodes,mydict))
    return ' '.join(rc)

def isRelationship(text):
    query = '|'.join(Queries)
    match = re.findall(query,text)
    if len(match)>0:
        val = True
    else:
        val = False
    return val

def getChapters(pages):
    texts = []
    for page in pages:
        html = urllib.urlopen(URL+page).read()
        if len(html) == 0:
            print "Error: No html was read!"
        else:
            text = clean(html)
            texts.append(text)
            saveFile(page, text, "txt")
            saveFile(page, toXml(text), "xml")

    return texts


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

def toXml(text):
    svUrl = "http://localhost:8125/BARTDemo/ShowText/process/"
    xml = urllib.urlopen(svUrl, text).read()
    return xml
            
def main():
    filename = "./data/xml/vol1ch02.xml"
    files = [f for f in os.listdir('./data/xml/')]
    for filename in files:
        corefDict, text = extractRelationInfo("./data/xml/" + filename)
        print filename
        print text

if __name__ == '__main__':
    main()
    
