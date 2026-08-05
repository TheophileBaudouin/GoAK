// Package postgrespgx demonstrates a small native pgxpool persistence boundary.
package postgrespgx

import (
	"context"
	"errors"
	"fmt"
	"strings"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

// Widget is the concrete row owned by this small persistence example.
type Widget struct {
	ID        int64
	Name      string
	CreatedAt time.Time
}

// Store owns a pgx connection pool.
type Store struct {
	pool *pgxpool.Pool
}

// Open parses databaseURL, creates a pool, and proves its liveness with Ping.
// The context controls both allocation and connection establishment.
func Open(ctx context.Context, databaseURL string) (*Store, error) {
	if strings.TrimSpace(databaseURL) == "" {
		return nil, errors.New("DATABASE_URL is required")
	}
	config, err := pgxpool.ParseConfig(databaseURL)
	if err != nil {
		return nil, fmt.Errorf("parse PostgreSQL configuration: %w", err)
	}
	pool, err := pgxpool.NewWithConfig(ctx, config)
	if err != nil {
		return nil, fmt.Errorf("create PostgreSQL pool: %w", err)
	}
	if err := pool.Ping(ctx); err != nil {
		pool.Close()
		return nil, fmt.Errorf("ping PostgreSQL: %w", err)
	}
	return &Store{pool: pool}, nil
}

// Close releases all pool resources. It is safe to call on a nil Store.
func (s *Store) Close() {
	if s != nil && s.pool != nil {
		s.pool.Close()
	}
}

// CreateWidget inserts one named row with a positional PostgreSQL parameter.
func (s *Store) CreateWidget(ctx context.Context, name string) (Widget, error) {
	if strings.TrimSpace(name) == "" {
		return Widget{}, errors.New("widget name is required")
	}
	if s == nil || s.pool == nil {
		return Widget{}, errors.New("PostgreSQL store is not open")
	}
	var widget Widget
	err := s.pool.QueryRow(ctx, `
		INSERT INTO recipe_widgets (name)
		VALUES ($1)
		RETURNING id, name, created_at`, name).Scan(&widget.ID, &widget.Name, &widget.CreatedAt)
	if err != nil {
		return Widget{}, fmt.Errorf("create widget: %w", err)
	}
	return widget, nil
}

// Widget fetches one row by its positional PostgreSQL parameter.
func (s *Store) Widget(ctx context.Context, id int64) (Widget, error) {
	if id <= 0 {
		return Widget{}, errors.New("widget ID must be positive")
	}
	if s == nil || s.pool == nil {
		return Widget{}, errors.New("PostgreSQL store is not open")
	}
	var widget Widget
	err := s.pool.QueryRow(ctx, `
		SELECT id, name, created_at
		FROM recipe_widgets
		WHERE id = $1`, id).Scan(&widget.ID, &widget.Name, &widget.CreatedAt)
	if err != nil {
		if errors.Is(err, pgx.ErrNoRows) {
			return Widget{}, fmt.Errorf("get widget %d: %w", id, pgx.ErrNoRows)
		}
		return Widget{}, fmt.Errorf("get widget %d: %w", id, err)
	}
	return widget, nil
}
