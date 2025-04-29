from django.shortcuts import redirect, render

def register(request):
    return render(request, './account/register.html')
