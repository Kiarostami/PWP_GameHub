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
        if avatar:
            self.avatar = avatar

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def protected(self):
        tmp = self.__dict__
        tmp.pop('email')
        tmp.pop('password')
        return tmp.__str__()


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

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()


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

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()


class GameList:
    id: int = None
    user_id: int = None
    game_id: int = None

    def __init__(self, glid, uid, gid):
        self.id = glid
        self.user_id = uid
        self.game_id = gid

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()


class Genres:
    id: int = None
    game_id: int = None
    name: str = None

    def __init__(self, ggid, name):
        self.id = ggid
        self.name = name

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()


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

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()


class FriendRequest:
    id: int = None
    sender_id: int = None
    receiver_id: int = None
    creationTime: str = None

    def __init__(self, frid, sender_id, receiver_id, ct):
        self.id = frid
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.creationTime = ct

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()


class FriendList:
    id: int = None
    user_1_id: int = None
    user_2_id: int = None

    def __init__(self, flid, user_1_id, user_2_id):
        self.id = flid
        self.user_1_id = user_1_id
        self.user_2_id = user_2_id

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()
