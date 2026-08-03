-- query.sql — the named queries sqlc turns into type-safe Go methods.
-- Run `sqlc generate` to emit models.go + query.sql.go from this file + schema.sql.

-- name: CreateFoo :execlastid
INSERT INTO foos (name) VALUES (?);

-- name: GetFoo :one
SELECT id, name, created_at FROM foos WHERE id = ?;

-- name: ListFoos :many
SELECT id, name, created_at FROM foos ORDER BY id;
