import sys

def lookup_zipcode(db, lat, lon):
    '''
    '''
    point_wkt = 'POINT ({lon} {lat})'.format(**locals())

    db.execute('''SELECT "ZCTA5CE10"
                  FROM tl_2016_us_zcta510
                  WHERE ST_Intersects(geog, ST_Buffer(ST_GeogFromText(%s), 500))
                  ORDER BY ST_Distance(geog, %s) ASC
                  LIMIT 1
                  ''',
               (point_wkt, point_wkt))
    
    row = db.fetchone()
    
    if row is None:
        return None

    return row[0]
