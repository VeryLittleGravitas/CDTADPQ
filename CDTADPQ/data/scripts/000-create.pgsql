DROP TABLE IF EXISTS world;
DROP EXTENSION IF EXISTS postgis CASCADE;

CREATE EXTENSION postgis;

CREATE TABLE world
(
);

SELECT AddGeometryColumn('world', 'geom', 4326, 'POLYGON', 2);
