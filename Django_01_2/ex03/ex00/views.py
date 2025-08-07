from django.shortcuts import render

# Create your views here.
def markdown_cheatsheet(request):
    return render(request, 'index.html')
