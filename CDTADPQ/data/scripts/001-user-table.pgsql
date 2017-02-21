DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS unverified_signups;

CREATE TABLE users
(
    phone_number    TEXT,
    zip_codes       TEXT[]
);

CREATE TABLE unverified_signups
(
    phone_number    TEXT,
    pin_number      TEXT,
    created         TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
