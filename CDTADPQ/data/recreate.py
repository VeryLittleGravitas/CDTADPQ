import psycopg2, os.path, glob

def main(database_url):
    '''
    '''
    pattern = os.path.join(os.path.dirname(__file__), 'scripts', '???-*.pgsql')
    
    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as db:
            for filename in sorted(glob.glob(pattern)):
                with open(filename) as file:
                    db.execute(file.read())

if __name__ == '__main__':
    exit(main(os.environ['DATABASE_URL']))
