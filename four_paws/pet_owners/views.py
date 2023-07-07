from django.shortcuts import render
from django.views.generic import ListView

from .utils import DataMixin
from .models import *

def index(request):
    return render(request, 'pet_owners/main_page.html')

class ProfileHome(DataMixin, ListView):
    """Страница профиля"""
    model = Owner
    template_name = 'pet_owners/profile_page.html'
    context_object_name = 'profile'

    '''def get_queryset(self):
        return Owner.objects.get(pk=self.kwargs['id'])'''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Мой профиль")
        context.update(c_def)
        return context
