INSERT INTO world (geom) VALUES (ST_SetSRID(ST_MakeBox2D(ST_MakePoint(-180, -90), ST_MakePoint(180, 90)), 4326));
