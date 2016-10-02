from django.shortcuts import render
from django.http import HttpResponse

def create_post_page(request):
    return render(request, 'create_post.html')
