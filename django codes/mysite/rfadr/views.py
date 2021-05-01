#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Rfadd, Modstatus

#def stat_check(x):
#    num = int(x)
#    if num == 1:
#        text2 = "Module added"
#    else:
#        text2 = "Module removed"
#    return text2


def index(request):
    return render(request, 'rfadr/index.html')

def editadr(request):
    return render(request, 'rfadr/editadr.html')

def details(request):
    text1 = Rfadd.objects.latest('id')
    text2 = Modstatus.objects.latest('id')
    context = { 'address': text1, 'modstat': text2 }
    return render(request, 'rfadr/details.html', context)

def error(request):
    adr = request.POST['add']
    try:
        stat = request.POST['status']
    except:
        return render(request, 'rfadr/editadr.html', {"error_message":"Complete data not entered"})
    if not bool(adr):
        return render(request, 'rfadr/editadr.html', {"error_message":"Complete data not entered"})
    else:
        temp = Rfadd(rf_adr=adr, pub_date=timezone.now())
        temp.save()
        temp1 = Modstatus(status=stat, pub_date=timezone.now())
        temp1.save()
        return HttpResponseRedirect(reverse('rfadr:details'))

