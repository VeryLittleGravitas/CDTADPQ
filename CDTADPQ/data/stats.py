def get_all_notifications_log_rows(db):
    db.execute('SELECT * FROM notifications_log')
    return db.fetchall()
