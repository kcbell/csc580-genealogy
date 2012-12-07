'''
Created on Dec 6, 2012

@author: Karl
'''

from family import Relation, Person, PARENT, CHILD, GRANDPARENT, GRANDCHILD, AUNTUNC, NEPHNIECE, SIBLING, SPOUSE, COUSIN

# "ENTITY2's RELATION, ENTITY1" Relation(ENTITY2, RELATION, ENTITY1)
# "ENTITY1's RELATION, ENTITY2" Relation(ENTITY1, RELATION, ENTITY2)

relations = {
      "parent" : PARENT,
      "mother" : PARENT,
      "father" : PARENT,
      "mom" : PARENT,
      "dad" : PARENT,
      
      "grandparent" : GRANDPARENT,
      "grandmother" : GRANDPARENT,
      "grandfather" : GRANDPARENT,
      "grandma" : GRANDPARENT,
      "grandpa" : GRANDPARENT,
      
      "son" : CHILD,
      "daughter" : CHILD,
      "child" : CHILD,
      "children" : CHILD,
      
      "grandson" : GRANDCHILD,
      "granddaughter" : GRANDCHILD,
      "grandchild" : GRANDCHILD,
      "grandchildren" : GRANDCHILD,
      
      "sibling" : SIBLING,
      "brother" : SIBLING,
      "sister" : SIBLING,
      "bro" : SIBLING,
      "sis" : SIBLING,
      
      "aunt" : AUNTUNC,
      "uncle" : AUNTUNC,
      
      "nephew" : NEPHNIECE,
      "niece" : NEPHNIECE,
      
      "cousin" : COUSIN,
      
      "husband" : SPOUSE,
      "wife" : SPOUSE,
      "married" : SPOUSE,
      "marriage" : SPOUSE,
      }

def cleanText(text):
    return text.strip().replace(",", "")

def convertRelation(text):
    t = cleanText(text)
    s = sorted(relations.iteritems(), key=lambda x: len(x[0]), reverse=True)
    for (k, v) in s:
        if (k in t):
            return v

def tuplesToRelations(tupleList):
    ret = set()
    for tup in tupleList:
        rel = Relation(Person([tup[0]]), convertRelation(tup[1]), Person([tup[2]]))
        ret.add(rel)
    return ret
        
def main():
    tupleList = [("This person", raw_input(), "That person"), 
                 ("That person", raw_input(), "This person")]
    print [str(rel) for rel in tuplesToRelations(tupleList)]

if __name__ == '__main__':
    main()
