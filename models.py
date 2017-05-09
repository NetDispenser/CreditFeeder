from django.db import models
from django.dispatch import receiver
from django.dispatch import dispatcher
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField
import datetime

class UserProfile(models.Model):
	user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
	is_parent = models.BooleanField(default=False)
	credit_balance = models.IntegerField(default=1000)
	students=PickledObjectField(default=[])
	assignments=PickledObjectField(default=[])#would have been better: "assignment_ids"

#@receiver(post_save, sender=User)
#def ensure_profile_exists(sender, **kwargs):
#    if kwargs.get('created', False):
#        UserProfile.objects.get_or_create(user=kwargs.get('instance'))

def user_post_save(sender, instance, signal, *args, **kwargs):
    # Creates user profile
    profile, new = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, sender=User)
#dispatcher.connect(user_post_save, signal=signals.post_save, sender=User)

class Assignment(models.Model):
	id=models.AutoField(primary_key=True)
	title=models.CharField(max_length=30,default="New")
	date=models.DateField(default=datetime.date.today())
	author_id=models.IntegerField(default=999)
	activity=models.CharField(max_length=30,blank=True)
	credits=models.IntegerField(default=1800)
	repeatable=models.BooleanField(default=True,blank=True)
	data=PickledObjectField()
