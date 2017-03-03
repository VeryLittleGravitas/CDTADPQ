DROP TABLE IF EXISTS notifications_log;

CREATE TABLE notifications_log
(
    id                    SERIAL PRIMARY KEY,
    message               TEXT,
    emergency_id          INT,
    emergency_type        TEXT,
    notified_users_count  INT,
    created_at            TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

