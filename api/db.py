from datetime import datetime
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from passlib.hash import sha256_crypt

from api.models import User
from api.models import Profile
from api.models import Game
from api.models import Genres
from api.models import InviteMessage
from api.models import FriendRequest

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
    if avatar: # pragma: no cover
        db.execute(f"INSERT INTO user (username, password, email, avatar) "
                f"VALUES ('{username}', '{hashed_pass}', '{email}', '{avatar}')")
    else:
        db.execute(f"INSERT INTO user (username, password, email) "
                f"VALUES ('{username}', '{hashed_pass}', '{email}')")
    db.commit()
    return "ok"


def check_login(username, password):
    db = get_db()
    try:
        res = db.execute(f"SELECT id, username, password, email, avatar FROM user WHERE username = '{username}'").fetchone()
        if sha256_crypt.verify(password, res[2]):
            user = User(res[0], res[1], None, res[3], res[4])
            return "ok", user
        else:
            return "username or password is wrong!", None
    except Exception:
        return "username or password is wrong!", None


def add_profile(uid, bio, status, background='defaultbg.png'):
    db = get_db()
    db.execute(f"INSERT INTO profile (user_id, bio, status, background) "
                f"VALUES({uid}, '{bio}', '{status}', '{background}') "
            )
    db.commit()
    return "ok"


def update_profile_status(user_id, status):
    db = get_db()
    db.execute(f"UPDATE profile SET status = '{status}' where user_id = {user_id}")
    db.commit()
    return "ok"


def update_profile_bio(user_id, bio):
    db = get_db()
    db.execute(f"UPDATE profile SET bio = '{bio}' where user_id = {user_id}")
    db.commit()
    return "ok"

def get_user_by_id(user_id):
    db = get_db()
    res = db.execute(f"SELECT * FROM USER "
                f"WHERE id = {user_id}").fetchone()
    
    if res:        
        return User(res[0], res[1], None, None, res[4])
    return "not found"


def get_user_profile(user_id):
    db = get_db()
    try:
        res = db.execute(f"SELECT * from profile WHERE user_id = {user_id}").fetchone()
        if res:
            prof = Profile(res[0], res[1], res[2], res[3], res[4])
            return "ok", prof
        return "not found", None

    except Exception:
        
        return "invalid", None


def check_user_has_game(user_id, game_id):
    db = get_db()
    res = db.execute(f"SELECT * from gameList where user_id = {user_id} and game_id = {game_id}").fetchone()
    if res:
        return True
    return False


def get_list_of_games_per_user(user_id):
    db = get_db()
    result = db.execute(f"SELECT game.* from game "
                        f"LEFT JOIN gameList gL on game.id = gL.game_id "
                        f"WHERE {user_id} = gL.user_id").fetchall()
    lst = []
    for i in result:
        lst.append(Game(i[0], i[1], i[2], i[3], i[4], i[5]).__dict__)

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
    res = db.execute(f"SELECT * FROM gameList WHERE (user_id={user_id} "
                    f"AND game_id = {game_id})").fetchall()
    if res:
        return "already added"

    res = db.execute(f"SELECT * FROM gameList "
                    f"").fetchall()
    db.execute(f"INSERT INTO gameList (user_id, game_id) "
               f"VALUES ({user_id}, {game_id})")
    db.commit()
    return "ok"


def get_list_of_friends(user_id):
    db = get_db()
    res = db.execute(f"SELECT user.id, user.username FROM user "
                     f"LEFT JOIN friendList AS FL ON (FL.user_1_id = {user_id}  "
                     f"OR FL.user_2_id = {user_id}) "
                     f"WHERE ((FL.user_2_id = user.id OR FL.user_1_id = user.id) "
                     f"AND user.id != {user_id})"
                    ).fetchall()

    lst = [(i[0], i[1]) for i in res]
    return lst



def get_invite_from_others_message(user_id):
    db = get_db()
    res = db.execute(f"SELECT user.id, user.username, game.id, game.name, "
                     f"IM.id, IM.suggestedTime, IM.creationTime, IM.accepted, "
                     f"IM.sender_id, IM.receiver_id "
                     f"FROM user, game, inviteMessage as IM "
                     f"WHERE (IM.receiver_id = {user_id} AND user.id = IM.sender_id "
                     f"AND game.id = IM.game_id)"
                    ).fetchall()

    lst = [InviteMessage(i[4], i[2], i[8], i[9], i[5], i[6], i[7]).__dict__ for i in res]
    return lst


def get_invite_to_others_message(user_id):
    db = get_db()
    res = db.execute(f"SELECT user.id, user.username, game.id, game.name, "
                     f"IM.id, IM.suggestedTime, IM.creationTime, IM.accepted, "
                     f"IM.sender_id, IM.receiver_id "
                     f"FROM user, game, inviteMessage as IM "
                     f"WHERE (IM.sender_id = {user_id} AND user.id = IM.receiver_id "
                     f"AND game.id = IM.game_id)"
                    ).fetchall()
    
    lst = [InviteMessage(i[4], i[2], i[8], i[9], i[5], i[6], i[7]).__dict__ for i in res]
    return lst


def get_invite_msg_by_id(msg_id):
    db = get_db()
    res = db.execute(f"SELECT SEN.id, SEN.username, REC.id, REC.username, game.id, "
                     f"game.name, IM.id, IM.suggestedTime, IM.creationTime, IM.accepted "
                     f"FROM user AS SEN, user AS REC, game, inviteMessage as IM "
                     f"WHERE (IM.id = {msg_id} AND REC.id = IM.receiver_id "
                     f"AND game.id = IM.game_id AND SEN.id = IM.sender_id)"
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

    res = db.execute(f"SELECT SEN.id, SEN.username, REC.id, REC.username, game.id, "
                     f"game.name, IM.id, IM.suggestedTime, IM.creationTime, IM.accepted "
                     f"FROM user AS SEN, user AS REC, game, inviteMessage as IM "
                     f"WHERE (IM.id = {msg_id} AND REC.id = IM.receiver_id "
                     f"AND game.id = IM.game_id AND SEN.id = IM.sender_id)"
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
    db.execute(f"INSERT INTO inviteMessage (game_id, sender_id, receiver_id, "
               f"suggestedTime, creationTime) "
               f"VALUES ({im.game_id}, {im.sender_id}, {im.receiver_id}, "
               f"'{im.suggestedTime}', '{im.creationTime}')"
              )
    db.commit()
    return "ok"


def delete_invite_msg(msg_id: int):
    db = get_db()
    db.execute(f"DELETE FROM inviteMessage WHERE id = {msg_id}")
    db.commit()
    return("ok")


def get_sent_friend_requests_by_user_id(user_id):
    db = get_db()
    res = db.execute(f"SELECT * from friendRequest WHERE sender_id = {user_id}").fetchall()
    if res:
        lst = [FriendRequest(i[0], i[1], i[2], i[3]).__dict__ for i in res]
        return lst
    return None
    

def get_received_friend_requests_by_user_id(user_id):
    db = get_db()
    res = db.execute(f"SELECT * from friendRequest WHERE receiver_id = {user_id}").fetchall()
    if res:
        lst = [FriendRequest(i[0], i[1], i[2], i[3]).__dict__ for i in res]
        return lst
    return None


def check_if_friends(user_1_id, user_2_id):
    db = get_db()
    res = db.execute(f"SELECT * FROM friendList "
                     f"WHERE ((user_1_id = {user_1_id} AND user_2_id = {user_2_id}) "
                     f"OR (user_2_id = {user_1_id} AND user_1_id = {user_2_id}))").fetchone()
    if res:
        return True
    return False

def check_if_pending_request(user_1_id, user_2_id):
    db = get_db()
    res = db.execute(f"SELECT * FROM friendRequest "
                    f"WHERE sender_id = {user_2_id} AND receiver_id = {user_1_id}").fetchone()

    if res:
        return res[0]
    return False
     

def add_friend_req(sender_id, receiver_id):
    db = get_db()
    cf = check_if_friends(sender_id, receiver_id)
    if cf:
        return "already friends"
    cpr = check_if_pending_request(sender_id, receiver_id)
    # CPR: INT 
    if cpr:
        # ACCEPT FRIEND REQUEST
        db.execute(f"DELETE FROM friendRequest WHERE id = {cpr}")
        db.commit()
        db.execute(f"INSERT INTO friendList (user_1_id, user_2_id) "
                    f"VALUES ({receiver_id}, {sender_id})")
        db.commit()
        return "accepted"
    cpr = check_if_pending_request(receiver_id, sender_id)
    if cpr:
        return "already sent"
    ct = datetime.now()
    db.execute(f"INSERT INTO friendRequest (sender_id, receiver_id, creationTime) "
                f"VALUES ({sender_id}, {receiver_id}, '{ct}')")
    db.commit()
    return "ok"


def delete_friend_req(user_id, fr_id):
    db = get_db()
    # check if friend request exists
    res = db.execute(f"SELECT * FROM friendRequest WHERE id = {fr_id}").fetchone()
    if res:
        db.execute(f"DELETE FROM friendRequest WHERE (id = {fr_id} AND receiver_id = {user_id}) ")
        db.commit()
        return "ok"
    return "not found"


def accept_friend_request(user_id, fr_id):
    db = get_db()
    res = db.execute(f"SELECT * FROM friendRequest "
                     f"WHERE id = {fr_id} AND receiver_id = {user_id} "
                     ).fetchone()
    if res:
        db.execute(f"DELETE FROM friendRequest WHERE id = {res[0]}")
        db.commit()
        db.execute(f"INSERT INTO friendList (user_1_id, user_2_id) "
                    f"VALUES ({res[1]}, {res[2]})")
        db.commit()
        return "accepted"

    return "not found"


def delete_friend_from_friend_list(user1_id, user2_id):
    db = get_db()
    # check if user_1 is in user_2's friend list and vice versa
    res = check_if_friends(user1_id, user2_id)
    if res:
        db.execute(f"DELETE FROM friendList WHERE (user_1_id = {user1_id} AND user_2_id = {user2_id}) "
                   f"OR (user_1_id = {user2_id} AND user_2_id = {user1_id})")
        db.commit()
        return "ok"
    return "not found"