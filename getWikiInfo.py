"""
This function gets wikipedia articles
"""

import re, nltk

from urllib import urlopen

def getSubjectInfo(subject): 
    subjURL = subject.replace(" ", "_") 
    url = "http://en.wikipedia.org/w/api.php?format=xml&prop=extracts&explaintext=true&action=query&redirects=yes&titles=" + subjURL
    html = urlopen(url).read()
    raw = nltk.clean_html(html)
    raw = re.sub(r'\[.*\]', '', raw)
    raw = raw.replace('\n', ' ')
    return raw

def getContentDict(raw):
    if 'may refer to:' in raw[:raw.find(':')+1] or len(raw) < 1:
        return None
    raw = raw.replace('&quot;', '"').replace('&amp;', '&')
    raw = re.sub(r'(\s)*==+(.+?)==+(\s)*', '[\g<2>] ', raw)
    sections = re.findall(r'\[(.+?)\]', raw)
    if (len(sections) == 0):
        return None
    subjDict = {}
    index = 0
    tempRaw = raw
    uselessInfo = ['bibliography', 'primary sources', 'further reading and resources', 'external links', 'notes', 'see also', 'further reading', 'references', 'publications']

    subjDict['Introduction'] = tempRaw[:tempRaw.find(sections[index])-1]

    while index < len(sections) - 1:
        if sections[index].strip().lower() in uselessInfo:
            index += 1
            continue
        start = tempRaw.find(sections[index])
        end = tempRaw.find(sections[index+1])
        s = tempRaw[start+len(sections[index])+1:end-1]
        if s != ' ':
            subjDict[sections[index].strip()] = tempRaw[start+len(sections[index])+1:end-1].strip()
        index += 1
        tempRaw = tempRaw[end:]
    if sections[index].strip().lower() not in uselessInfo:
        subjDict[sections[index].strip()] = tempRaw[tempRaw.find(sections[index])+len(sections[index])+1:].strip()    
    return subjDict

def getContent(msg):
    return getContentDict(getSubjectInfo(msg))

def main():
    msg = raw_input()
    #resp = getFirstTwoLines(getSubjectInfo(msg))
    content = getContent(msg)
    for (k, v) in content.iteritems():
        print k, ":", v
    
if __name__ == "__main__":
    main()
