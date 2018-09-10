from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django import forms
from django.forms import modelformset_factory

from .models import Convention, EventSchedule, Event
from .forms import EventCreateForm, EventScheduleForm, EventScheduleFormSet

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
    template_name = 'con/cons_detail.html'
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

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and setups blank ersion of the form and inline formsets
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        eventschedule_form = EventScheduleFormSet()
        return self.render_to_response(self.get_context_data(form=form,
                                                             eventschedule_form=eventschedule_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instatiating form instance and its inline formsets
        with the passed POST variables and then checking them for validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        eventschedule_form = EventScheduleFormSet(self.request.POST)
        if (form.is_valid() and eventschedule_form.is_valid()):
            return self.form_valid(form, eventschedule_form)
        else:
            return self.form_invalid(form, eventschedule_form)

    def form_valid(self, form, eventschedule_form, **kwargs):
        """
        Called if all forms are valid. Creates a Event instance along with
        associated EventSchedule and then redirects to a success page.
        """
        form.instance.creator = self.request.user
        form.instance.convention = Convention.objects.get(key=self.kwargs['convention_key'])
        self.object = form.save()
        scheduled_event = eventschedule_form.save(commit=False)
        for scheduled_event in scheduled_event:
            scheduled_event.creator = self.request.user
        eventschedule_form.instance = self.object
        eventschedule_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, eventschedule_form):
        """
        Called if a form is invalid. Re-renders the context data with the data-filled forms and errors.
        """
        return self.render_to_response(self.get_context_data(form=form, eventschedule_form=eventschedule_form))

class EventDetailView(DetailView):
    model = Event
    template_name = 'con/event_detail.html'
