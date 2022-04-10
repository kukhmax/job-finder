MANAGE := python manage.py

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

shell:
	$(MANAGE) shell

run:
	$(MANAGE) runserver

messages:
	$(MANAGE) makemessages -l ru

compile:
	$(MANAGE) compilemessages --ignore=cache --ignore=.venv/*/locale

superuser:
	$(MANAGE) createsuperuser

lint:
	flake8