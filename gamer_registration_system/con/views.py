from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django import forms

from .models import Convention, EventSchedule, Event
from .forms import EventCreateForm

# Create your views here.
class ConventionIndexView(ListView):
    template_name = 'con/cons_index.html'
    context_object_name = 'latest_convention_list'

    def get_queryset(self):
        """Return the last five conventions."""
        return Convention.objects.order_by('-start_date')[:5]

class ConventionDetailView(DetailView):
    model = Convention
    slug_field = 'key'
    template_name = 'con/conevents_detail.html'
    """
    Maybe it is better to do this? except I cannot get it to work.

    def get_object(self):
        return get_object_or_404(Convention, pk=self.key)
    """

class ResultsView(DetailView):
    model = Convention
    slug_field = 'convention_key'
    template_name = 'con/results.html'

def events(request, convention_key):
    convention = get_object_or_404(Convention, key=convention_key)
    return render(request, 'con/conevents_detail.html', {'convention': convention})

def signup(request, convention_key):
    convention = get_object_or_404(Convention, key=convention_key)
    try:
        selected_event = convention.eventschedule_set.get(pk=request.POST['eventsignup'])
    except (KeyError, EventSchedule.DoesNotExist):
        # Redisplay the form
        return render(request, 'con/conevents_detail.html', {
            'convention': convention,
            'error_message': "You didn't select an event",
        })
    else:
        selected_event.num_of_players += 1
        selected_event.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('con:results', args=(convention.key,)))

class EventCreateView(LoginRequiredMixin, CreateView):
    form_class = EventCreateForm
    template_name = 'con/event_form.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Add in the convention data
        context['convention'] = Convention.objects.get(key=self.kwargs['convention_key'])
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.convention = Convention.objects.get(key=self.kwargs['convention_key'])
        return super().form_valid(form)

class EventDetailView(DetailView):
    model = Event
    template_name = 'con/event_detail.html'

class EventScheduleCreateView(CreateView):
    """
    Takes a given event as input and lets you select when that event should be run.
    This is going to be hard:
        1. How do you allow arbitrary numbers of times to be selected?
        2. Ideally you can select multiple times in one entry.
    """
    pass
