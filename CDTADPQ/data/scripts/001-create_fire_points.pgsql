DROP TABLE IF EXISTS fire_points;

CREATE TABLE fire_points
(
    id         SERIAL PRIMARY KEY,
    usgs_id    VARCHAR(40) UNIQUE,
    location   GEOGRAPHY(POINT, 4326),
    name       TEXT,
    contained  INTEGER,
    discovered TIMESTAMP,
    cause      TEXT,
    acres      INTEGER
);