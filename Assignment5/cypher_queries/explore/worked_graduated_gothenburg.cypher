// The names of people who both have worked and graduated in Gothenburg

MATCH (person:Person)-[:alumnusOf]->()-[:locatedIn]->(place)<-[:locatedIn]-()<-[:employeeOf]-(person)
WHERE place.placeName =~ '(.*Göteborg.*)|(.*Gothenburg.*)'
RETURN person
