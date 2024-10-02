from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, LearnerProfile
import datetime

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    datestr = datetime.datetime.today().date().strftime("%Y-%m-%d")
    if created:
        Profile.objects.create(user=instance)
        LearnerProfile.objects.create(user=instance, plan=[[0,datestr,0],[5,5],[datestr,[]]])
        instance.profile.learnings = {"xp": 0, "courses": {"current": 0, "enrolled": [1]}, "vocab": [[0,datestr,0],[5,5],[datestr,[]]], "stats":[], "games": {"wordscapes": [0, 0], "name_that_thing":[0,0], "word_search":[0,0]}}

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()