from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from languages.models import Dictionary, Post, Quote, GK
from django.contrib.auth.models import User
import time

def index(request):
    user = request.user
    quotes = Quote.objects.all()[0]
    posts = Post.objects.filter(published=True).order_by("-created_at")[0:4]
    gks = GK.objects.filter(published=True).order_by("-created_at")[0:4]

    now = time.strftime("%a, %d %b %Y %H:%M")
    word = Dictionary.objects.get(pk=41053) #WordOfTheDay.objects.all().order_by("-created_at")[0]

    vars = {
        "quotes":quotes,
        "posts":posts,
        "gks":gks,
        "word":word,
        "now":now,
    }
    return render(request,"index.html", vars)

def test(request):
    return render(request,"_test.html")
# from django.conf import settings
def vacuum_db(request):
    # print("Vacuuming database...")
    # before = os.stat(settings.default).st_size
    # print("Size before: %s bytes" % before)

    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("VACUUM")
    connection.close()
    
    # after = os.stat(settings.default).st_size
    # print("Size after: %s bytes" % after)
    # print("Reclaimed: %s bytes" % (before - after))
    messages.success(request,"Database was vaccumed successfully!")
    return HttpResponseRedirect('/english/dictionary')