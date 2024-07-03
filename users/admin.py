from django.contrib import admin
from .models import Profile, LearnerProfile, Contact, Friend, Notification, Notes

admin.site.register(Profile)
admin.site.register(LearnerProfile)
admin.site.register(Friend)
admin.site.register(Contact)
admin.site.register(Notification)
admin.site.register(Notes)