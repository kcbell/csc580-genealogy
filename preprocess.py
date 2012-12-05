'''
Pulls the knights and knaves puzzles from http://philosophy.hku.hk/think/logic/knight.php

Created on Nov 26, 2012

@author: Toshi
'''
import re, string, urllib, os, nltk

#from nltk.corpus import brown
#from nltk.chunk import RegexpParser


URL = "http://en.wikipedia.org/w/api.php?format=xml&prop=extracts&explaintext=true&action=query&redirects=yes&titles="
SUBJECT = "Barack_Obama"

def getWikiContent(subject): 
    subjURL = subject.replace(" ", "_") 
    url = "http://en.wikipedia.org/w/api.php?format=xml&prop=extracts&explaintext=true&action=query&redirects=yes&titles=" + subjURL
    html = urllib.urlopen(url).read()
    raw = nltk.clean_html(html)
    raw = re.sub(r'\[.*\]', '', raw)
    raw = raw.replace('\n', ' ')
    return raw

def preProcess(text):
    page = SUBJECT
    #text = clean(text)
    chunks = chunkText(text)
    i = 0
    for chunk in chunks:
        i += 1
        chunk = clean(chunk)
        saveFile(page+str(i), chunk, "txt")
        saveFile(page+str(i), toXml(chunk), "xml")
        
    return i

def chunkText(text):
    chunks = []
    marker = "== Presidency =="
    idx = text.find(marker)
    chunks.append(text[:idx])
    chunks.append(text[idx+len(marker):])
    #chunks.append(text)
    return chunks

def clean(text):
    replaceList = [("Sr.","Sr"),("&quot;",'"'),('&amp;','and'),("&ndash;","-"),("&mdash;","-"),("II","2nd"),("III","3rd")]
    eTag = '   == Notes =='
    text = text[:text.find(eTag)]
    text = unicode(text,errors='ignore')
    #text = text.replace(u'\xe2','-')
    
    for item in replaceList:
        text = text.replace(item[0],item[1])
        
    format = "\s*==*.{3,100}==*\s"
    items = re.findall(format,text,flags=0)
    for item in items:
        text = text.replace(item, "")

    return text
            
def saveFile(fname, content, suffix):
    print fname
    f = fname+'.'+suffix
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
    text = getWikiContent(SUBJECT)
    print preProcess(text)

if __name__ == '__main__':
    main()
    
