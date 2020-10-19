from django.shortcuts import render
from accounts.models import Batch
from classlinks.models import ClassLink,Subject
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse

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

def batch_to_subjects(request):
    data = {}
    if request.GET:
        batch_id = request.GET.get('batch_id')
        batch = Batch.objects.get(pk=batch_id)
        if batch:
            subjects = batch.subject_set.all()
            data = serializers.serialize('json', subjects)
        print(data)
    return JsonResponse(data,safe=False)


def vedio_links_students(request,id):
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
