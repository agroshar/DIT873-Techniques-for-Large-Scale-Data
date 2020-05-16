import requests
from time import sleep
import pandas as pd

from queries import *


def construct_dataframe_from_wikidata(query):
    def send_request():
        return requests.get('https://query.wikidata.org/sparql',
                            headers={
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 ('
                                              'KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'},
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
    entries = []
    for record in records:
        entry = dict.fromkeys(labels)
        for label, values in record.items():
            entry[label] = values['value']
        entries.append(entry)

    df = pd.DataFrame(entries, columns=labels)

    return df


if __name__ == '__main__':
    universities_df = construct_dataframe_from_wikidata(universities_query)
    universities_df.to_csv('data/universities.csv')

    alumni_df = construct_dataframe_from_wikidata(alumni_query)
    alumni_df.to_csv('data/alumni.csv')

    organisations_df = construct_dataframe_from_wikidata(organisations_query)
    organisations_df.to_csv('data/organisations.csv')
