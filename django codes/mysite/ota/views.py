from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Modules

def int_check(x):
    try:
        temp2 = int(x)
    except ValueError:
        return False
    if temp2 > 0:
        return True
    else:
        return False

def index(request):
    return render(request, 'ota/index.html')

def details(request):
    id = Modules.objects.latest('id')
    #mod_list = Modules.objects.order_by('-pub_date')[:1]
    context = { 'mod_list': id }
    return render(request, 'ota/details.html', context)

def editmod(request):
    return render(request, 'ota/editmod.html')

def error(request):
    text = request.POST['num']
    temp1 = int_check(text)
    if not bool(text) or not temp1:
        return render(request, 'ota/editmod.html', {"error_message":"Invalid input"})
    else:
        temp = Modules(num_mod=text, pub_date=timezone.now())
        temp.save()
        return HttpResponseRedirect(reverse('ota:details'))
