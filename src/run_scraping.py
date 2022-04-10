'''решение как запустить сторонний файл с django
https://stackoverflow.com/questions/42813453/how-to-run-django-setup-properly-from-within-a-stand-alone-python-file-inside'''  # noqa E501

import os
import sys
import asyncio

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE",
#  "myproject.settings") tried as well
os.environ["DJANGO_SETTINGS_MODULE"] = "job_finder.settings"

import django  # noqa E402
django.setup()


from django.db import DatabaseError  # noqa E402
from django.contrib.auth import get_user_model  # noqa E402

from scraping.models import Error, Vacancy, Url  # noqa E402
from scraping.parser import *  # noqa E402, E403

User = get_user_model()  # вернет пользователя, который есть в настройках джанго проекта: AUTH_USER_MODEL = 'accounts.MyUser'  # noqa E501

parsers = (
    (get_vac_from_indeed, 'indeed'),
    (get_vac_from_olx, 'olx'),
    (get_vac_from_jooble, 'jooble'),
    (get_vac_from_nofluffjobs, 'nofluffjobs'),
)

jobs, errors = [], []


def get_settings():
    """Собираем настройки для пользователейю
       Фильтруем пользователей кому отправлять (values - список словарей c id)
       Returns:
            set c парами место и язык
    """
    qs = User.objects.filter(send_email=True).values()  #фильтруем пользователей кому отправлять (values - список словарей c id)
    settings_set = set((q['location_id'], q['language_id']) for q in qs)
    return settings_set


def get_urls(_settings):
    """Получаем наборы url для парсинга """
    qs = Url.objects.all().values() # values выдает только ID
    url_dict = {(q['location_id'], q['language_id']): q['data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['location'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dict[pair]
        urls.append(tmp)
    return urls


async def main(value):
    func, url, location, language = value
    job, err = await loop.run_in_executor(None, func, url, location, language)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
urls = get_urls(settings)

# location = Location.objects.filter(slug='warsaw').first()
# language = Language.objects.filter(slug='python').first()
# import time

# start = time.time()

# cоздаем очередь задач в async
loop = asyncio.get_event_loop()
# создаем список задач
tmp_tasks = [
    (
        func,
        url_data['url_data'][key],
        url_data['location'],
        url_data['language'],
    )
    for url_data in urls
    for func, key in parsers
]
# запускаем таск на выполнение конкретной функции
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
# for url_data in urls:

#     for func, key in parsers:
#         url = url_data['url_data'][key]
#         j, e = func(url, location=url_data['location'], language=url_data['language'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()
# print(time.time() - start)

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Error(data=errors).save()

# with open('work.json', 'w') as f:
#         f.write(str(jobs))
