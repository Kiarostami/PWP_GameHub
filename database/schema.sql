DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS profile;
DROP TABLE IF EXISTS gameGenresList;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS friendRequest;
DROP TABLE IF EXISTS gameList;
DROP TABLE IF EXISTS friendList;
DROP TABLE IF EXISTS inviteMessage;


CREATE TABLE user(
    id INTEGER primary key AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    avatar TEXT NULL
);


CREATE TABLE game(
    id INTEGER primary key AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    publisher TEXT NOT NULL,
    description TEXT NOT NULL,
    isFree BOOLEAN,
    price integer
);


CREATE TABLE profile(
    id INTEGER primary key AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    bio TEXT,
    status TEXT,
    background TEXT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);


CREATE TABLE genre(
    id INTEGER primary key AUTOINCREMENT,
    name TEXT NOT NULL
);


CREATE TABLE gameGenresList(
    game_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,

    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(id) ON DELETE CASCADE
);

CREATE TABLE friendRequest(
    id INTEGER primary key AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    creationTime timestamp,
    FOREIGN KEY (sender_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE gameList(
    id INTEGER primary key AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    game_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE
);

CREATE TABLE friendList(
    id INTEGER primary key AUTOINCREMENT,
    user_1_id INTEGER NOT NULL,
    user_2_id INTEGER NOT NULL,
    FOREIGN KEY (user_1_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (user_2_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE inviteMessage(
    id INTEGER primary key AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    suggestedTime timestamp,
    creationTime timestamp,
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES user(id) ON DELETE CASCADE
)