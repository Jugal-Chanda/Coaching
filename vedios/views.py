from django.shortcuts import render
from accounts.models import Batch
from classlinks.models import ClassLink,Subject
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from datetime import datetime

# Create your views here.

def subject_to_classlink(request):
    data = {}
    if request.GET:
        subject_id = request.GET.get('subject_id')
        subject = Subject.objects.get(pk = subject_id)
        classlinks = subject.classlink_set.all()
        data = serializers.serialize('json', classlinks)
        print(data)
    return JsonResponse(data,safe=False)




def vedio_links_students(request,id):
    context = {}
    subject = Subject.objects.get(pk=id)
    if request.POST:
        date_str = request.POST.get('date')
        search_date = datetime.strptime(date_str,'%d/%m/%Y').date()
        classlinks = subject.classlink_set.filter(classdate=search_date)
        # classlinks = subject.classlink_set.all().filter(classdate,search_date).order_by('classdate')

    else:
        classlinks = subject.classlink_set.all().order_by('classdate')

    vedios = []
    for classlink in classlinks:
        vedio = classlink.vedio_set.all().first()
        if vedio:
            vedio_id = vedio.url.split('=')[1]
            vedios.append({'title': vedio.title,'vedio_id': vedio_id,'classdate':classlink.classdate})
            context['vedios'] = vedios
    return render(request,'students/vedios.html',context)

def vedio_links_teachers(request,id):
    context = {}
    subject = Subject.objects.get(pk=id)
    classlinks = subject.classlink_set.all().order_by('classdate')
    vedios = []
    for classlink in classlinks:
        vedio = classlink.vedio_set.all().first()
        if vedio:
            vedio_id = vedio.url.split('=')[1]
            vedios.append({'title': vedio.title,'vedio_id': vedio_id,'classdate':classlink.classdate})
            context['vedios'] = vedios
    return render(request,'teachers/vedios.html',context)
