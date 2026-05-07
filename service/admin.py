from django.contrib import admin
from service.models import Contact
from django.contrib.auth.admin import UserAdmin
from .models import *

class ContactAdmin(admin.ModelAdmin):
    list_display=('username', 'email', 'add')
admin.site.register(Contact, ContactAdmin)


from django.contrib import admin
from .models import Poll, Profile, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question', 'college', 'created_at']
    list_filter = ['college']

# ✅ ONLY THIS
admin.site.register(Poll, PollAdmin)
admin.site.register(Profile)