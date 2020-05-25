// The most common nationalities among foreign alumni of Swedish universities

MATCH ()-[:bornIn]->(place)
WITH place.countryName AS country, COUNT(place) AS alumnis_count
WHERE NOT place.countryName = 'Sweden'
RETURN country, alumnis_count
ORDER BY alumnis_count DESC
