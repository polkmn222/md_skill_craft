# [PROJECT_NAME]

## Project
[One-line API service description]
**Stack**: Gin / Echo, Go 1.21+, PostgreSQL

## Setup
```bash
go mod tidy
go run ./cmd/[app-name]
# or: make run
```

## Key Commands
| Task | Command |
|------|---------|
| Run | `go run ./cmd/main.go` |
| Build | `go build -o bin/app ./cmd/main.go` |
| Tests | `go test ./...` |
| Lint | `golangci-lint run` |
| Format | `gofmt -w .` |
| Migrate | `migrate -path db/migrations -database $DATABASE_URL up` |

## Architecture
- `cmd/[app]/` — Executable entry points
  - `main.go` — Application startup
- `internal/` — Private package namespace (not importable)
  - `api/` — HTTP handlers
    - `routes.go` — Route registration
    - `handlers.go` — Handler functions
  - `models/` — Data structures
    - `user.go`
    - `post.go`
  - `services/` — Business logic
    - `user_service.go`
    - `post_service.go`
  - `repository/` — Data access layer
    - `user_repo.go`
    - `post_repo.go`
  - `config/` — Configuration
    - `config.go`
  - `middleware/` — HTTP middleware
    - `auth.go`
    - `logging.go`
  - `errors/` — Error types
    - `errors.go`
- `db/` — Database
  - `migrations/` — SQL migration files
- `tests/` — Integration tests
- `Makefile` — Build automation
- `go.mod` — Dependency management
- `README.md` — Usage guide

## Conventions
- Go idioms: CamelCase, error last return value
- Interface segregation (small focused interfaces)
- Dependency injection (pass dependencies to functions)
- Error wrapping with `fmt.Errorf` or `errors.Is/As`
- Struct embedding for composition
- Unexported types by default (lowercase)
- Exported types have documentation comments
- No global state
- Context for request cancellation and timeouts

## Key Dependencies
- **Gin** / **Echo** — Web framework
- **GORM** — ORM (if using database)
- **sqlc** or **sql** — Database access
- **golang-migrate** — Migrations
- **testify** — Testing assertions

## Handler Pattern (Gin)

```go
// internal/api/handlers.go
type UserHandler struct {
    service *services.UserService
}

func (h *UserHandler) GetUser(c *gin.Context) {
    id := c.Param("id")
    
    user, err := h.service.GetUser(c.Context(), id)
    if err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    
    c.JSON(200, user)
}

// main.go
func main() {
    router := gin.Default()
    
    userHandler := &UserHandler{
        service: services.NewUserService(db),
    }
    
    router.GET("/users/:id", userHandler.GetUser)
    router.Run(":8080")
}
```

## Error Handling
```go
// internal/errors/errors.go
type APIError struct {
    Code    int
    Message string
}

func (e *APIError) Error() string {
    return e.Message
}

// In handler
func (h *UserHandler) GetUser(c *gin.Context) {
    user, err := h.service.GetUser(c.Context(), id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            c.JSON(404, gin.H{"error": "not found"})
            return
        }
        c.JSON(500, gin.H{"error": "internal server error"})
        return
    }
    c.JSON(200, user)
}
```

## Testing
```go
// internal/api/handlers_test.go
func TestGetUser(t *testing.T) {
    service := &mockUserService{
        user: &models.User{ID: "1", Name: "John"},
    }
    handler := &UserHandler{service: service}
    
    w := httptest.NewRecorder()
    req, _ := http.NewRequest("GET", "/users/1", nil)
    
    router := gin.Default()
    router.GET("/users/:id", handler.GetUser)
    router.ServeHTTP(w, req)
    
    assert.Equal(t, 200, w.Code)
}

// Use testify for assertions
assert.NoError(t, err)
assert.Equal(t, expected, actual)
```

## Middleware Pattern
```go
func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.JSON(401, gin.H{"error": "unauthorized"})
            c.Abort()
            return
        }
        
        // Validate token...
        c.Set("user_id", userID)
        c.Next()
    }
}

// Use in routes
router.Use(AuthMiddleware())
router.GET("/protected", handler.Protected)
```

## Database Pattern (GORM)
```go
type User struct {
    ID    string `gorm:"primaryKey"`
    Name  string
    Email string `gorm:"uniqueIndex"`
}

func (s *UserService) GetUser(ctx context.Context, id string) (*User, error) {
    var user User
    if err := s.db.WithContext(ctx).First(&user, "id = ?", id).Error; err != nil {
        return nil, err
    }
    return &user, nil
}
```

## Anti-Patterns
- ❌ Global variables for configuration
- ❌ Ignoring errors (always handle with `if err != nil`)
- ❌ Business logic in handlers (move to services)
- ❌ Untyped interfaces (use specific types)
- ❌ No context propagation
- ❌ Hardcoded strings/magic numbers

## Logging
```go
import "log/slog"

func (h *UserHandler) GetUser(c *gin.Context) {
    slog.Info("getting user", "id", id)
    user, err := h.service.GetUser(c.Context(), id)
    if err != nil {
        slog.Error("failed to get user", "id", id, "error", err)
    }
}
```

## Configuration
```go
// internal/config/config.go
type Config struct {
    DatabaseURL string
    Port        int
    Environment string
}

func Load() *Config {
    return &Config{
        DatabaseURL: os.Getenv("DATABASE_URL"),
        Port:        8080,
        Environment: os.Getenv("ENV"),
    }
}
```

## Development Workflow
1. Define API routes in `internal/api/routes.go`
2. Create handler in `internal/api/handlers.go`
3. Create service in `internal/services/` for business logic
4. Create repository in `internal/repository/` for data access
5. Write tests in `*_test.go` files
6. Run `go test ./...` to verify
7. Run `make check` (lint → vet → test)
8. Commit and push

## Deployment
```bash
go build -o bin/app ./cmd/main.go
# Run with: ./bin/app
```

## Skills
@skills/coding-standards.md @skills/validation.md @skills/orchestration.md

## References
- [Gin Web Framework](https://gin-gonic.com/)
- [Echo Web Framework](https://echo.labstack.com/)
- [GORM Documentation](https://gorm.io/)
- [Go Error Handling](https://golang.org/doc/effective_go#errors)
- [Effective Go](https://golang.org/doc/effective_go)
