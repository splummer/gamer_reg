from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Convention, EventSchedule

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'con/cons_index.html'
    context_object_name = 'latest_convention_list'

    def get_queryset(self):
        """Return the last five conventions."""
        return Convention.objects.order_by('-start_date')[:5]

class DetailView(generic.DetailView):
    model = Convention
    slug_field = 'convention_key'
    template_name = 'con/conevents_detail.html'
    """
    Maybe it is better to do this? except I cannot get it to work.

    def get_object(self):
        return get_object_or_404(Convention, pk=self.convention_key)
    """

class ResultsView(generic.DetailView):
    model = Convention
    slug_field = 'convention_key'
    template_name = 'con/results.html'

def events(request, convention_key):
    convention = get_object_or_404(Convention, convention_key=convention_key)
    return render(request, 'con/conevents_detail.html', {'convention': convention})

def signup(request, convention_key):
    convention = get_object_or_404(Convention, convention_key=convention_key)
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
        return HttpResponseRedirect(reverse('con:results', args=(convention.convention_key,)))


