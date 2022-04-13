CREATE TABLE users (
    id serial primary key,
    username text not null,
    password text not null,
    mail text,
    role text
);

-- user1 / pass1
INSERT INTO users (
        username,
        password,
        mail,
        role
    )
    VALUES (
        'user1',
        '$2b$12$Dvg7PxbLvkvFmMOab163peFfwKDyoL2K5qmld6PbTtQ9P0pBuirxe',
        'a@b.com',
        'ADMIN'
    );