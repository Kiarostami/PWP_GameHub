INSERT INTO user (username, password, email)
VALUES ("test", "$5$rounds=535000$U39C77Rk4IOk2P0e$qKPito9ZaBAfTMQV28urOeBcUVMQf2a42xYDpolaV06", "test.test@test.fi");

INSERT INTO profile (user_id, bio, status)
VALUES (6, "KOALA", "Online");

INSERT INTO friendList (user_1_id, user_2_id)
VALUES (6, 1);


