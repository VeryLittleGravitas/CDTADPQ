import psycopg2, os.path, glob, logging

def main(database_url):
    '''
    '''
    pattern = os.path.join(os.path.dirname(__file__), 'scripts', '???-*.pgsql')
    
    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as db:
            db.execute('SELECT last FROM migrations')
            (last_migration, ) = db.fetchone()

            for filename in sorted(glob.glob(pattern)):
                if os.path.basename(filename) <= last_migration:
                    logging.info('Skipping {}'.format(filename))
                    continue
                
                with open(filename) as file:
                    logging.info('Applying {}'.format(file.name))

                    db.execute(file.read())
                    db.execute('DELETE FROM migrations')
                    db.execute('INSERT INTO migrations (last) VALUES (%s)',
                               (os.path.basename(file.name), ))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    exit(main(os.environ['DATABASE_URL']))
