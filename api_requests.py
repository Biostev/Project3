import requests
import os
from pprint import pprint
from data.games import Game

token = os.getenv('Website_Token')
client_id = os.getenv('Website_Client_ID')

url = "https://api.igdb.com/v4/"
headers = {
    'Client-ID': client_id,
    'Authorization': token,
}


def get_all_genres():
    endpoint = 'genres'
    query = 'fields id, name; limit 100;'
    params = {
        'headers': headers,
        'data': query
    }
    response = requests.post(url + endpoint, **params).json()

    return response


def get_all_platforms():
    endpoint = 'platforms'
    query = 'fields id, name; limit 500;'
    params = {
        'headers': headers,
        'data': query
    }
    response = requests.post(url + endpoint, **params).json()

    return response


def get_all_companies():
    endpoint = 'companies'
    query = 'fields id, name; limit 500;'
    params = {
        'headers': headers,
        'data': query
    }
    response = requests.post(url + endpoint, **params).json()

    return response


def find_companies(ids):
    endpoint = 'involved_companies'
    ids = ', '.join(map(str, ids))
    query = f'fields id, company; limit 500; where id = ({ids});'
    params = {
        'headers': headers,
        'data': query
    }
    response = requests.post(url + endpoint, **params).json()

    ids = [i['company'] for i in response]
    ids = ', '.join(map(str, ids))

    endpoint = 'companies'
    query = f'fields id, name; limit 500; where id = ({ids});'
    params = {
        'headers': headers,
        'data': query
    }
    response = requests.post(url + endpoint, **params).json()

    return response


def get_many_games():
    endpoint = 'games'
    query = 'fields id, name, rating, first_release_date, genres, platforms, involved_companies; ' \
            'limit 500;' \
            'where id != null & name != null & rating != null & first_release_date != null' \
            '& genres != null & platforms != null & involved_companies != null;'
    params = {
        'headers': headers,
        'data': query
    }
    response = requests.post(url + endpoint, **params).json()

    return response


# pprint(get_all_genres())
# pprint(get_all_platforms())
# pprint(get_all_companies())
# pprint(get_many_games())
