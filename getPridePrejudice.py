'''
Pulls the knights and knaves puzzles from http://philosophy.hku.hk/think/logic/knight.php

Created on Nov 15, 2012

@author: Toshi
'''
import re, string, urllib, os

#from nltk.corpus import brown
#from nltk.chunk import RegexpParser


URL = "http://www.austen.com/pride/"
PARAM = "qno=%d"
#NUM_PUZZLES = 25


def getPages():
    pages = []
    html = urllib.urlopen(URL).read()
    if len(html) == 0:
        print "Error: No html was read!"
        return pages
    print html
    sTag = '<li><a href="'
    eTag = '">'
    idx1 = html.find(sTag)
    while idx1 > -1 and len(html) > 0:
        html = html[idx1+len(sTag):]
        idx2 = html.find(eTag)
        pages.append(html[:idx2])
        html = html[idx2+len(eTag):]
        idx1 = html.find(sTag)

    return pages

def getChapters(pages):
    texts = []
    for page in pages:
        html = urllib.urlopen(URL+page).read()
        if len(html) == 0:
            print "rror: No html was read!"
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
    pages = getPages()
    print pages
    texts = getChapters(pages)
    print len(texts), texts[-1]

if __name__ == '__main__':
    main()
    
