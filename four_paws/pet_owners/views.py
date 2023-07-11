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

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Owner.objects.get(pk=self.kwargs['id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.id == self.kwargs['id']:
            title = "Мой профиль"
        else:
            title = f"Профиль {Owner.objects.get(pk=self.kwargs['id']).username}"
        if self.request.user.is_authenticated:
            c_def = self.get_user_context(id=self.request.user.id, title=title,
                                          is_authenticated=True)
        else:
            c_def = self.get_user_context(title=title, is_authenticated=False)
        context.update(c_def)
        return context


def register(request):
    return render(request, 'pet_owners/register_page.html')


def login(request):
    return render(request, 'pet_owners/login_page.html')
