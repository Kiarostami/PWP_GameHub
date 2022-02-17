------------ADD GAME--------------
-----------COUNTER STRIKE --------

INSERT INTO game (name, publisher, description, isFree, price)
VALUES ("Counter Strike",
        "VALVE",
        "Counter-Strike is a series of multiplayer first-person shooter video games in which teams of terrorists battle to perpetrate an act of terror while counter-terrorists try to prevent it.",
        true,
        0);


INSERT INTO gameGenres (game_id, name)
SELECT game.id, 'First-person shooter' FROM game
WHERE game.name == 'Counter Strike';

INSERT INTO gameGenres (game_id, name)
SELECT game.id, 'Online-Multiplayer' FROM game
WHERE game.name == 'Counter Strike';

------------ADD GAME--------------
-------- DOTA 2 ------------------


INSERT INTO game (name, publisher, description, isFree, price)
VALUES ("DOTA 2",
        "VALVE",
        "Dota 2 is a multiplayer online battle arena (MOBA) video game developed and published by Valve.",
        true,
        0);

INSERT INTO gameGenres (game_id, name)
SELECT game.id, 'Multiplayer online battle arena' FROM game
WHERE game.name == 'DOTA 2';


INSERT INTO gameGenres (game_id, name)
SELECT game.id, 'Action role-playing game' FROM game
WHERE game.name == 'DOTA 2';

INSERT INTO gameGenres (game_id, name)
SELECT game.id, 'Speculative fiction' FROM game
WHERE game.name == 'DOTA 2';





------------ADD GAME--------------
-------OVERWATCH------------------

INSERT INTO game (name, publisher, description, isFree, price)
VALUES ("Overwatch",
        "Blizzard",
        "Overwatch is a 2016 team-based multiplayer first-person shooter game developed and published by Blizzard Entertainment. Described as a hero shooter, Overwatch assigns players into two teams of six, with each player selecting from a large roster of characters, known as heroes, with unique abilities.",
        false ,
        30);

INSERT INTO gameGenres (game_id, name)
SELECT game.id, 'first-person' FROM game
WHERE game.name == 'Overwatch';

INSERT INTO gameGenres (game_id, name)
SELECT game.id, 'shooter' FROM game
WHERE game.name == 'Overwatch';


INSERT INTO gameGenres (game_id, name)
SELECT game.id, 'Hero' FROM game
WHERE game.name == 'Overwatch';



------------ADD USER--------------
-------default-pass = 1234 -------
------only for populating=--------
INSERT INTO user (username, password, email)
VALUES ("vahid", "$5$rounds=535000$U39C77Rk4IOk2P0e$qKPito9ZaBAfTMQV28urOeBcUVMQf2a42xYDpolaV06", "vahid.mohsseni@oulu.fi");


INSERT INTO user (username, password, email)
VALUES ("sadaf", "$5$rounds=535000$U39C77Rk4IOk2P0e$qKPito9ZaBAfTMQV28urOeBcUVMQf2a42xYDpolaV06", "sadaf.3.nazari@student.oulu.fi");

INSERT INTO user (username, password, email)
VALUES ("sina", "$5$rounds=535000$U39C77Rk4IOk2P0e$qKPito9ZaBAfTMQV28urOeBcUVMQf2a42xYDpolaV06", "mohammad.kiarostami@oulu.fi");


INSERT INTO user (username, password, email)
VALUES ("danial", "$5$rounds=535000$U39C77Rk4IOk2P0e$qKPito9ZaBAfTMQV28urOeBcUVMQf2a42xYDpolaV06", "danial.3.khoshkholgh@student.oulu.fi");



----------ADD Profiles -------------
INSERT INTO profile (user_id, bio, status)
VALUES (1, "KOALA", "Online");
INSERT INTO profile (user_id, bio, status)
VALUES (2, "DORI 98", "Online");
INSERT INTO profile (user_id, bio, status)
VALUES (3, "InYourDreams", "Online");
INSERT INTO profile (user_id, bio, status)
VALUES (4, "KTKamran", "Online");



------------ADD Friend --------------
INSERT INTO friendList (user_1_id, user_2_id)
VALUES (1, 2);

INSERT INTO friendList (user_1_id, user_2_id)
VALUES (1, 3);

INSERT INTO friendList (user_1_id, user_2_id)
VALUES (3, 2);

INSERT INTO friendList (user_1_id, user_2_id)
VALUES (1, 4);


------Friend Request --------
INSERT INTO friendRequest (sender_id, receiver_id, creationTime)
VALUES (4, 2, "2022-02-16 12:11:24");


----------Add game for Users--------
INSERT INTO gameList (user_id, game_id)
VALUES (1, 3);

INSERT INTO gameList (user_id, game_id)
VALUES (1, 2);

INSERT INTO gameList (user_id, game_id)
VALUES (2, 1);

INSERT INTO gameList (user_id, game_id)
VALUES (3, 2);

INSERT INTO gameList (user_id, game_id)
VALUES (4, 2);




