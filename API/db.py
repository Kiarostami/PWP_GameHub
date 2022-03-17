import sqlite3
from webbrowser import get

import click
from flask import current_app, g
from flask.cli import with_appcontext

from passlib.hash import sha256_crypt

from API.models import User
from API.models import Profile
from API.models import Game
from API.models import Genres
from API.models import InviteMessage

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('../database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_data():
    db = get_db()

    with current_app.open_resource('../database/data.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    init_data()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def add_user(username, password, email, avatar = None):
    db = get_db()

    a = db.execute(f"SELECT * FROM user where username = '{username}' or email = '{email}'").fetchall()

    if len(a) != 0:
        return "user already exists"

    hashed_pass = sha256_crypt.hash(password)
    try:
        if avatar:
            db.execute(f"INSERT INTO user (username, password, email, avatar) "
                   f"VALUES ('{username}', '{hashed_pass}', '{email}', '{avatar}')")
        else:
            db.execute(f"INSERT INTO user (username, password, email) "
                   f"VALUES ('{username}', '{hashed_pass}', '{email}')")
        db.commit()
        return "OK"

    except Exception:
        db.rollback()
        return "failed"


def check_login(username, password):
    db = get_db()
    try:
        res = db.execute(f"SELECT id, username, password, email, avatar FROM user WHERE username = '{username}'").fetchone()
        if sha256_crypt.verify(password, res[2]):
            user = User(res[0], res[1], None, res[3], res[4])
            return "OK", user
        else:
            return "username or password is wrong!", None
    except Exception:
        return "username or password is wrong!", None


def add_profile(username, bio, status, background):
    db = get_db()
    try:
        db.execute(f"INSERT INTO profile (user_id, bio, status, background) "
                         f"VALUES (SELECT id from user WHERE username = '{username}', "
                         f"'{bio}', '{status}', '{background}')")
        db.commit()
        return "OK"
    except Exception:
        return "failed"


def update_profile_status(user_id, status):
    db = get_db()
    try:
        db.execute(f"UPDATE profile SET status = '{status}' where user_id = {user_id}")
        db.commit()

        return "OK"

    except Exception:
        return "failed"

def get_user_by_id(user_id):
    db = get_db()
    try:
        res = db.execute(f"SELECT * FROM USER "
                   f"WHERE id = {user_id}").fetchone()
        
        if res:        
            return User(res[0], res[1], None, None, res[4])
        return "not found"
    except:
        return "invalid"


def get_user_by_name(username):
    db = get_db()
    try:
        res = db.execute(f"SELECT * FROM USER "
                   f"WHERE username = '{username}'").fetchone()
        
        if res:        
            return User(res[0], res[1], None, None, res[4])
        return "not found"
    except:
        return "invalid"


def get_user_profile(user_id):
    db = get_db()
    try:
        res = db.execute(f"SELECT * from profile WHERE user_id = {user_id}").fetchone()

        prof = Profile(res[0], res[1], res[2], res[3], res[4])
        return "OK", prof

    except Exception:
        return "invalid", None


def get_list_of_games_per_user(user_id):
    db = get_db()
    result = db.execute(f"SELECT game.* from game "
                        f"LEFT JOIN gameList gL on game.id = gL.game_id "
                        f"WHERE {user_id} = gL.user_id").fetchall()
    lst = []
    for i in result:
        lst.append(Game(i[0], i[1], i[2], i[3], i[4], i[5]))

    return lst


def get_list_of_all_games():
    db = get_db()
    result = db.execute(f"SELECT game.* from game "
                        ).fetchall()
    lst = []
    for i in result:
        lst.append(Game(i[0], i[1], i[2], i[3], i[4], i[5]))

    return lst


def get_game_by_name_or_id(name_or_id):
    db = get_db()
    try:
        res = db.execute(f"SELECT * from game "
                        f"WHERE id = {name_or_id}").fetchone()
        if res:
            gel = get_game_genres_list(res[0])
            return Game(res[0], res[1], res[2], res[3], res[4], res[5], gel)

    except sqlite3.OperationalError:
        res = db.execute(f"SELECT * from game "
                         f"WHERE name = '{name_or_id}'").fetchone()
                         
        if res:
            gel = get_game_genres_list(res[0])
            return Game(res[0], res[1], res[2], res[3], res[4], res[5], gel)
    return None 


def get_game_genres_list(game_id):
    db = get_db()
    res = db.execute(f"SELECT genre.* FROM genre "
                      f"LEFT JOIN gameGenresList as GGL ON GGL.genre_id = genre.id "
                      f"WHERE GGL.game_id = {game_id}").fetchall()

    genre_list = [Genres(i[0], i[1]) for i in res]

    return genre_list

def add_game_to_list(user_id, game_id):
    db = get_db()
    res = db.execute(f"SELECT * FROM gameList WHERE user_id={user_id} AND game_id = game_id").fetchall()
    if len(res) > 0:
        return "already added"
    db.execute(f"INSERT INTO gameList (user_id, game_id) "
               f"VALUES ({user_id}, {game_id})")
    return "OK"

def get_list_of_friends(user_id):
    db = get_db()
    res = db.execute(f"SELECT user.id, user.username FROM user "
                     f"LEFT JOIN friendList AS FL ON (FL.user_1_id = {user_id} OR FL.user_2_id = {user_id}) "
                     f"WHERE ((FL.user_2_id = user.id OR FL.user_1_id = user.id) AND user.id != {user_id})"
                    ).fetchall()

    lst = [(i[0], i[1]) for i in res]
    return lst


def get_receiving_friend_request(user_id):
    db = get_db()
    res = db.execute(f"SELECT user.id, user.username, FR.creationTime FROM user, friendRequest as FR "
                     f"WHERE (FR.receiver_id = {user_id} AND FR.sender_id = user.id)"
                    ).fetchall()

    lst = [(i[0], i[1]) for i in res]
    return lst

def get_pending_friend_request(user_id):
    db = get_db()
    res = db.execute(f"SELECT user.id, user.username, FR.creationTime FROM user, friendRequest as FR "
                     f"WHERE (FR.sender_id = {user_id} AND FR.receiver_id = user.id)"
                    ).fetchall()

    lst = [(i[0], i[1]) for i in res]
    return lst


def get_invite_from_others_message(user_id):
    db = get_db()
    res = db.execute(f"SELECT user.id, user.username, game.id, game.name, IM.id, IM.suggestedTime, IM.creationTime, IM.accepted "
                     f"FROM user, game, inviteMessage as IM "
                     f"WHERE (IM.receiver_id = {user_id} AND user.id = IM.sender_id AND game.id = IM.game_id)"
                    ).fetchall()

    lst = [(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]) for i in res]
    return lst


def get_invite_to_others_message(user_id):
    db = get_db()
    res = db.execute(f"SELECT user.id, user.username, game.id, game.name, IM.id, IM.suggestedTime, IM.creationTime, IM.accepted "
                     f"FROM user, game, inviteMessage as IM "
                     f"WHERE (IM.sender_id = {user_id} AND user.id = IM.receiver_id AND game.id = IM.game_id)"
                    ).fetchall()
    
    lst = [(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]) for i in res]
    return lst

def get_invite_msg_by_id(msg_id):
    db = get_db()
    res = db.execute(f"SELECT SEN.id, SEN.username, REC.id, REC.username, game.id, game.name, IM.id, IM.suggestedTime, IM.creationTime, IM.accepted "
                     f"FROM user AS SEN, user AS REC, game, inviteMessage as IM "
                     f"WHERE (IM.id = {msg_id} AND REC.id = IM.receiver_id AND game.id = IM.game_id AND SEN.id = IM.sender_id)"
                    ).fetchone()
    if res:
        im = InviteMessage(res[6], res[4], res[0], res[2], res[7], res[8], res[9])
        im.game_name = res[5]
        im.receiver_username = res[3]
        im.sender_username = res[1]
        return (im)
    return None


def update_invite_msg_by_id(msg_id, status):
    db = get_db()
    db.execute(f"UPDATE inviteMessage as IM "
               f"SET accepted={status} "
               f"WHERE IM.id = {msg_id}"
              )
    db.commit()

    res = db.execute(f"SELECT SEN.id, SEN.username, REC.id, REC.username, game.id, game.name, IM.id, IM.suggestedTime, IM.creationTime, IM.accepted "
                     f"FROM user AS SEN, user AS REC, game, inviteMessage as IM "
                     f"WHERE (IM.id = {msg_id} AND REC.id = IM.receiver_id AND game.id = IM.game_id AND SEN.id = IM.sender_id)"
                    ).fetchone()
    if res:
        im = InviteMessage(res[6], res[4], res[0], res[2], res[7], res[8], res[9])
        im.game_name = res[5]
        im.receiver_username = res[3]
        im.sender_username = res[1]
        return (im)
    return None


def create_invite_msg(im: InviteMessage):
    db = get_db()
    db.execute(f"INSERT INTO inviteMessage (game_id, sender_id, receiver_id, suggestedTime, creationTime) "
               f"VALUES ({im.game_id}, {im.sender_id}, {im.receiver_id}, '{im.suggestedTime}', '{im.creationTime}') "
              )
    db.commit()
    return "ok"


def delete_invite_msg(msg_id: int):
    db = get_db()
    db.execute(f"DELETE FROM inviteMessage WHERE id = {msg_id}")
    db.commit()
    return("ok")