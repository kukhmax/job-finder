'''решение как запустить сторонний файл с django
https://stackoverflow.com/questions/42813453/how-to-run-django-setup-properly-from-within-a-stand-alone-python-file-inside'''

import os
import sys



proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings") tried as well
os.environ["DJANGO_SETTINGS_MODULE"] = "job_finder.settings"

import django
django.setup()


from scraping.models import Language, Location, Vacancy, Error
from scraping.parser import *
from django.db import DatabaseError

parsers = (
    (get_vac_from_indeed, 'https://pl.indeed.com/jobs?q=python%20junior&l=Warszawa%2C%20mazowieckie&vjk=e9f46c76587e2d7b'),
    (get_vac_from_olx, 'https://www.olx.pl/praca/informatyka/warszawa/q-python/'),
    (get_vac_from_jooble, 'https://pl.jooble.org/SearchResult?date=3&rgns=Warszawa&ukw=junior%20python'),
    (get_vac_from_nofluffjobs, 'https://nofluffjobs.com/pl/praca-it/warszawa/backend?criteria=seniority%3Djunior%20requirement%3Dpython&page=1'),
)
location = Location.objects.filter(slug='warsaw').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, location=location, language=language)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Error(data=errors).save()

# with open('work.json', 'w') as f:
#         f.write(str(jobs))
