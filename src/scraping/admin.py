from django.contrib import admin

from .models import Language, Location, Vacancy


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {"slug": ("name",)}


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {"slug": ("name",)}


class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'city', 'url', 'company', 'description',
        'location', 'language', 'timestamp',
    )

admin.site.register(Location, LocationAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Vacancy, VacancyAdmin)
