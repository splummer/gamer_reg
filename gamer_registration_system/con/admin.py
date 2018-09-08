from django import forms
from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Convention, Day, Badge, Event, EventSchedule

class EventForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    class Meta:
        model = Event
        fields = '__all__'

class EventAdmin(admin.ModelAdmin):
    form = EventForm

# Register your models here.
admin.site.register(Convention)
admin.site.register(Day)
admin.site.register(Badge)
admin.site.register(Event, EventAdmin)
admin.site.register(EventSchedule)
