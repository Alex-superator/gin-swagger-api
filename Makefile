.PHONY: all build run test swag docker up dc-down clean

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
	docker build -t crudlGo:latest .

up:
	docker-compose up -d

dc-down:
	docker-compose down

clean:
	rm -rf bin/ docs/
