from django.contrib.auth.models import User
import datetime

class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            notifications = []

            today = datetime.datetime.today()
            usrobj = User.objects.get(username=user.username)
            usrobj.profile.last_seen = today.astimezone() # astimezone is used to avoid naive datetimeobject
            usrobj.profile.save()
            
            streak_date = datetime.datetime.strptime(usrobj.learnerprofile.plan[0][1],"%Y-%m-%d").date()
            if streak_date == today.date()-datetime.timedelta(days=2):
                usrobj.learnerprofile.plan[0][0] = 0
                #user.plan[0][1] = today.strftime("%Y-%m-%d")
                usrobj.learnerprofile.save()
            
            notif = user.notification_set.all()
            for n in notif:
                notifications.append({
                    "created":n.created.strftime("%I:%M"),
                    "type":n.type,
                    "sender":n.sender.username,
                    "content":n.content
                })
        else:
            notifications = []

        request.notifications = notifications
        
        response = self.get_response(request)
        return response