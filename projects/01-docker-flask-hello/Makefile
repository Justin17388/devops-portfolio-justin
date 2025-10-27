.PHONY: run test docker

run:
	python app/app.py

test:
	pytest -q

docker:
	docker build -t flask-hello:dev .
