from data import db_session
from data.games import Game
from data.users import User
from data.genres import Genre
import datetime

from faker import Faker


faker_obj = Faker('en_US')


def init_db():
    db_sess = db_session.create_session()

    users = {}
    for _ in range(20):
        password = faker_obj.password()
        user = User(
            faker_obj.name(),
            faker_obj.email(),
            password
        )
        users[user] = password
        db_sess.add(user)

    db_sess.commit()

    genre_names = ['Adventure', 'Shooter', 'Horror', 'Sandbox', 'RPG', 'Simulator']
    genres = []
    for genre_name in genre_names:
        genre = Genre(genre_name)
        genres.append(genre)
        db_sess.add(genre)

    platforms = ['PC', 'Xbox', 'PS', 'Switch']
    names = ['Overwatch', 'League of Legends', 'Valorant',
             'World of Warcraft', 'cs:go', 'Danganronpa',
             'Stardew valley', 'Starbound', 'Terraria',
             'Enter the Gungeon']
    companies = ['EA', 'Ubisoft', 'Riot Games',
                 'Warner Bros. Entertainment Inc.', 'Bethesda Softworks', 'Microsoft',
                 'Rockstar games', 'T2', 'Jages',
                 'Netherrealm']
    games = []
    for _ in range(10):
        name = faker_obj.random.choice(names)
        names.remove(name)
        company = faker_obj.random.choice(companies)
        companies.remove(company)
        game = Game(
            name,
            company,
            faker_obj.random.choice(platforms),
            faker_obj.date_between(
                datetime.date(2006, 1, 1), datetime.date(2023, 1, 1)
            ),
        )
        games.append(game)
        db_sess.add(game)

    for game in games:
        for user in users:
            if faker_obj.random.randint(0, 1):
                game.users.append(user)
        for genre in genres:
            if faker_obj.random.randint(0, 1):
                game.genres.append(genre)

    db_sess.commit()


'''This func creates db with fake users, games and genres'''
