from django.shortcuts import render
from django.http import HttpResponse


def new_post(request):
    return render(request, 'new_post.html')
