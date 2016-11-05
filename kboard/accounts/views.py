from django.shortcuts import render

def tns_page(request):
    return render(request, 'terms.html')
