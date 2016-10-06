from django.shortcuts import render
from django.http import HttpResponse

def new_post(request):
    return render(request, 'new_post.html')

def post_list(request):
    return render(request, 'post_list.html')

