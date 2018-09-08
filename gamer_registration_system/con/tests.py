import datetime

from django.test import TestCase
from django.utils import timezone

from .models import *

# Create your tests here.
class EventScheduleModelTests(TestCase):
    new_con = Convention(convention_name='Test Future Con')
    new_event = Event(convention=new_con, title='Test Future Event')

    def test_recent_event_with_future_start(self, new_con=new_con, new_event=new_event):
        """
        recent_event() returns False for events whose start_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_eventsched = EventSchedule(convention=new_con, event=new_event, start_date=time)
        self.assertIs(future_eventsched.recent_event(), False)

    def test_recent_event_with_old_event(self, new_con=new_con, new_event=new_event):
        """
        recent_event() returns False for events whose start_date is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_event = EventSchedule(convention=new_con, event=new_event, start_date=time)
        self.assertIs(old_event.recent_event(), False)

    def test_recent_event_with_recent_question(self, new_con=new_con, new_event=new_event):
        """
        recent_event() returns True for events whose start_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_event = EventSchedule(convention=new_con, event=new_event, start_date=time)
        self.assertIs(recent_event.recent_event(), True)
