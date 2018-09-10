import datetime

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Convention(models.Model):
    name = models.CharField('Convention Name', max_length=100)
    key = models.CharField('Convention Key', max_length=10, unique=True, null=False)
    start_date = models.DateTimeField('Convention start time')
    end_date = models.DateTimeField('Convention end time')
    venue = models.CharField('Venue Name', max_length=100)
    street_address = models.CharField('Street Address', max_length=100)
    city = models.CharField('City', max_length=50)
    state = models.CharField('State', max_length=2)
    zip_code = models.CharField('Zip Code', max_length=5)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]
        ordering = ['-name']
        verbose_name = 'convention'
        verbose_name_plural = 'conventions'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('con:convention-detail', args=[str(self.id)])

    def schedule(self):
        return EventSchedule.objects.filter(event__convention=self)

class Day(models.Model):
    convention = models.ForeignKey(Convention, on_delete=models.CASCADE)
    day_name = models.CharField('Day Name', max_length=20)
    start_date = models.DateTimeField('Start time')
    end_date = models.DateTimeField('End Time')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.day_name

class Badge(models.Model):
    convention = models.ForeignKey(Convention, on_delete=models.CASCADE)
    badge_name = models.CharField('Badge Name', max_length=20)
    cost = models.FloatField('Additional Cost', default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.badge_name

class Event(models.Model):
    GAME_TYPE_CHOICES = (
        ('Board', 'Board Game'),
        ('RolePlaying', 'Role-Playing'),
        ('CollectibleCard', 'Collectible Card'),
        ('LARP', 'LARP'),
        ('Seminar', 'Seminar'),
    )
    convention = models.ForeignKey(
        Convention,
        on_delete=models.CASCADE,
        related_name='events',
        related_query_name='event',
    )
    title = models.CharField('Title', max_length=70)
    game_system = models.CharField('Game System', max_length=70)
    game_type = models.CharField(
        'Game Type',
        max_length=20,
        choices=GAME_TYPE_CHOICES,
    )
    additional_cost = models.FloatField('Additional Cost', default=0.00, null=True, blank=True)
    description = models.CharField('Description', max_length=1200)
    short_description = models.CharField('Short Description', max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return "%s at %s" % (self.title, self.convention.name)

    def get_absolute_url(self):
        return reverse('con:event-detail', args=[str(self.convention.key), str(self.id)])

    def event_schedule(self):
        return self.schedules.prefetch_related('schedules')

class EventSchedule(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='schedules',
        related_query_name='schedule',
    )
    start_date = models.DateTimeField('Start time')
    end_date = models.DateTimeField('End Time')
    min_players = models.IntegerField('Minimum Players')
    max_players = models.IntegerField('Maximum Players')
    room = models.CharField('Room', max_length=100, blank=True)
    num_of_players = models.IntegerField('Current Number of Players', default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    players = models.ManyToManyField(User, related_name="event_schedule", blank=True)
    gms = models.ManyToManyField(User, related_name="events_gming", blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s starting at %s at %s" % (self.event.title, self.start_date, self.event.convention.name)

    def starting_soon(self):
        return self.start_date <= timezone.now() + datetime.timedelta(hours=4)

    def recent_event(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.start_date <= now
