from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect

# forms
from users.forms import SignUpForm, EditUserProfileForm, EditAdminProfileForm, SignInForm, ProfileUpdateForm, ContactForm
from django.contrib import messages

# models
from django.contrib.auth.models import User
from users.models import Contact, Friend, Notification, LearnerProfile, Profile, Notes

from django.http import JsonResponse


from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

import datetime, json

def userlog(request):
    pk = request.GET.get("user") or 1
    user = User.objects.get(id=pk)
    usr_pr = user.profile.last_seen or user.last_login
    
    return render(request, "userlog.html", {"usr_pr":usr_pr})

from django.core.paginator import Paginator
def users(request):
    datag = request.GET
    if datag.get("users") == "friends":
        users = Friend.objects.all()
        type = "friends"
    else:
        users = User.objects.exclude(username=request.user.username)
        type = "users"

    paginator = Paginator(users, 5)  # Show 5 contacts per page.
    page_number = datag.get("page")
    page_obj = paginator.get_page(page_number)

    vars = {
        "users":users,
        "page_obj": page_obj,
        "type":type
    }
    return render(request, "users.html", vars)


def user_detail(request, id):
    user_obj = User.objects.get(pk=id)
    current_user = request.user
    form = EditUserProfileForm(instance=user_obj)
    p_form = ProfileUpdateForm(instance=user_obj.profile)


    datap = request.GET
    ''' current user-friend object '''
    fr_other_obj = Friend.objects.filter(user=user_obj, friend=request.user).first()
    ''' other user-friend object'''
    fr_own_obj = Friend.objects.filter(user=request.user, friend=user_obj).first()
    if datap.get("action"):
        if datap.get("action") == "accept":
            Notification.objects.filter(sender=user_obj, type="friend request")
            fr_other_obj.is_friend = True
            fr_other_obj.save()
            messages.success(request, f'You have become a friend of "{user_obj.username}"')
            return HttpResponseRedirect(request.path)
    
        if datap.get("action") == "cancel":
            if fr_own_obj:
                fr_own_obj.delete()
                messages.success(request, f"You have cancelled the friend request.")
                return HttpResponseRedirect(request.path)
            elif fr_other_obj:
                fr_other_obj.delete()
                messages.success(request, f"You have cancelled the friend request.")
                return HttpResponseRedirect(request.path)
        
        if datap.get("action") == "befriend":
            if fr_own_obj:
                if fr_own_obj.is_friend:
                    messages.error(request, f"You are already a friend of {user_obj.username}")
                else:
                    messages.warning(request, f"You have already sent friend request to {user_obj.username}")
                    return HttpResponseRedirect(request.path)
            elif fr_other_obj:
                if fr_other_obj.is_friend:
                    messages.error(request, f"You are already a friend of {user_obj.username}")
                else:
                    fr_other_obj.is_friend = True
                    fr_other_obj.save()
                    messages.success(request, f"Friend request has been sent to {user_obj.username}")
                    return HttpResponseRedirect(request.path)

            else:
                Friend.objects.create(user=request.user, friend=user_obj)
                Notification.objects.create(sender=current_user, type="friend request", receiver=user_obj)

                messages.success(request, f"Friend request has been sent to {user_obj.username}")

        elif datap.get("action") == "unfriend":
            fr_obj = Friend.objects.filter(user=request.user, friend=user_obj) | Friend.objects.filter(user=user_obj, friend=request.user)
            if fr_obj.exists():
                fr_obj.first().delete()
            messages.warning(request, f'You are no longer friend of "{user_obj.username}".')
            return HttpResponseRedirect(request.path)

    if fr_own_obj:
        if fr_own_obj.is_friend:
            fr_own_obj = True
            fr_req = True
        else:
            fr_own_obj = True
            fr_req = "request_sent"
    else:
        fr_own_obj = False
        fr_req = False

    if fr_other_obj:
        if fr_other_obj.is_friend:
            fr_other_obj = True
            fr_req = True
        else:
            fr_other_obj = True
            fr_req = "request_received"
    else:
        fr_other_obj = False
        fr_req = False if fr_req == False else fr_req

    vars = {
        'user':user_obj,
        'form':form,
        'p_form':p_form,
        "is_friend":fr_own_obj or fr_other_obj,
        "fr_req":fr_req
    }
    return render(request, "userdetail.html", vars)

def chat(request):
    contacts = Friend.objects.all()

    vars = {
        "contacts":contacts
    }
    return render(request,"chat.html",vars)

#Registration
def sign_up(request):
    if not request.user.is_authenticated:
        fm = SignUpForm(request.POST or None)
        if request.method == "POST":
            if fm.is_valid():
                fm.save()
                messages.success(request,'Your Account was Created!')
                return redirect('sign_in')
                # messages.add_message(request, messages.SUCCESS, 'Your Account Has Been Created!')
            else:
                messages.error(request,'Please check for any errors below!')

        return render(request, "sign_up.html", {'fm':fm})
    else:
        return redirect('profile')


'''Sign In / Login'''
def sign_in(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            # fm = AuthenticationForm(request=request, data=request.POST)
            fm = SignInForm(request=request, data=request.POST) #custom login form
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request,'Loggen In Successfully!')
                    return HttpResponseRedirect('/users/profile/')
                # messages.add_message(request, messages.SUCCESS, 'Your Account Has Been Created!')
            else:
                messages.error(request,'Please check for any errors below!')
        else:
            fm = SignInForm() # fm = AuthenticationForm()
        return render(request, "sign_in.html", {'form':fm})
    else:
        next = request.GET.get("next")
        next = next if next else "/"
        messages.success(request,"You are logged in.")
        return HttpResponseRedirect(next)
        

def user_profile(request):
    if request.user.is_authenticated:

        if request.method == 'POST':

            if request.user.is_superuser:
                fm = EditAdminProfileForm(request.POST, instance=request.user)
            else:
                fm = EditUserProfileForm(request.POST, instance=request.user)

            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            
            if fm.is_valid() and p_form.is_valid():
                fm.save()
                p_form.save()
                messages.success(request, f'Profile updated!!')
            return redirect('profile')
        else:
            if request.user.is_superuser:
                fm = EditAdminProfileForm(instance=request.user)
            else:
                fm = EditUserProfileForm(instance=request.user)

            p_form = ProfileUpdateForm(instance=request.user.profile)

        vars = {
            'form':fm,
            'p_form': p_form,
            'user':request.user,
            "friends":Friend.objects.filter(user=request.user) | Friend.objects.filter(friend=request.user)
        }

        return render(request, "profile.html", vars)
    
    else:
        return HttpResponseRedirect('/users/signin')

def change_profile(request):
    if request.user.is_authenticated:

        if request.method == 'POST':

            if request.user.is_superuser:
                fm = EditAdminProfileForm(request.POST, instance=request.user)
            else:
                fm = EditUserProfileForm(request.POST, instance=request.user)

            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            
            if fm.is_valid() and p_form.is_valid():
                fm.save()
                p_form.save()
                messages.success(request, f'Profile updated!!')
                return redirect('profile')
            else:
                messages.error(request, f'There was an error!!')
        else:
            if request.user.is_superuser:
                fm = EditAdminProfileForm(instance=request.user)
            else:
                fm = EditUserProfileForm(instance=request.user)

            p_form = ProfileUpdateForm(instance=request.user.profile)

        vars = {
            'form':fm,
            'p_form': p_form,
            'user':request.user
        }

        return render(request, "profile_change.html", vars)
    
    else:
        return HttpResponseRedirect('/users/signin')
 


def sign_out(request):
    logout(request)
    return redirect('sign_in')

'''change password with old password'''
def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid() :
                fm.save()
                update_session_auth_hash(fm.user)
                messages.success(request,'Password was changed Successfully!')
                return HttpResponseRedirect('/users/profile')
        else:
            fm = PasswordChangeForm(user=request.user)
        vars = {
            'form':fm
        }
        return render(request, "change_password.html", vars)
    else:
        return HttpResponseRedirect('/users/signin')

'''change password without old password'''
def change_password2(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = SetPasswordForm(user=request.user, data=request.POST)
            if fm.is_valid() :
                fm.save()
                update_session_auth_hash(fm.user)
                messages.success(request,'Password was changed Successfully!')
                return HttpResponseRedirect('/users/profile')
        else:
            fm = SetPasswordForm(user=request.user)
        vars = {
            'form':fm
        }
        return render(request, "change_password.html", vars)
    else:
        return HttpResponseRedirect('/users/signin')


from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
        "if an account exists with the email you entered. You should receive them shortly." \
        " If you don't receive an email, " \
        "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('sign_in')


def custom_url(request, year):
    vars = {'year':year}
    return render(request, 'custom_url.html', vars)


def contact_us(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            req_post = request.POST.copy()
            req_post.update({'operator':request.user})
            form.save()
            messages.success(request, "Your message was sent, thank you!")
            return HttpResponseRedirect(request.GET.get("next"))
    vars = {
        "form":form
    }
    return render(request, "contact_us.html")

def subscription(request):
    user = request.user
    return render(request,"subscription.html")

def plan(request):
    get = request.GET
    user = LearnerProfile.objects.get(user_id=request.user.pk)
    key = get.get("key")
    val = int(get.get("val"))
    sen = int(get.get("sense"))

    if key == "lt":
        user.plan[2][1].append([val,sen])
        user.save()
        return HttpResponse("true")

    elif key == "points":
        user.plan[0][2] += val
        user.save()
        return HttpResponse("true")
    
    elif key == "streak":
        date = datetime.datetime.strptime(user.plan[0][1],"%Y-%m-%d").date()
        today = datetime.datetime.today().date()
        if date == today-datetime.timedelta(days=1):
            user.plan[0][0] += 1
            user.plan[0][1] = today.strftime("%Y-%m-%d")
            user.save()
            return HttpResponse("true")
        elif date == today:
            return HttpResponse("none")
        else:
            user.plan[0][0] = 1
            user.plan[0][1] = today.strftime("%Y-%m-%d")
            user.save()
            return HttpResponse("false")
    
    elif key == "learn":
        user.plan[1][0] = val
        user.save()
        return HttpResponse("true")
    
    elif key == "revise":
        user.plan[1][1] = val
        user.save()
        return HttpResponse("true")

def leaderboard(request):
    users = LearnerProfile.objects.order_by("-plan__0__2")

    vars = {
        "users":users
    }
    return render(request,"leaderboard.html",vars)

def notes(request):
    user = request.user
    notes = Notes.objects.filter(user=user)
    notes_dict = [{
        "pk":x.pk,
        "title":x.note_title,
        "note":x.note,
        "created":datetime.date.strftime(x.created,"%m %d, %Y"),
        "color":x.color
    } for x in notes]

    if request.method == "POST":
        post = request.POST
        npk = int(post.get("pk","0"))
        data = json.loads(post.get("note"))
        title = data["title"]
        description = data["description"]
        color = data["color"]

        if post.get("action") == "add":
            Notes.objects.create(user=user,note_title=title,note=description,color=color)

        elif post.get("action") == "update":
            note = Notes.objects.get(pk=npk)
            note.note_title = title
            note.note = description
            note.color = color
            note.save()
            return None
         
        elif post.get("action") == "remove":
            note = Notes.objects.get(pk=npk)
            note.delete()
            return None

    vars = {
        "notes":json.dumps(notes_dict)
    }
    return render(request,"notes.html",vars)