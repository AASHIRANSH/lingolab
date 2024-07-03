from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, LearnerProfile
import datetime

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        LearnerProfile.objects.create(user=instance, plan=[[0,datetime.datetime.today().date().strftime("%Y-%m-%d"),0],5,10])
        instance.profile.learnings = {"courses": {"current": 0, "enrolled": [1]}, "vocab": [5,5], "stats":[]}

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()