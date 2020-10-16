from django.shortcuts import render
from classlinks.models import ClassLink,Subject

# Create your views here.

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
