DROP TABLE IF EXISTS quake_points;

CREATE TABLE quake_points
(
    id          SERIAL PRIMARY KEY,
    quake_id    VARCHAR(40) UNIQUE,
    location    GEOGRAPHY(POINT, 4326),
    region      TEXT,
    datetime    TIMESTAMP,
    magnitude   FLOAT,
    depth       FLOAT,
    numstations INTEGER
);
