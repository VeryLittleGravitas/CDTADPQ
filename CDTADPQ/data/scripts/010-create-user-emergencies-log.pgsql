DROP TABLE IF EXISTS user_emergencies_log;

CREATE TABLE user_emergencies_log
(
    id                    SERIAL PRIMARY KEY,
    emergency_type        TEXT,
    emergency_external_id TEXT,
    user_id               INT,
    created_at            TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
