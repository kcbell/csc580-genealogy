'''
Created on Nov 25, 2012

@author: Karl
'''

class RelationType(object):
    def __init__(self, lrdescr, rldescr):
        self.lr = lrdescr
        self.rl = rldescr
        
    def __hash__(self):
        #hash should be same for PARENT and CHILD (for Relation)
        return hash(self.rl) + hash(self.lr) 
        
    def swap(self):
        return RelationType(self.rl, self.lr)

class Person(object):
    MALE, FEMALE = range(2)
    
    def __init__(self, cnames, onames, gender = None):
        self.cnames = set()
        for name in cnames:
            self.cnames.add(name)
        self.onames = set()
        for name in onames:
            self.onames.add(name)
        self.gender = gender
        
    def __str__(self):
        return "?" if len(self.cnames) == 0 else self.cnames[0]
    
    def __eq__(self, rhs):
        return (len(self.cnames & rhs.cnames) > 0) or \
            (len(self.cnames & rhs.onames) > 0) or \
            (len(rhs.cnames & self.onames) > 0) or \
            self is rhs
            
    def mergeIn(self, rhs):
        self.cnames = self.cnames | rhs.cnames
        self.onames = self.onames | rhs.onames

class Relation(object):
    def __init__(self, p1, typ, p2):
        self.p1 = p1
        self.type = typ
        self.p2 = p2
        self.notes = []

    def __str__(self):
        return "%s %s of %s" % (str(self.p1), str(self.type), str(self.p2))
    
    def __hash__(self):
        # lots of collisions, but we can't accurately hash people...
        return self.type.__hash__() 
    
    def __eq__(self, rhs):
        return (rhs.p1 == self.p1 and rhs.type == self.type and rhs.p2 == self.p2) or \
            (rhs.p1 == self.p2 and rhs.type == self.type.swap() and rhs.p2 == self.p1)

    def swap(self):
        temp = self.p1
        self.p1 = self.p2
        self.p2 = temp
        self.type = self.type.swap()

    def addNotes(self, *notes):
        self.notes.extend(notes)

PARENT = RelationType("Parent", "Child")
CHILD = PARENT.swap()
SIBLING = RelationType("Sibling", "Sibling")
SPOUSE = RelationType("Spouse", "Spouse")

def Parent(parent, child):
    return Relation(parent, PARENT, child)

def Child(parent, child):
    return Relation(child, CHILD, parent)

def Sibling(sib1, sib2):
    return Relation(sib1, SIBLING, sib2)

def Spouse(sp1, sp2):
    return Relation(sp1, SPOUSE, sp2)
