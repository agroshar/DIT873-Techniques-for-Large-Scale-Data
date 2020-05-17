from owlready2 import *


onto = get_ontology('../assignment4.owl').load()

onto.Place("place1", countryName=['Germany'], placeName=['Jena'])
onto.Place("place2", countryName=['Poland'], placeName=['Poznań'])
onto.Place("place3", countryName=['Sweden'], placeName=['Lund Municipality'])

onto.Organisation("org1", organisationName=['University of Jena'])
onto.org1.locatedIn = [onto.place1]

onto.University('uni1', yearFounded=[1666], organisationName=['Lund University'])
onto.uni1.locatedIn = [onto.place3]

onto.Person('person1', personName=['Aleksander Radler'])
onto.person1.alumnusOf = [onto.uni1]
onto.person1.bornIn = [onto.place2]
onto.person1.employeeOf = [onto.org1]

onto.save(file='data/onto.owl', format='rdfxml')
