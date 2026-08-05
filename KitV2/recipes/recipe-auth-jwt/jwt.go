// Package authjwt demonstrates a narrow HS256 Bearer-token API boundary.
package authjwt

import (
	"context"
	"errors"
	"net/http"
	"strings"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var errUnauthorized = errors.New("unauthorized")

type subjectContextKey struct{}

// Config contains the complete cryptographic and claim policy. Key must be an
// injected, high-entropy secret shared only by the issuer and verifier.
type Config struct {
	Key      []byte
	Issuer   string
	Audience string
	TTL      time.Duration
	Now      func() time.Time
}

// Authenticator issues and verifies tokens for one HS256 trust boundary.
type Authenticator struct {
	key      []byte
	issuer   string
	audience string
	ttl      time.Duration
	now      func() time.Time
}

// New validates Config and constructs an Authenticator.
func New(config Config) (*Authenticator, error) {
	if len(config.Key) < 32 {
		return nil, errors.New("JWT key must contain at least 32 bytes")
	}
	if strings.TrimSpace(config.Issuer) == "" {
		return nil, errors.New("JWT issuer is required")
	}
	if strings.TrimSpace(config.Audience) == "" {
		return nil, errors.New("JWT audience is required")
	}
	if config.TTL <= 0 {
		return nil, errors.New("JWT TTL must be positive")
	}
	if config.Now == nil {
		config.Now = time.Now
	}

	return &Authenticator{
		key:      append([]byte(nil), config.Key...),
		issuer:   config.Issuer,
		audience: config.Audience,
		ttl:      config.TTL,
		now:      config.Now,
	}, nil
}

// Issue signs a short-lived token for subject.
func (a *Authenticator) Issue(subject string) (string, error) {
	if strings.TrimSpace(subject) == "" {
		return "", errors.New("JWT subject is required")
	}
	now := a.now()
	claims := jwt.RegisteredClaims{
		Issuer:    a.issuer,
		Subject:   subject,
		Audience:  jwt.ClaimStrings{a.audience},
		ExpiresAt: jwt.NewNumericDate(now.Add(a.ttl)),
		IssuedAt:  jwt.NewNumericDate(now),
	}
	return jwt.NewWithClaims(jwt.SigningMethodHS256, claims).SignedString(a.key)
}

// Middleware authorizes only Authorization: Bearer tokens and adds only their
// validated subject to the request context.
func (a *Authenticator) Middleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		subject, err := a.verifyRequest(r)
		if err != nil {
			http.Error(w, "unauthorized", http.StatusUnauthorized)
			return
		}
		next.ServeHTTP(w, r.WithContext(context.WithValue(r.Context(), subjectContextKey{}, subject)))
	})
}

func (a *Authenticator) verifyRequest(r *http.Request) (string, error) {
	values := r.Header.Values("Authorization")
	if len(values) != 1 {
		return "", errUnauthorized
	}
	scheme, tokenString, ok := strings.Cut(values[0], " ")
	if !ok || scheme != "Bearer" || tokenString == "" || strings.Contains(tokenString, " ") {
		return "", errUnauthorized
	}

	claims := new(jwt.RegisteredClaims)
	token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (any, error) {
		if token.Method != jwt.SigningMethodHS256 {
			return nil, errUnauthorized
		}
		return a.key, nil
	},
		jwt.WithValidMethods([]string{jwt.SigningMethodHS256.Alg()}),
		jwt.WithIssuer(a.issuer),
		jwt.WithAudience(a.audience),
		jwt.WithExpirationRequired(),
		jwt.WithTimeFunc(a.now),
	)
	if err != nil || token == nil || !token.Valid || strings.TrimSpace(claims.Subject) == "" {
		return "", errUnauthorized
	}
	return claims.Subject, nil
}

// Subject returns the validated JWT subject stored by Middleware.
func Subject(ctx context.Context) (string, bool) {
	subject, ok := ctx.Value(subjectContextKey{}).(string)
	return subject, ok
}
