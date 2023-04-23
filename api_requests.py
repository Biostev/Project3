import requests
import os
from pprint import pprint
from data.games import Game
import datetime

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


def get_many_games(game_ids):
    endpoint = 'games'
    query = 'fields id, name, rating, first_release_date, genres, ' \
            'platforms, involved_companies, cover, storyline, summary; ' \
            'limit 50;' \
            f'where id != ({",".join(game_ids)}) & name != null & rating >= 70 & first_release_date != null' \
            '& genres != null & platforms != null & involved_companies != null' \
            '& storyline != null & summary != null;'
    params = {
        'headers': headers,
        'data': query
    }
    response = requests.post(url + endpoint, **params).json()

    return response


def get_new_games():
    days_to_subtract = 120
    date = datetime.datetime.today() - datetime.timedelta(days=days_to_subtract)
    date = int(round(date.timestamp()))

    endpoint = 'games'
    query = 'fields id, name, rating, first_release_date, genres, ' \
            'platforms, involved_companies, cover, storyline, summary; ' \
            'limit 50;' \
            f'where id != null & name != null & rating >= 70 & first_release_date >= {date}' \
            '& genres != null & platforms != null & involved_companies != null' \
            '& storyline != null & summary != null;'
    params = {
        'headers': headers,
        'data': query
    }
    response = requests.post(url + endpoint, **params).json()

    return response


def get_cover_for_game(game_id):
    endpoint = 'covers'
    query = 'fields *; ' \
            f'where game = {game_id};'
    params = {
        'headers': headers,
        'data': query
    }
    response = requests.post(url + endpoint, **params).json()[0]['image_id']

    im_url = f'https://images.igdb.com/igdb/image/upload/t_cover_big/{response}.png'

    return im_url


def search_game_by_name(name):
    endpoint = 'games'
    query = f'search "{name}";' \
            'fields id, name, rating, first_release_date, genres, ' \
            'platforms, involved_companies, cover, storyline, summary; '
    params = {
        'headers': headers,
        'data': query
    }
    response = requests.post(url + endpoint, **params).json()

    return response


def game_arrays(game_id):
    endpoint = 'games'
    query = 'fields id, genres, platforms, involved_companies;' \
            f'where id = {game_id};'
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
# pprint(get_cover_for_game(1942))
