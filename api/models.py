from flask import url_for


from api.util.masonbuilder import MasonBuilder

class User:
    id: int = None
    username: str = None
    password: str = None
    email: str = None
    avatar: str = "defaultav.png"

    def __init__(self, uid, username, password, email, avatar=None):
        self.id = uid
        self.username = username
        self.password = password
        self.email = email
        if avatar: # pragma: no cover
            self.avatar = avatar

    def protected(self):
        tmp = self.__dict__
        tmp.pop('email')
        tmp.pop('password')
        return tmp

    @staticmethod
    def signup_json_schema():
        return {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
                "email": {"type": "string"}
            },
            "required": ["username", "password", "email"]
        }

    @staticmethod
    def login_json_schema():
        return {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
                "email": {"type": "string"}
            },
            "required": ["username", "password"]
        }


class Profile:
    id: int = None
    user_id: int = None
    bio: str = None
    status: str = None
    background: str = "defaultbg.png"

    def __init__(self, pid, user_id, bio, status, background):
        self.id = pid
        self.user_id = user_id
        self.bio = bio
        self.status = status
        self.background = background
    

class InviteMessage:
    id: int = None
    game_id: int = None
    sender_id: int = None
    receiver_id: int = None
    suggestedTime: str = None
    creationTime: str = None
    accepted: bool = None

    def __init__(self, imid, game_id, sender_id, receiver_id, st, ct, accepted = None):
        self.id = imid
        self.game_id = game_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.suggestedTime = st
        self.creationTime = ct
        self.accepted = accepted

    @staticmethod
    def new_json_schema():
        # return the jsonschema for invite message
        return {
            "type": "object",
            "properties": {
                "game_id": {"type": "integer"},
                "receiver_id": {"type": "integer"},
                "suggestedTime": {"type": "string"}
            },
            "required": ["game_id", "receiver_id", "suggestedTime"]
        }


class GameList:
    id: int = None
    user_id: int = None
    game_id: int = None

    def __init__(self, glid, uid, gid): # pragma: no cover
        self.id = glid
        self.user_id = uid
        self.game_id = gid

    def __repr__(self): # pragma: no cover
        return self.__dict__.__str__() 

    def __str__(self):
        return self.__dict__.__str__() # pragma: no cover

class Genres:
    id: int = None
    game_id: int = None
    name: str = None

    def __init__(self, ggid, name, game_id): 
        self.id = ggid  # pragma: no cover
        self.name = name  # pragma: no cover
        self.game_id = game_id  # pragma: no cover

    def __repr__(self): 
        return self.__dict__.__str__() # pragma: no cover

    def __str__(self): 
        return self.__dict__.__str__() # pragma: no cover

    def serialize(self):
        return {
            "id": self.id,
            "game_id": self.game_id,
            "name": self.name
        }


class Game:
    id: int = None
    name: str = None
    publisher: str = None
    description: str = None
    isFree: int = None
    price: int = None
    genresList: list = None

    def __init__(self, gid, name, publisher, description, isFree, price, genresList=None):
        self.id = gid
        self.name = name
        self.publisher = publisher
        self.description = description
        self.isFree = isFree
        self.price = price
        self.genresList = genresList

    def __repr__(self): # pragma: no cover
        return self.__dict__.__str__()

    def __str__(self):  # pragma: no cover
        return self.__dict__.__str__()

    def serialize(self, user_id):
        data = MasonBuilder(
            id=self.id,
            name=self.name,
            publisher=self.publisher,
            description=self.description,
            isFree=self.isFree,
            price=self.price
        )

        data.add_control("genres", href=url_for("genres.get_genres", game_id=self.id))
        
        # add post control to add the game to user
        data.add_control_post("add_game", href=url_for("user.add_game_to_user", uid=user_id, gid=self.id), title="Add Game to this user", schema=None)

        return data



class FriendRequest:
    id: int = None
    sender_id: int = None
    receiver_id: int = None
    creationTime: str = None

    def __init__(self, frid, sender_id, receiver_id, ct): # pragma: no cover
        self.id = frid
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.creationTime = ct


class FriendList:
    id: int = None
    user_1_id: int = None
    user_2_id: int = None

    def __init__(self, flid, user_1_id, user_2_id): # pragma: no cover
        self.id = flid
        self.user_1_id = user_1_id
        self.user_2_id = user_2_id
 
    def __repr__(self): # pragma: no cover
        return self.__dict__.__str__()

    def __str__(self): # pragma: no cover
        return self.__dict__.__str__()
