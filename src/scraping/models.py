from django.db import models
from django.utils.text import slugify
from django.urls import reverse

def default_urls():
    return {
        'indeed': '',
        'olx': '',
        'from_jooble': '',
        'nofluffojbs': ''
    }

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, null=True, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


class Language(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Programming language',
                            unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Programming language'
        verbose_name_plural = 'Programming languages'


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    city = models.CharField(max_length=50)
    title = models.CharField(max_length=250, verbose_name='Title of vacancy')
    company = models.CharField(max_length=250, verbose_name='Company')
    description = models.TextField(verbose_name='Description of vacancy')
    location = models.ForeignKey('Location', on_delete=models.CASCADE, verbose_name='Location')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Language')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
        ordering = ['-timestamp']


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()


class Url(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE, verbose_name='Location')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Language')
    data = models.JSONField(default=default_urls)

    class Meta:
        unique_together = ('location', 'language')  # два параметра вместе уникальны
