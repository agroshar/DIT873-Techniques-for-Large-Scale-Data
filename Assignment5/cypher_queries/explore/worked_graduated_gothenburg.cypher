MATCH (person:Person)-[:alumnusOf]->()-[:locatedIn]->(place)<-[:locatedIn]-()<-[:employeeOf]-(person)
WHERE place.placeName =~ '(.*Göteborg.*)|(.*Gothenburg.*)'
RETURN person
