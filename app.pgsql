DROP TABLE IF EXISTS world;
DROP EXTENSION IF EXISTS postgis;

CREATE EXTENSION postgis;

CREATE TABLE world
(
);

SELECT AddGeometryColumn('world', 'geom', 4326, 'POLYGON', 2);

INSERT INTO world (geom) VALUES (ST_SetSRID(ST_MakeBox2D(ST_MakePoint(-1, -1), ST_MakePoint(1, 1)), 4326));
