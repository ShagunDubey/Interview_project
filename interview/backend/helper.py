from .models import Interview
from datetime import datetime
from django.utils import timezone

def check(email1,email2,start,end):
  candidate_slots = Interview.objects.filter(cand_email=email1)
  interviewer_slots = Interview.objects.filter(int_email=email2)
  start = datetime.strptime(start,'%Y-%m-%d %H:%M')
  start=timezone.make_aware(start)
  end = datetime.strptime(end,'%Y-%m-%d %H:%M')
  end=timezone.make_aware(end)

  for slot in candidate_slots:
    if (start < slot.start_time and end < slot.end_time) or (start > slot.start_time and end > slot.end_time):
      continue
    else:
      return False
  
  for slot in interviewer_slots:
    if (start < slot.start_time and end < slot.end_time) or (start > slot.start_time and end > slot.end_time):
      continue
    else:
      return False

  return True