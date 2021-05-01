from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Moisture, Humidity, Temperature, Light

def int_check(x,y,z,w):
    try:
        temp2 = int(x)
        temp3 = int(y)
        temp4 = int(z)
        temp5 = int(w)
    except ValueError:
        return False
    if temp2 > 0 and temp3 > 0 and temp4 > 0 and temp5 > 0:
        return True
    else:
        return False

def index(request):
    return render(request, 'field/index.html')

def editfld(request):
    return render(request, 'field/editfld.html')

def details(request):
    txt1 = Moisture.objects.latest('id')
    txt2 = Temperature.objects.latest('id')
    txt3 = Humidity.objects.latest('id')
    txt4 = Light.objects.latest('id')
    #mod_list = Modules.objects.order_by('-pub_date')[:1]
    context = { 'moisture': txt1, 'temperature': txt2, 'humidity': txt3, 'light': txt4 }
    return render(request, 'field/details.html', context)

def error(request):
    text1 = request.POST['mst']
    text2 = request.POST['tmp']
    text3 = request.POST['hmd']
    text4 = request.POST['lgt']
    temp1 = int_check(text1,text2,text3,text4)
    if not bool(text1) or not bool(text2) or not bool(text3) or not bool(text4) or not temp1:
        return render(request, 'field/editfld.html', {"error_message":"Invalid Input"})
    else:
        temp6 = Moisture(mois_field=text1, pub_date=timezone.now())
        temp6.save()
        temp7 = Humidity(hum_field=text3, pub_date=timezone.now())
        temp7.save()
        temp8 = Temperature(temp_field=text2, pub_date=timezone.now())
        temp8.save()
        temp9 = Light(int_field=text4, pub_date=timezone.now())
        temp9.save()
        return HttpResponseRedirect(reverse('field:details'))