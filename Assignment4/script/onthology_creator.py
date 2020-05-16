from owlready2 import *


onto = get_ontology('../assignment4.owl').load()
o = onto.Organisation("org", organisationName=['ABC'])
p = onto.Person("test_person", personName=['John'])
p.employeeOf = [o]

print(onto.test_person.employeeOf.organisationName)
print([x for x in onto.individuals()])