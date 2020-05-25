MATCH (org) <-[:employeeOf]-(person)-[:alumnusOf]->(:University {organisationName: 'Chalmers University of Technology'})
WITH org, COUNT(*) AS chalmerists_count
RETURN org, chalmerists_count
ORDER BY chalmerists_count DESC
