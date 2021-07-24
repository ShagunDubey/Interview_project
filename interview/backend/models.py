from django.db import models

# Create your models here.

class Participant(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField(primary_key=True)

  def __str__(self):
    return self.name + "(email:" + self.email + ")"

class Interview(models.Model):
  
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  int_email = models.ForeignKey(Participant,on_delete=models.CASCADE,related_name='interviewer')
  cand_email = models.ForeignKey(Participant,on_delete=models.CASCADE,related_name='candidate')
  
  def __str__(self):
    return str(self.start_time )+ "-" + str(self.end_time) + ","
