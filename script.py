import zipfile
import os

# Создаем структуру репозитория
os.makedirs('repo/main', exist_ok=True)
os.makedirs('repo/cmd', exist_ok=True)
os.makedirs('repo/docs', exist_ok=True)
os.makedirs('repo/examples', exist_ok=True)

# main.go
main_content = '''package main

import (
    "net/http"

    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()
    
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{
            "message": "pong",
        })
    })
    
    r.Run(":8080")
}
'''
with open('repo/main.go', 'w', encoding='utf-8') as f:
    f.write(main_content)

# go.mod
go_mod = '''module github.com/yourusername/yourproject

go 1.22

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/swaggo/gin-swagger v1.6.0
    github.com/swaggo/files v1.0.1
    github.com/swaggo/swag v1.16.2
)
'''
with open('repo/go.mod', 'w', encoding='utf-8') as f:
    f.write(go_mod)

# .gitignore
gitignore = '''# Binaries
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with `go test -c`
*.test

# Output of `go test -c`
*.out

# Dependency directories (remove the comment below to include it)
# vendor/

# Go workspace file
go.work

# IDE
.idea/
.vscode/

# Docker
.dockerignore

# Logs
*.log

# Swag
/docs
'''
with open('repo/.gitignore', 'w', encoding='utf-8') as f:
    f.write(gitignore)

# Makefile
makefile = '''.PHONY: all build run test swag docker up dc-down clean

all: build swag

build:
	go build -o bin/server ./main.go

run:
	go run main.go

test:
	go test ./...

swag:
	swag init

docker:
	docker build -t yourproject:latest .

up:
	docker-compose up -d

dc-down:
	docker-compose down

clean:
	rm -rf bin/ docs/
'''
with open('repo/Makefile', 'w', encoding='utf-8') as f:
    f.write(makefile)

# Dockerfile
dockerfile = '''FROM golang:1.22-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o main main.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/

COPY --from=builder /app/main .
EXPOSE 8080

CMD ["./main"]
'''
with open('repo/Dockerfile', 'w', encoding='utf-8') as f:
    f.write(dockerfile)

# docker-compose.yml
dc_yml = '''version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - GIN_MODE=release
'''
with open('repo/docker-compose.yml', 'w', encoding='utf-8') as f:
    f.write(dc_yml)

# docker-compose.override.yml
dc_override = '''version: '3.8'
services:
  app:
    ports:
      - "8081:8080"  # override port
    volumes:
      - .:/app
    environment:
      - GIN_MODE=debug
    command: go run main.go
'''
with open('repo/docker-compose.override.yml', 'w', encoding='utf-8') as f:
    f.write(dc_override)

# README.md
readme = '''# Your Go Project

REST API на Gin + Swagger.

## Quick Start

```bash
make all
make run
```

Swagger: http://localhost:8080/swagger/index.html

## Docker

```bash
docker-compose up
```
'''
with open('repo/README.md', 'w', encoding='utf-8') as f:
    f.write(readme)

# example requests
with open('repo/examples/example.json', 'w', encoding='utf-8') as f:
    f.write('''{
  "ping": {
    "method": "GET",
    "url": "http://localhost:8080/ping",
    "response": {
      "message": "pong"
    }
  }
}''')

# curl collection
curl_collection = '''# Curl Examples

## Ping
```bash
curl -X GET http://localhost:8080/ping
```

## Swagger UI
http://localhost:8080/swagger/index.html
'''
with open('repo/examples/curl-examples.md', 'w', encoding='utf-8') as f:
    f.write(curl_collection)

# Swag annotations example
with open('repo/cmd/healthcheck.go', 'w', encoding='utf-8') as f:
    f.write('''// @title Your API
// @version 1.0
// @description REST API with Swagger
// @host localhost:8080
// @BasePath /

package main

import (
    "net/http"

    "github.com/gin-gonic/gin"
)

// PingExample godoc
// @Summary Ping the server
// @Description Simple ping endpoint
// @Tags healthcheck
// @Accept json
// @Produce json
// @Success 200 {object} map[string]string
// @Router /ping [get]
func Ping(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{
        "message": "pong",
    })
}
''')

# Создаем ZIP
with zipfile.ZipFile('output/full-repo-zip-level.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('repo'):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, 'repo')
            zipf.write(file_path, arcname)

print("ZIP создан: output/full-repo-zip-level.zip")
print("Структура:")
for root, dirs, files in os.walk('repo'):
    level = root.replace('repo', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for f in files:
        print(f"{subindent}{f}")
