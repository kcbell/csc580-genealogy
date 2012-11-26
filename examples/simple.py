'''
Created on Nov 25, 2012

@author: Karl
'''

from family import Person, Parent, Child, Sibling, Spouse

JOHN = Person(["John X. Smith"], ["John"], Person.MALE)
ANNE = Person(["Anne Smith"], ["Anne"], Person.FEMALE)
PETE = Person(["Pete"], [], Person.MALE)
BOB = Person(["Bob"], [], Person.MALE)
SUE = Person(["Sue"], [], Person.FEMALE)
ROBERT = Person(["Robert"], [], Person.MALE)
ANNA = Person(["Anna"], [], Person.FEMALE)
HANNAH = Person(["Hannah"], [], Person.FEMALE)
SAVANNAH = Person(["Savannah"], [], Person.FEMALE)
KEN = Person(["Ken Torse"], ["Ken"], Person.MALE)
JANE = Person(["Jane"], [], Person.FEMALE)
JOSEPH = Person(["Joseph"], [], Person.MALE)
JAKE = Person(["Jake"], [], Person.MALE)
JAMES = Person(["James"], [], Person.MALE)

FAMILY = [
          Sibling(JOHN, JOSEPH),
          Sibling(JOHN, JAKE),
          Sibling(JOHN, JAMES),
          Sibling(JOHN, JANE),
          Parent(ANNE, JOHN),
          Parent(PETE, JOHN),
          Sibling(PETE, ANNA),
          Sibling(PETE, HANNAH),
          Sibling(PETE, SAVANNAH),
          Spouse(SAVANNAH, KEN),
          Child(ROBERT, SAVANNAH),
          Child(ROBERT, KEN),
          Parent(BOB, ANNE),
          Parent(SUE, ANNE)
          ]

if __name__ == '__main__':
    for r in FAMILY:
        print r