import pandas as pd 
import numpy as np
from time import sleep
import requests
import re
import csv


cities_query = """
SELECT ?cityLabel ?populationLabel ?coordinateLabel

WHERE {
 
  ?city (wdt:P31/(wdt:P279*)) wd:Q486972;
    wdt:P17 wd:Q34.
  ?city wdt:P1082 ?population .
  ?city wdt:P625  ?coordinate .
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }

}
"""


def construct_dataframe_from_wikidata(query):
    def send_request():
        return requests.get('https://query.wikidata.org/sparql',
                            params={'format': 'json',
                                    'query': query})

    print("Retrieving data...")
    resp = send_request()
    while not resp.ok:
        sleep(3)
        print(resp.status_code, resp.reason, resp.text)
        print("Retrieving data...")
        resp = send_request()

    labels, records = [list(data.values())[0] for data in resp.json().values()]

    print("Creating dataframe...")
    entries = [[values['value'] for values in record.values()] for record in records]
    df = pd.DataFrame(entries, columns=labels)

    return df


def create_north_south_csv_files(data):
    print('Processing data ...')

    city_data = []
    for row in data.values:
        coordinates = re.split('\(| ',row[-1])
        city_list = [row[0], int(row[1]), float(coordinates[1])]
        if city_list in city_data or 'Municipality'in row[0] or 'urban area' in row[0]:
            continue
        city_data.append(city_list)
        
    city_sorted_by_coor = sorted(city_data, key=lambda x: x[2], reverse=False)

    city_north_result = []
    city_south_result = []

    most_south_pop_temp = city_sorted_by_coor[0][1]
    city_south_result.append(city_sorted_by_coor[0])

    for i in range(1, len(city_sorted_by_coor)):
        if most_south_pop_temp < city_sorted_by_coor[i][1]:
            city_south_result.append(city_sorted_by_coor[i])
            most_south_pop_temp = city_sorted_by_coor[i][1]

    most_north_pop_temp = city_sorted_by_coor[len(city_sorted_by_coor)-1][1]
    city_north_result.append(city_sorted_by_coor[len(city_sorted_by_coor)-1])

    for i in range( len(city_sorted_by_coor)-1, 0, -1):
        if most_north_pop_temp < city_sorted_by_coor[i][1]:
            city_north_result.append(city_sorted_by_coor[i])
            most_north_pop_temp = city_sorted_by_coor[i][1]
    print('Creating city tables ...')

    df1 = pd.DataFrame(city_north_result, columns=['City', 'Population', 'Latitude'])
    df1.to_csv('./data/northern_cities.csv')

    df2 = pd.DataFrame(city_south_result, columns=['City', 'Population', 'Latitude'])
    df2.to_csv('./data/southern_cities.csv')
    print('City tables were created.')

if __name__ == '__main__':
    cities_data = construct_dataframe_from_wikidata(cities_query)
    create_north_south_csv_files(cities_data)

