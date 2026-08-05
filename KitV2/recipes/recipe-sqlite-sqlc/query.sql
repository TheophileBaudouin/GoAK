-- name: CreateFoo :execlastid
INSERT INTO foos (name) VALUES (?);

-- name: GetFoo :one
SELECT id, name, created_at FROM foos WHERE id = ?;

-- name: ListFoos :many
SELECT id, name, created_at FROM foos ORDER BY id;
