run:
	python manage.py runserver 8001

rebuild:
	docker build --no-cache -t pandora-backend .
	docker run --network pandora --name pandora-backend --rm -d pandora-backend