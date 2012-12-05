'''
Pulls the knights and knaves puzzles from http://philosophy.hku.hk/think/logic/knight.php

Created on Nov 29, 2012

@author: Toshi
'''
import re, string, urllib, os

from xml.parsers import expat

#from nltk.corpus import brown
#from nltk.chunk import RegexpParser


Queries = ["nephew","niece","relative","daughter","son","cousin","wife","married","marriage","birth","born","father","mother","brother","sister","child","children","parent","sibling","aunt","uncle"]



def extractRelationInfo(filename):
    corefDict = {}
    readsents = []
    texts = []
    from xml.dom import minidom
    xmldoc = minidom.parse(filename)
    itemlist = xmldoc.getElementsByTagName('s') 
    print len(itemlist)
    for s in itemlist:
        nordlist = s.getElementsByTagName('w')
        text,readsent = toText(nordlist, readsents)
        texts.append(text)
        readsents.append(readsent)
    return texts, readsents

def toText(nodelist, readsents):
    rc = []
    readsent = []
    result = ""
    idx = 0
    for node in nodelist:
        pos = node.attributes['pos'].value
        word = getText(node.childNodes)
        if pos == 'prp' and \
           (word.lower() != 'it' and word.lower() != 'its' and \
            word.lower() != 'that'):
            ref = getReference(pos,readsent,readsents)
            if ref != None:
                if pos == 'prp$':
                    ref = ref+"'s"
                rc.append(ref)
            else:
                rc.append(word)
        else:
            rc.append(word)
            
        #if pos == 'nnp' and len(nnps) == 0:
        #    v, name = lookAhead(nodelist,idx)
        #    if v:
        #        nnps.append(name)
                
        readsent.append((word,pos))
        idx += 1
        
    if len(rc) > 0:
        #print rc
        result = ' '.join(rc)
    return result, readsent
    
def lookAhead(nodelist, idx):
    name = []
    state = 1
    loop = 10
    count = 0
    while count < loop and count < len(nodelist[idx:]):
        node = nodelist[idx+count]
        pos = node.attributes['pos'].value
        name.append(getText(node.childNodes))
        state = transition(state,pos)
        if state == 9:
            break
        
    if state == 3:
        val = True
    else:
        val = False
        
    return val, ' '.join(name)

def lookBack(sent):
    name = []
    ref = None
    state = 1
    #print sent
    if len(sent) == 0:
        return ref
    
    for tup in sent:
        #print tup
        pos = tup[1]
        state = transition(state,pos)
        if state == 9 or state == 3:
            break
        if state == 2:
            name.append(tup[0])
        
    if state == 3:
        ref = ' '.join(name)
    print name
        
    return ref

def getReference(pos,readsent,readsents):
    ref = None
    loop = len(readsents)-1    
    verb = getVerb(readsent)
    if (pos == 'prp$' and (verb == 'is' or verb == 'was')) or len(readsent) == 0:
        #look at last sentence
        count = loop
        while count >= 0:
            ref = lookBack(readsents[count])
            if ref != None:
                break
            count -= 1
    else:
        #look at current sentence
        ref = lookBack(readsent)
        if ref == None:
            count = loop
            while count >= 0:
                ref = lookBack(readsents[count])
                if ref != None:
                    break
                count -= 1
                   
    return ref

def getVerb(sent):
    verb = None
    if len(sent) == 0:
        return verb
    
    for tup in sent:
        if tup[1] == 'vb' or verb == 'vbd' or verb == 'vbz':
            verb = tup[0]
            break
        
    return verb

def transition(state,pos):
    table = {1:{'nnp':2,'*':9},
             2:{'nnp':2,'vb':3,'vbz':3,'vbd':3,'md':3,'-lrb-':6,',':4,'rb':5,'*':9},
             3:{'*':3},
             4:{'nnp':2,'vb':3,'vbz':3,'vbd':3,'md':3,'*':9},
             5:{'vb':3,'vbz':3,'vbd':3,'md':3,'*':9},
             6:{'-rrb-':7,'*':6},
             7:{'vb':3,'vbz':3,'vbd':3,'md':3,'*':9},
             8:{'*':9},
             9:{'*':9}}
    nextstates = table[state]
    if nextstates.has_key(pos):
        state = nextstates[pos]
    else:
        state = nextstates['*']
    return state
    
def resolveRef(nnps):
    word = ''
    idx = len(nnps) - 1
    if idx > 0:
        word = nnps[idx]
    else:
        word = 'nnp of last sentence'
               
    return word

def getText(nodelist):
    rc = []
    result = ''
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            if node.data != '\n' and node.data != ' ':
                rc.append(node.data)
    if len(rc) > 0:
        result = ''.join(rc)
    return result

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
        if name == "the 44th and current President":
            corefDict[setid] = "Barack Obama"
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
    filename = "Barack_Obama1.xml"
    #files = [f for f in os.listdir('.')]
    files = [filename]
    for filename in files:
        texts, tups = extractRelationInfo(filename)
        saveFile('_obama.txt', ''.join(texts), 'txt')
        #saveFile(filename + '_tups', tups, 'txt')
        print filename
        #print texts
        #print tups
        #print corefDict

if __name__ == '__main__':
    main()
    
