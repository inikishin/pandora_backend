run:
	python manage.py runserver 8001

rebuild:
	docker build --no-cache -t pandora-backend .
	docker container stop pandora-backend
	docker container rm pandora-backend
	docker run --network pandora --mount source=pandora_static,target=/app/static --name pandora-backend -d pandora-backend