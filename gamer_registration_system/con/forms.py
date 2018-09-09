from django import forms

from .models import Event

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
