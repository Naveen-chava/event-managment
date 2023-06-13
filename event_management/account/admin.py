from django.contrib import admin

from account.models import User, UserProfile, StaffProfile

models = [User, UserProfile, StaffProfile]

admin.site.register(models)