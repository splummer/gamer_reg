from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Event, EventSchedule

class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'game_system', 'game_type', 'short_description', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 100})
        }
        help_texts = {
            'game_system': 'Please try to be consistent',
            'short_description': 'This is what will be used in hover text on the site and other space constrained layouts.',
            'description': 'Keep this exciting, concise, and informative. All games are considered to be for any skill/familiarity level player if you are looking for something else include it here.<br /><strong>Avoid ellipsis</strong>',
        }

class EventScheduleForm(forms.ModelForm):
    """
    Form to enter a given event into a given time
    """
    class Meta:
        model = EventSchedule
        fields = ['start_date', 'end_date', 'max_players', 'min_players']

    def __init__(self, *args, **kwargs):
        super(EventScheduleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'

EventScheduleFormSet = inlineformset_factory(Event, EventSchedule, form=EventScheduleForm)
