migrations:
	python3 archaos/manage.py makemigrations

migrate:
	python3 archaos/manage.py migrate

runserver:
	python3 archaos/manage.py runserver

collectstatic:
	python3 archaos/manage.py collectstatic

superuser:
	python3 archaos/manage.py createsuperuser
