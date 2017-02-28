DROP TABLE IF EXISTS flood_polys;

CREATE TABLE flood_polys
(
    id          SERIAL PRIMARY KEY,
    location    GEOGRAPHY(POLYGON, 4326),
    valid_time  TEXT,
    outlook     TEXT,
    issue_time  TIMESTAMP,
    start_time  TIMESTAMP,
    end_time    TIMESTAMP,
    idp_source  TEXT,
    idp_subset  TEXT
);
