from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Interview,Participant
from django.contrib import messages
from datetime import datetime
from .helper import check
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def create(request):
  if request.method == 'POST':
    start = request.POST.get('start_date',False)
    end = request.POST.get('end_date',False)
    
    int_email = str(request.POST['interviewer'])
    cand_email = str(request.POST['candidate'])
    
    if(int_email == cand_email):
      messages.add_message(request,messages.WARNING,'Minimum 2 participants required. Please try again.')
      return HttpResponseRedirect(reverse('create'))
    elif start >= end:
      messages.add_message(request,messages.WARNING,'Invalid time slot.')
      return HttpResponseRedirect(reverse('create'))

    elif not check(int_email,cand_email,start,end):
      messages.add_message(request,messages.WARNING,'Time slot not available. Please try again.')
      return HttpResponseRedirect(reverse('create'))
    else:
      candidate = Participant.objects.get(pk=cand_email)
      interviewer = Participant.objects.get(pk=int_email)
      interviewObj = Interview(start_time=start, end_time=end,cand_email=candidate,int_email=interviewer)
      interviewObj.save()
      messages.add_message(request,messages.SUCCESS,"Interview has been created successfully.")
    #  send_mail("Interview","Your interview has been setup.",settings.EMAIL_HOST_USER,[cand_email])

  interviews = Interview.objects.all()
  participants = Participant.objects.all()
  context={
    'interviews':interviews,
    'participants':participants,
  }
  return render(request,'home.html',context=context)

def update_request(request,pk):
  if request.method == 'POST':
    obj = Interview.objects.get(pk=pk)
    context={
      'slot':obj
    }
    
    return render(request,'update.html',context=context)

def update(request):
  if request.method == 'POST':
    pk = request.POST.get('pk',False)
    start = request.POST.get('start_date',False)
    end = request.POST.get('end_date',False)
    obj = Interview.objects.get(pk=pk)
    int_email = obj.int_email
    cand_email = obj.cand_email
    if start >= end:
      messages.add_message(request,messages.WARNING,'Invalid time slot.')
      return HttpResponseRedirect(reverse('create'))

    elif not check(int_email,cand_email,start,end):
      messages.add_message(request,messages.WARNING,'Time slot not available. Please try again.')
      return HttpResponseRedirect(reverse('create'))
    else:
      
      obj.start_time = start
      obj.end_time = end
      obj.save()
      messages.add_message(request,messages.SUCCESS,"Interview slot has been updated successfully.")
      return HttpResponseRedirect(reverse('create'))

def delete(request):
  if request.method=='POST':
    obj_id=(request.POST['del'])
    obj = Interview.objects.get(pk=obj_id)
    obj.delete()
    messages.add_message(request,messages.WARNING,'Interview removed')
    return HttpResponseRedirect(reverse('create'))

  return render(request,'home.html')