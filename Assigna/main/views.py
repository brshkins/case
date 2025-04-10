from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def test1(request):
    return render(request, 'main/test1.html')

def test2(request):
    return render(request, 'main/test2.html')

def test3(request):
    return render(request, 'main/test3.html')