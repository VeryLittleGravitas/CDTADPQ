import flask, psycopg2, os, json

app = flask.Flask(__name__)

@app.route('/')
def get_index():
    with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
        with conn.cursor() as db:
            db.execute('SELECT ST_AsGeoJSON(geom) FROM world LIMIT 1')
            (geometry, ) = db.fetchone()
    
    feature = dict(geometry=json.loads(geometry), type='Feature', properties={})
    geojson = dict(type='FeatureCollection', features=[feature])
    
    return flask.jsonify(geojson)

if __name__ == '__main__':
    app.run(debug=True)
