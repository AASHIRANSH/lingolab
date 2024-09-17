from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from languages.models import Dictionary, Post, Quote, GK
# from django.contrib.auth.models import User
import time, json

def index(request):
    quote = Quote.objects.get(qod=True)
    posts = Post.objects.filter(published=True).order_by("-created_at")[0:4]
    gks = GK.objects.filter(published=True).order_by("-created_at")[0:4]
    sl_bgs = ["libr-digital.jpg","libr-digital.webp"]

    now = time.strftime("%a, %d %b %Y %H:%M")
    word = Dictionary.objects.get(is_complete=True) #WordOfTheDay.objects.all().order_by("-created_at")[0]

    vars = {
        "quote":quote,
        "posts":posts,
        "gks":gks,
        "word":word,
        "now":now,
        "bg":sl_bgs
    }
    return render(request,"index.html", vars)

def quotes(request):
    if request.GET.get("author"):
        quotes = Quote.objects.filter(author=request.GET.get("author"))
    else:
        quotes = Quote.objects.all()
    vars = {
        "quotes":quotes
    }
    return render(request,"quotes.html",vars)

def test(request):
    get = request.GET
    with open("database/games/levels.json") as f:
        game_db = json.load(fp=f)
    vars = {
        "game_db":json.dumps(game_db),
        "level":int(get.get("level"))
    }
    return render(request,"_test.html",vars)

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