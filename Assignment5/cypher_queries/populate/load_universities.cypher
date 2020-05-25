LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/agroshar/DIT873-Techniques-for-Large-Scale-Data/master/Assignment5/csv_files/universities.csv' AS row
MERGE (p:Place {placeName: row.place, countryName: row.country})
MERGE (u:Organisation:University {organisationName: row.university, yearFounded: toInteger(row.yearFounded)})
MERGE (u)-[:locatedIn]->(p)
