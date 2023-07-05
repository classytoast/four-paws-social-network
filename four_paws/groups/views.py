from django.shortcuts import render
from django.views.generic import ListView


def index(request):
    return render(request, 'groups/all_groups.html')
