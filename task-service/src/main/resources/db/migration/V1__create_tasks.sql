CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    title VARCHAR(140) NOT NULL,
    description VARCHAR(1000),
    status VARCHAR(32) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ
);

