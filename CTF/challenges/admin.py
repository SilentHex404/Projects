from django.contrib import admin
from .models import Challenge , SolvedChallenge

admin.site.register(Challenge)
admin.site.register(SolvedChallenge)