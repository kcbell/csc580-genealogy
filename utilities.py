'''
Pulls the knights and knaves puzzles from http://philosophy.hku.hk/think/logic/knight.php

Created on Nov 29, 2012

@author: Toshi
'''
import re, string, urllib, os, nltk

from xml.parsers import expat

#from nltk.corpus import brown
#from nltk.chunk import RegexpParser


Queries = ["nephew","niece","relative","daughter","stepdaughter","son","stepson",
           "cousin","wife","married","birth","father","mother",
           "stepfather","stepmother","brother","sister","stepbrother","stepsister",
           "child","children","parent","grandparent","sibling","aunt","uncle"]



def extractRelationInfo(filename):
    corefDict = {}
    readsents = []
    tupsents = []
    texts = []
    from xml.dom import minidom
    xmldoc = minidom.parse(filename)
    itemlist = xmldoc.getElementsByTagName('s') 
    print len(itemlist)
    for s in itemlist:
        nordlist = s.getElementsByTagName('w')
        text,readsent,tupsent = toText(nordlist, readsents)
        texts.append(text)
        readsents.append(readsent)
        tupsents.append(tupsent)
    return texts, readsents, tupsents

def toText(nodelist, readsents):
    rc = []
    readsent = []
    tupsent = []
    result = ""
    couple = False
    idx = 0
    ref = None
    for node in nodelist:
        pos = node.attributes['pos'].value
        word = getText(node.childNodes)
        if word == 'couple':
            word = 'they'
            pos = 'prp'
            couple = True
            
        if (pos == 'prp' or pos == 'prp$') and \
           (word.lower() != 'it' and word.lower() != 'its' and \
            word.lower() != 'that'):
            ref = getReference(word.lower(),pos,readsent,readsents)
            if ref != None:
                if pos == 'prp$':
                    ref = ref+"'s"
                if couple:
                    if rc[-1].lower() == 'the':
                        rc = rc[:-1]
                        tupsent = tupsent[:-1]
                    couple = False
                rc.append(ref)
                tupsent.append((ref,'rep'))
            else:
                rc.append(word)
                tupsent.append((word,pos))
        else:
            rc.append(word)
            tupsent.append((word,pos))
            
           
        readsent.append((word,pos))
        idx += 1
        
    if len(rc) > 0:
        #print rc
        result = ' '.join(rc)
    return result, readsent, tupsent
    
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
                  'niece':'f','nephew':'m',
                  'lolo':'m','barack':'m','obama':'m','michelle':'f','robinson':'f','ann':'f','dunham':'f'}
    #print word
    from nltk.corpus import wordnet as wn
    wgender = genderDict[word]
    gen = 'n'
    gen2 = 'n'
    gen3 = 'n'
    name = []
    name2 = []
    name3 = []
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
        if state == 9:
            break
        if state == 2 and pos == 'nnp':
            name.append(tup[0])
            #if pos != 'nnp':
            if genderDict.has_key(noun):
                gen = genderDict[noun]
            else:
                if len(wn.synsets(noun.lower())) > 0:
                    gen = 'in'
                
        if state == 10 and pos == 'nnp':
            name2.append(tup[0])
            #if pos != 'nnp':
            if genderDict.has_key(noun):
                gen2 = genderDict[noun]
            else:
                if len(wn.synsets(noun.lower())) > 0:
                    gen2 = 'in'

        if state == 11 and pos == 'nnp':
            name3.append(tup[0])
            #if pos != 'nnp':
            if genderDict.has_key(noun):
                gen3 = genderDict[noun]
            else:
                if len(wn.synsets(noun.lower())) > 0:
                    gen3 = 'in'
        
        
    #if state == 3 or state == 10:
    if word == 'they' or word == 'their':
        if name and name3:
            #print name
            #print name3
            ref = ' '.join(name) + ' and ' + ' '.join(name3)
        elif name and name2:
            #print name
            #print name2
            ref = ' '.join(name) + ' and ' + ' '.join(name2)
    elif (gen == wgender) and wgender != 'n' and name:
        ref = ' '.join(name)
            
    #print name        
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
    table = {1:{'nnp':2,'nn':1,'nns':1,'prp$':1,'*':1,'in':8,'vbn':8},
             2:{'nnp':2,'nn':2,'nns':2,'pos':1,'vb':3,'vbz':3,'vbd':3,'md':3,'-lrb-':6,',':4,'rb':5,'*':9,'cc':11,'prp$':1},
             3:{'nnp':10,'nn':10,'prp$':10,'*':9},
             4:{'nnp':2,'vb':3,'vbz':3,'vbd':3,'md':3,'*':9},
             5:{'vb':3,'vbz':3,'vbd':3,'md':3,'*':9},
             6:{'-rrb-':7,'*':6},
             7:{'vb':3,'vbz':3,'vbd':3,'md':3,'*':9},
             8:{'*':8,',':1},
             9:{'*':9},
             10:{'nnp':10,'nn':10,'prp$':10,'*':9},
             11:{'nnp':11,'nn':11,'pos':11,'prp$':11,'vb':3,'vbz':3,'vbd':3,'md':3,'-lrb-':6,',':4,'rb':5,'*':9}}
    
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
    match = re.findall(r'^'+query,text)
    if len(match)>0:
        val = True
    else:
        val = False
    return val

def isRelationship2(tups):
    val = False
    query = '|'.join(Queries)
    for tup in tups:
        match = re.findall(query,tup[0])
        if len(match)>0:
            val = True
            break
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

def extractRelation(sents):
    regexps = [(r".*([A-Z]\w*)\sand\s(([A-Z]\w*\s)*).*(married)\s",2,4,1),  #(r".*([A-Z]\w*)\s?'s\s(\w*)\s?,\s?(([A-Z]\w*\s?,?\s?)*)",1,2,3),
               (r".*([A-Z]\w*)'s\s*(\w*\s*grandparents)\s,?\s?(([A-Z]\w*)(\sand\s)?([A-Z]\w*)?)",3,2,1)]
    for q in Queries:
        query = r".*([A-Z]\w*)\s?'s.*\s(\w*\s*"+q+")\s,?\s?(([A-Z]\w*\s?,?\s?)*)" #([A-Z]\w*)
        regexps.append((query,3,2,1))
        query = r".*([A-Z]\w*)\shas\s\w*\s*("+q+").*(([A-Z]\w*\s?,?\s?)*)"
        regexps.append((query,3,2,1))
        query = r".*([A-Z].*)\s,\s("+q+")\sof\s([A-Z].*)"
        regexps.append((query,3,2,1))


    result = []
        
    for s in sents:
        for regexp in regexps:
            match = re.match(regexp[0], s)
            if match:
                if len(match.group(regexp[1])) > 0 and len(match.group(regexp[2])) > 0 and len(match.group(regexp[3])) > 0:
                    if goodRel(match.group(regexp[2])):
                        ent1 = match.group(regexp[1]).rstrip(', ')
                        ent2 = match.group(regexp[3]).rstrip(', ')
                        rel = match.group(regexp[2]).rstrip(', ')
                        de1 = decompose(ent1)
                        de2 = decompose(ent2)
                        for m in de1:
                            for n in de2:
                                result.append((m.rstrip(),rel.rstrip(),n.rstrip()))
                    
        fall = re.findall(r"(daughter)\s,\s([A-Z]\w*)",s)
        if fall:
            ent1 = re.findall(r"([A-Z].*)\s's",s)
            if ent1:
                for f in fall:
                    de1 = decompose(f[1].rstrip())
                    de2 = decompose(ent1[0].rstrip())
                    for m in de1:
                        for n in de2:
                            result.append((m.rstrip(),"daughter",n.rstrip()))

    return result

def decompose(s):
    rc = []
    splits = string.split(s, ' and ')
    #print s
    #print splits
    if len(splits) > 1:
        for split in splits:
            rc.append(split)
    else:
        rc.append(s)
    return rc

def goodRel(s):
    for q in Queries:
        v = re.search(r"^[a-z\s]*"+q+"s?",s)
        if v:
            return True
    return False

def extractRelation2(sents):
    grammar = r"""
                NP: {<dt>?<en>*<,><nnp>*|<nnp>*|<nnp>*<,>?<nnp>?}
                REL: {<nn><,>}
                """
    #print sents
    cp = nltk.RegexpParser(grammar)
    for s in sents:
        #print s
        print cp.parse(s)
        
def selectRelSents(sents):
    for s in sents:
        if isRelationship(s):
            print s
            
def selectRelSents2(sents):
    for s in sents:
        if isRelationship2(s):
            print s

def callme(filename="Barack_Obama3.xml"):
    texts, oritups, reptups = extractRelationInfo(filename)
    return extractRelation(texts)

def main():
    filename = "Barack_Obama3.xml"
    print callme(filename)

if __name__ == '__main__':
    main()
    
