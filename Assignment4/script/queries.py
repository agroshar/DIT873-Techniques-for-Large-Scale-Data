universities_query = """
SELECT ?universityLabel ?countryLabel (YEAR(?inception) AS ?yearFounded)

WHERE
{
  ?university wdt:P31 wd:Q3918 .
  ?university wdt:P17 wd:Q34 .
  ?university wdt:P571 ?inception .
  ?university wdt:P17 ?country .

  SERVICE wikibase:label {bd:serviceParam wikibase:language "en,sv,[AUTO_LANGUAGE]" .}
}
"""

alumni_query = """
SELECT ?alumnusLabel ?birthplaceLabel ?birthplacecountryLabel ?universityLabel

WHERE
{
  ?alumnus wdt:P69 ?university .

  ?university wdt:P31 wd:Q3918 ;
              wdt:P17 wd:Q34 .

  OPTIONAL {?alumnus wdt:P19 ?birthplace .
            ?birthplace wdt:P17 ?birthplacecountry}

  SERVICE wikibase:label {bd:serviceParam wikibase:language "en,sv,[AUTO_LANGUAGE]" .}
}
"""

organisations_query = """
SELECT ?alumnusLabel ?organisationLabel ?placeLabel ?countryLabel

WHERE
{
  ?alumnus wdt:P69 ?university .

  ?university wdt:P31 wd:Q3918 ;
              wdt:P17 wd:Q34 .

  ?alumnus wdt:P108 ?organisation .
  OPTIONAL {?organisation wdt:P131 ?place .
            ?place wdt:P17 ?country .}

  SERVICE wikibase:label {bd:serviceParam wikibase:language "en,sv,[AUTO_LANGUAGE]" .}
}
"""
