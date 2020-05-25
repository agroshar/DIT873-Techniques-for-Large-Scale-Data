LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/agroshar/DIT873-Techniques-for-Large-Scale-Data/master/Assignment5/csv_files/alumni.csv' AS row
MATCH (u:University) WHERE u.organisationName = row.university
MERGE (a:Person {personName: row.alumnus})
FOREACH (ignoreMe IN (CASE WHEN row.place IS NULL THEN [] ELSE [1] END) |
    MERGE (p:Place {placeName: row.place, countryName: row.country})
    MERGE (a)-[:bornIn]->(p)
)
MERGE (a)-[:alumnusOf]->(u)
