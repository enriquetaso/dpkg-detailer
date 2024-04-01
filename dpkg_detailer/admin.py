from django.contrib import admin
from .models import Package, Dependency

admin.site.register(Package)
admin.site.register(Dependency)
