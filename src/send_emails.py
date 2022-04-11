import os
import sys

import django
import datetime
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE",
#  "myproject.settings") tried as well
os.environ["DJANGO_SETTINGS_MODULE"] = "job_finder.settings"

django.setup()

from scraping.models import Vacancy, Error, Url
from job_finder.settings import EMAIL_HOST_USER

ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()

subject = f"mailing of vacancies of {today}"
text_content = f"mailing of vacancies {today}"
from_email = EMAIL_HOST_USER

empty = '<h2>Unfortunately, there is no data for your request</h2>'

User = get_user_model()
qs = User.objects.filter(send_email=True).values(
    'location', 'language', 'email'
)
users_dct = {}
for u in qs:
    # создаем словарь(ключ= ( location_id, language_id): значение= email)
    users_dct.setdefault((u['location'], u['language']), [] )
    users_dct[(u['location'], u['language'])].append(u['email'])
if users_dct:
    params = {'location_id__in': [], 'language_id__in': []}
    for pair in users_dct.keys():
        params['language_id__in'].append(pair[0])
        params['location_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params)[:10]

    vacancies = {}
        # for ii in qs:
        #     vacancies.setdefault((ii['location_id'], ii['language_id']), [])
        #     vacancies[(ii['location_id'], ii['language_id'])].append(ii)
        # for keys, emails in users_dict.items():
        #     rows = vacancies.get(keys, [])
        #     html = ''
        #     for row in rows:
        #         html += f'<h3><a href="{row["url"]}">{row["title"]}</a></h3>'
        #         html += f'<p>{row["description"]}</p>'
        #         html += f'<p>{row["company"]}</p><br><hr>'
        #     _html = html if html else empty
        #     for email in emails:
        #         to = email
        #         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        #         msg.attach_alternative(_html, "text/html")
        #         msg.send()

qs = Error.objects.filter(timestamp=today)

subject = ''
text_content = ''
_html = ''
to = ADMIN_USER
if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    
    for d in data:
        _html += f'<p><a href="{d["url"]}">Error : {d["title"]}</a></p><br>'
    subject = f"Errors of scraping of {today} "
    text_content = f"Errors of scraping of {today} "

    data = error.data.get('user_data', [])
    
    if data:
        _html += '<hr>'
        _html += "User's wishes"
    for d in data:
        _html += f'<p>Location : {d["location"]}, Language:{d["language"]}, Email: {d["email"]}</p><br>'
    subject = f"User's wishes {today} "
    text_content = f"User's wishes {today} "


    
qs = Url.objects.all().values('location', 'language')
urls_dict = {(i['location'], i['language']): True for i in qs}
urls_errors = ''
for keys in users_dct.keys():
    if keys not in urls_dict:
        if keys[0] and keys[1]:
            urls_errors += f'<p> For location :{keys[0]} and programming language: {keys[1]} do not exists vacancies</p><br>'
if urls_errors:
    subject += 'missing vacancies'
    _html += urls_errors
if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()

