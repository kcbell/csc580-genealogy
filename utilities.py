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
        if (pos == 'prp' or pos == 'prp$') and \
           (word.lower() != 'it' and word.lower() != 'its' and \
            word.lower() != 'that'):
            ref = getReference(word.lower(),pos,readsent,readsents)
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
    
def lookBack(word,wpos,sent):
    genderDict = {'they':'n','their':'n','them':'n',
                  'i':'n','my':'n','me':'n',
                  'we':'n','our':'n','us':'n',
                  'you':'n','your':'n','you':'n',
                  'he':'m','his':'m','him':'m',
                  'she':'f','her':'f',
                  'sister':'f','brother':'m',
                  'daughter':'f','son':'m',
                  'stepdaughter':'f','stepson':'m',
                  'mother':'f','father':'m',
                  'aunt':'f','uncle':'m',
                  'niece':'f','nephew':'m'}
    wgender = genderDict[word]
    gen = 'n'
    name = []
    ref = None
    state = 1
    #print sent
    if len(sent) == 0:
        return ref
    
    for tup in sent:
        #print tup
        pos = tup[1]
        noun = tup[0].lower()
        state = transition(state,pos)
        if state == 1 and pos == 'prp$' and word == noun:
            break
        if state == 9 or state == 3:
            break
        if state == 2:
            name.append(tup[0])
            if pos != 'nnp':
                if genderDict.has_key(noun):
                    gen = genderDict[noun]
        
        
    if state == 3:
        if (gen == wgender or gen == 'n') and wgender != 'n':
            ref = ' '.join(name)
            
    print name
        
    return ref

def getReference(word,pos,readsent,readsents):
    ref = None
    loop = len(readsents)-1    
    verb = getVerb(readsent)
    if (pos == 'prp$' and (verb == 'is' or verb == 'was')) or len(readsent) == 0:
        #look at last sentence
        count = loop
        while count >= 0:
            ref = lookBack(word,pos,readsents[count])
            if ref != None:
                break
            count -= 1
    else:
        #look at current sentence
        ref = lookBack(word,pos,readsent)
        if ref == None:
            count = loop
            while count >= 0:
                ref = lookBack(word,pos,readsents[count])
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
    #transition table for finite state machine
    table = {1:{'nnp':2,'nn':2,'prp$':1,'*':1,'in':8},
             2:{'nnp':2,'nn':2,'pos':2,'vb':3,'vbz':3,'vbd':3,'md':3,'-lrb-':6,',':4,'rb':5,'*':9},
             3:{'*':3},
             4:{'nnp':2,'vb':3,'vbz':3,'vbd':3,'md':3,'*':9},
             5:{'vb':3,'vbz':3,'vbd':3,'md':3,'*':9},
             6:{'-rrb-':7,'*':6},
             7:{'vb':3,'vbz':3,'vbd':3,'md':3,'*':9},
             8:{'*':8,',':1},
             9:{'*':9}}
    nextstates = table[state]
    if nextstates.has_key(pos):
        state = nextstates[pos]
    else:
        state = nextstates['*']
    return state
    
def getText(nodelist):
    rc = []
    result = ''
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            if node.data != '\n' and node.data != ' ':
                rc.append(node.data)
    if len(rc) > 0:
        result = ' '.join(rc)
    return result

def getName(nodelist):
    rc = []
    for node in nodelist:
        pos = node.attributes['pos'].value
        #if pos == "nnp":
        rc.append(getText(node.childNodes))
    return ' '.join(rc), pos
  

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
    f = fname.replace("xml",suffix)
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
    #filename = "Barack_Obama1.xml"
    files = [f for f in os.listdir('.') if re.match(r'.*\.xml$', f)]
    #files = [filename]
    for filename in files:
        texts, tups = extractRelationInfo(filename)
        saveFile('_'+filename, ' '.join(texts), 'txt')
        #saveFile(filename + '_tups', tups, 'txt')
        print filename
        #print texts
        #print tups
        #print corefDict

if __name__ == '__main__':
    main()
    
