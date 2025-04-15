from django.contrib import admin
from .models import TestResult, Profession, MBTIResult

admin.site.register(TestResult)
admin.site.register(Profession)
admin.site.register(MBTIResult)