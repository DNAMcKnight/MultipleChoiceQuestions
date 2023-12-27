from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class MCQ(models.Model):
    question= models.CharField(max_length=500)
    options= models.JSONField()
    answer= models.CharField(max_length=100)
    bangla=models.BooleanField()
def __str__(self):
        return self.question
    
class Import(models.Model):
    file = models.FileField(upload_to='app/')
    
class UserQuestions(models.Model):
    encoded_id = models.TextField(default="",blank=True)
    used_question = models.JSONField()
    user=models.ForeignKey(User,to_field='username',on_delete=models.CASCADE)
    
class UserInfo(models.Model):
    correct = models.IntegerField()
    incorrect = models.IntegerField()
    phone = models.CharField(max_length=50)
    user=models.ForeignKey(User,to_field='username',on_delete=models.CASCADE)