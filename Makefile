# Makefile
up:
\tdocker compose -f deploy/docker-compose.yml up -d --build

pull:
\tdocker compose -f deploy/docker-compose.yml pull app && docker compose -f deploy/docker-compose.yml up -d

down:
\tdocker compose -f deploy/docker-compose.yml down

slow:
\tsed -i.bak 's/# @app.get/@@@/; s/# def hello/@@@/; s/#     start/@@@/; s/#     time.sleep/@@@/; s/#     dur/@@@/' app/main.py

load:
\they -z 20s -q 50 http://localhost:8080/api/hello
