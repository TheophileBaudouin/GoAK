-- schema.sql — the table definition, fed to sqlc alongside query.sql.
CREATE TABLE IF NOT EXISTS foos (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
