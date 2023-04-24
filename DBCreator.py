from data import db_session
from data.games import Game
from data.genres import Genre
from data.platforms import Platform
from data.companies import Company
import datetime
import api_requests


def init_db():
    db_sess = db_session.create_session()

    # adding all genres from IGDB
    def add_all_genres():
        genres = api_requests.get_all_genres()
        for genre_data in genres:
            genre = Genre(genre_data['id'], genre_data['name'])
            db_sess.add(genre)
            db_sess.commit()

    # adding all platforms from IGDB
    def add_all_platforms():
        platforms = api_requests.get_all_platforms()
        for platform_data in platforms:
            platform = Platform(platform_data['id'], platform_data['name'])
            db_sess.add(platform)
            db_sess.commit()


def add_some_games():
    db_sess = db_session.create_session()
    all_games = db_sess.query(Game.id)
    all_game_ids = [str(i[0]) for i in list(all_games)]
    for cur_game in api_requests.get_many_games(all_game_ids):
        game = Game(
            cur_game['id'],
            cur_game['name'],
            cur_game['rating'],
            datetime.datetime.utcfromtimestamp(cur_game['first_release_date']).date(),
            api_requests.get_cover_for_game(cur_game['id']),
            cur_game['storyline'],
            cur_game['summary'],
        )

        for genre in db_sess.query(Genre).filter(Genre.id.in_(cur_game['genres'])):
            game.genres.append(genre)

        for platform in db_sess.query(Platform).filter(Platform.id.in_(cur_game['platforms'])):
            game.platforms.append(platform)

        companies = api_requests.find_companies(cur_game['involved_companies'])
        for cur_company in companies:
            company_in_db = db_sess.query(Company).filter(Company.id == cur_company['id'])
            if not list(company_in_db):
                company = Company(cur_company['id'], cur_company['name'])
                db_sess.add(company)
            else:
                company = db_sess.query(Company).filter(Company.id == cur_company['id']).first()
            game.companies.append(company)

        db_sess.add(game)
        db_sess.commit()

    db_sess.commit()
