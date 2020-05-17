from owlready2 import *
import pandas as pd
from re import sub


def is_unknown(data): return not isinstance(data, str)


def read_data():
    uni_df = pd.read_csv('data/universities.csv')
    alumni_df = pd.read_csv('data/alumni.csv')
    org_df = pd.read_csv('data/organisations.csv')

    return uni_df, alumni_df, org_df


def create_id(strings):
    object_id = '_'
    object_id = object_id.join(strings)
    object_id = sub(r'[^A-Za-z0-9öäåÖÄÅ_]', '_', object_id)

    return object_id


def create_places(onto, dfs):
    for df in dfs:
        for _, row in df[['place', 'country']].iterrows():
            if is_unknown(row.place):
                continue

            place_id = create_id([row.place, row.country])
            onto.Place(place_id,
                       placeName=[row.place],
                       countryName=[row.country])


def create_universities(onto, uni_df):
    for _, row in uni_df.iterrows():
        if is_unknown(row.university):
            continue

        uni_id = create_id([row.university])
        uni = onto.University(uni_id,
                              organisationName=[row.university],
                              yearFounded=[row.yearFounded])

        if is_unknown(row.place):
            continue

        uni_place_id = create_id([row.place, row.country])
        uni.locatedIn = [onto[uni_place_id]]


def create_organisations(onto, org_df):
    for _, row in org_df[['organisation', 'place', 'country']].iterrows():
        if is_unknown(row.organisation):
            continue

        org_id = create_id([row.organisation])

        if onto[org_id]:
            continue

        org = onto.Organisation(org_id,
                                organisationName=[row.organisation])

        if is_unknown(row.place):
            continue

        org_place_id = create_id([row.place, row.country])
        org.locatedIn = [onto[org_place_id]]


def create_persons(onto, alumni_df, org_df):
    for _, row in alumni_df.iterrows():
        if is_unknown(row.alumnus):
            continue

        person_id = create_id(['person', row.alumnus])
        person = onto.Person(person_id,
                             personName=[row.alumnus])
        uni_id = create_id([row.university])
        person.alumnusOf.append(onto[uni_id])

        if is_unknown(row.place):
            continue

        person_place_id = create_id([row.place, row.country])
        person.bornIn = [onto[person_place_id]]

    for _, row in org_df[['alumnus', 'organisation']].iterrows():
        person_id = create_id(['person', row.alumnus])
        org_id = create_id([row.organisation])

        onto[person_id].employeeOf.append(onto[org_id])


if __name__ == '__main__':
    onto = get_ontology('../assignment4.owl').load()

    uni_df, alumni_df, org_df = read_data()

    create_places(onto, [uni_df, alumni_df, org_df])
    create_universities(onto, uni_df)
    create_organisations(onto, org_df)
    onto.save(file='data/onto.owl', format='rdfxml')

    create_persons(onto, alumni_df, org_df)

    onto.save(file='data/onto.owl', format='rdfxml')
