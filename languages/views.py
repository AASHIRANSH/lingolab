from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

#WordsDB Model
from .models import Collocation, Dictionary, TopicDictionary, Fav, ZeroToHero
from .models import Post, Exercise, Comment, Like, Dislike
from .forms import PostForm, ExerciseForm, CommentForm, CollocationEntryForm, DictionaryForm

from django.core import serializers
from django.core.paginator import Paginator
import random, datetime, json#, requests
import urllib.request
from django.contrib import messages

''' /home/muhammadsog/learners_academy/ '''
def index(request, id):
    strid = str(id)

    with open("languages/english/data/db.json","rt",encoding='UTF-8') as fdb:
        db = fdb.read()

    vars = {
        "id":id,
        "data":db,
    }
    return render(request, "english/learn.html", vars)

def prayerTimes(request):
    # with open("Muslim/data/cities.db","rt",encoding='UTF-8') as cities:
    #     cities_db = cities.readlines() # listed lines from the deck/db file opened above
    with open("languages/templates/arabic/prayer/data/styles.css","rt",encoding='UTF-8') as styles:
        css = styles.read() # listed lines from the deck/db file opened above
    vars = {
        "styles":css
    }
    return render(request,"arabic/prayer/simple.html",vars)

# def urlToFile(request):
#     with open("languages/templates/english/dictionary/oxtems/temps/p.txt") as sfile:
#         file = sfile.readlines()
    
#     for x in range(len(file)):
#         with open("languages/templates/english/dictionary/oxtems/temps/p/ox"+f"{x+1:03n}",mode="w+",encoding="UTF-8") as tfile:
#             url = file[x][0:-1]
#             print(url)
#             response = requests.get(url)
#             tfile.write(response.content)
             
def oxtems(request):
    import os
    files_dir = "languages/templates/english/dictionary/oxtems/temps/m/"
    files = os.listdir(files_dir)
    get = request.GET

    if get.get("action")=="dup":
        aus = 0
        wos = []
        for f in files:
            with open(files_dir+f, encoding="UTF-8") as temp:
                html = temp.read()
            while True:
                w_s = html.find('htag="h1"')
                w_e = html.find('</h1>',w_s)
                p_s = html.find('class="pos"')
                p_e = html.find('</span>',p_s)
                w = html[w_s+10:w_e]
                p = html[p_s+13:p_e]
                if w+p in wos:
                    os.remove(files_dir+f)
                wos.append(w+p)
                break

    elif get.get("action")=="img":
        aus = 0
        links = []
        for f in files:
            with open(files_dir+f, encoding="UTF-8") as imgf:
                html = imgf.read()
                x = True
                while x:
                    aus = html.find('img class="thumb"',aus+1)
                    img = html.find('src="',aus+17)
                    aue = html.find('"',img+5)
                    if aus == -1:
                        break
                    else:
                        links.append(html[img+5:aue]+"\n")

        with open(f"languages/data/imglinks_{files[0]}_{len(files)}.txt", mode="w", encoding="UTF-8") as temp:
            temp.writelines(links)
        messages.success(request,"Picture links were generated!")
        return HttpResponseRedirect('/english/dictionary')

    elif get.get("action")=="mp3":
        aus = 0
        links = []
        for f in files:
            with open(files_dir+f, encoding="UTF-8") as mp3f:
                html = mp3f.read()

                while True:
                    aus = html.find('mp3="',aus+1)
                    aue = html.find('"',aus+5)
                    if aus == -1:
                        break
                    else:
                        links.append(html[aus+5:aue]+"\n")

        with open(f"languages/data/audlinks_{files[0]}_{len(files)}_mp3.txt", mode="w", encoding="UTF-8") as temp:
            temp.writelines(links)
        messages.success(request,"MP3 Audio Links were generated!")
        return HttpResponseRedirect('/english/dictionary')
    
    elif get.get("action")=="ogg":
        aus = 0
        links = []
        for f in files:
            with open(files_dir+f, encoding="UTF-8") as oggf:
                html = oggf.read()
                while True:
                    aus = html.find('ogg="',aus+1)
                    aue = html.find('"',aus+5)
                    if aus == -1:
                        break
                    else:
                        links.append(html[aus+5:aue]+"\n")

        with open(f"languages/data/audlinks_{files[0]}_{len(files)}_ogg.txt", mode="w", encoding="UTF-8") as temp:
            temp.writelines(links)
        messages.success(request,"OGG Audio Links were generated!")
        return HttpResponseRedirect('/english/dictionary')

    elif get.get("action")=="trim":
        for f in files:#.sort(key=os.path.getctime)
            with open(files_dir+f, mode="r", encoding="UTF-8") as temp:
                html = temp.read()
                html = html[html.find('<div id="entryContent"'):html.find('<div class="responsive_center')].replace(' class="oald"','').replace('entryContent"','entryContent" class="entry-content"')

            with open(files_dir+f, mode="w", encoding="UTF-8") as temp:
                temp.write(html)
        messages.success(request,"Templates were trimmed!")
        return HttpResponseRedirect('/english/dictionary')

    elif get.get("action")=="rename":
        prefix = "ox"
        for n, f in enumerate(files):
            os.rename(files_dir+f,files_dir+prefix+n)

    elif request.method == "POST":
        data = request.POST.get("data")
        data = data.replace("ampp","&")
        # print(data)
        # with requests.get('https://pastebin.com/raw/X8f4Nz6v', stream=True) as r:
        #     r.raise_for_status()
        #     b = bytearray()
        #     for chunk in r.iter_content(4096):
        #         b += chunk
        #     d = json.loads(b.decode())
        data = json.loads(data)

        if data["pronounciation"]:
            data["pronounciation"]["uk"]["texts"] = [" ".join(i.split()) for i in data["pronounciation"]["uk"]["texts"]]
            data["pronounciation"]["us"]["texts"] = [" ".join(i.split()) for i in data["pronounciation"]["us"]["texts"]]

        if data["forms"]:
            for x in range(len(data["forms"])):
                data["forms"][x][0] = " ".join(data["forms"][x][0].split())
                data["forms"][x][1] = " ".join(data["forms"][x][1].split())
                data["forms"][x][2][0] = [" ".join(i.split()) for i in data["forms"][x][2][0]]
                data["forms"][x][3][0] = [" ".join(i.split()) for i in data["forms"][x][3][0]]
        
        if data["word_details"][6]:
            data["word_details"][6] = " ".join(data["word_details"][6].split())
        if data["word_details"][7]:
            data["word_details"][7] = [" ".join(i.split()) for i in data["word_details"][7]]
        
        for x in data["senses"]:
            x[6] = " ".join(x[6].split()) # labels
            x[7] = [" ".join(i.split()) for i in x[7]] # variants
            x[9] = {
                "ar": [[],[]],
                "en": [[" ".join(x[9].split())],[]], #definition
                "hi": [[],[]],
                "ur": [[],[]],
                "tr": [[],[]],
                "gr": [[],[]]
            }
            x[10] = [" ".join(i.split()) for i in x[10]] # examples

        ''' Write to JSON file'''
        # with open("languages/data/oxtems.json", mode="r") as js:
        #     db = json.load(fp=js)
        #     db.append(data)

        # with open("languages/data/oxtems.json", mode="w") as js:
        #     js.write(json.dumps(db, indent=4))

        id_str = data["idioms_startfrom"]
        if data["pos"]!="phrasal verb":
            Dictionary.objects.create(
                word=data["word"],
                plural=data["plural"],
                pos=data["pos"],
                cefr=data["cefr"],
                pronounciation=data["pronounciation"],
                csforms=data["csforms"],
                forms=data["forms"],
                senses=data["senses"][0:id_str-1 if id_str else None],
                word_details=data["word_details"]
            )

        if id_str:
            for i in range(len(data["idcuts"][0])):
                for j in range((data["idcuts"][3][i][-1]+1)-data["idcuts"][3][i][0]):
                    data["senses"][data["idcuts"][3][i][j]][0] = j+1 # [0]  is sensenum
                Dictionary.objects.create(
                    word=data["idcuts"][0][i],
                    pos="phrasal verb" if data["pos"]=="phrasal verb" else "idiom",
                    senses=data["senses"][data["idcuts"][3][i][0]:data["idcuts"][3][i][-1]+1],
                    word_details=[
                        data["word_details"][0], # oxs
                        "",
                        data["idcuts"][1][i],
                        data["idcuts"][2][i],
                        "",
                        "",
                        "",
                        ""
                    ]
                )

        return JsonResponse(data, safe=False)
        ''' Write to JSON file end'''
    else:
        tn = int(get.get("t","1"))
        # page = requests.get('http://localhost:8000/english/')
        # r = urllib.request.urlopen('https://w3schools.com/')
        # page = r.read()

        links = []
        for x in range(tn, len(files)+1):#range(8195,14639): "+f" ({x})"
            link = "english/dictionary/oxtems/temps/m/ox"+f"{x:03n}"
            links.append(link)

        vars = {
            # "page":templ,
            # "p":page.text,
            # "link":"english/dictionary/oxtems/temps/m/ox"+f"{tn}" #str(tn)
            "links":links
        }
        return render(request,"english/dictionary/oxtems/index.html", vars)

def camtems(request):
    if request.GET.get("action")=="aud":
        import os
        aus = 0
        files = os.listdir("languages/templates/english/dictionary/oxtems/temps/")
        for f in files:
            links = []
            with open("languages/templates/english/dictionary/oxtems/temps/"+f, encoding="UTF-8") as temp:
                html = temp.read()

            with open(f"languages/data/audlinks_{files[0]}_{files[-1]}.txt", mode="a+", encoding="UTF-8") as temp:
                x = True
                while x:
                    aus = html.find('mp3="',aus+1)
                    aue = html.find('"',aus+5)
                    if aus == -1:
                        break
                    else:
                        links.append(html[aus+5:aue]+"\n")
                temp.writelines(links)

    if request.GET.get("action")=="trim":
        import os
        for f in os.listdir("languages/templates/english/dictionary/oxtems/temps/"):
            with open("languages/templates/english/dictionary/oxtems/temps/"+f, encoding="UTF-8") as temp:
                html = temp.read()
                html = html[html.find('<div class="di-body"'):html.find('<div class="lmt-10')]

            with open("languages/templates/english/dictionary/oxtems/temps/"+f, mode="w", encoding="UTF-8") as temp:
                temp.write(html)

    if request.method == "POST":
        data = request.POST.get("data")
        data = json.loads(data)

        if data["forms"]:
            for x in range(len(data["forms"])):
                data["forms"][x][0] = " ".join(data["forms"][x][0].split())
                data["forms"][x][1] = " ".join(data["forms"][x][1].split())
                data["forms"][x][2] = [" ".join(i.split()) for i in data["forms"][x][2]]
            
        for x in data["senses"]:
            x["definition"] = " ".join(x["definition"].split())
            x["examples"] = [" ".join(i.split()) for i in x["examples"]]
        
        for x in data["idioms"]:
            x["labels"] = " ".join(x["labels"].split())
            x["definition"] = " ".join(x["definition"].split())
            x["variants"] = " ".join(x["variants"].split())
            x["examples"] = [" ".join(i.split()) for i in x["examples"]]

      
        with open("languages/data/oxtems.json", mode="r") as js:
            db = json.load(fp=js)
            db.append(data)

        with open("languages/data/oxtems.json", mode="w") as js:
            js.write(json.dumps(db,indent=4))
            # json.dump(obj=db, fp=js, indent=4)
        return JsonResponse(data, safe=False)
    else:
        get = request.GET
        tn = get.get("t","1")
        page = requests.get('http://localhost:8000/english/')
        # r = urllib.request.urlopen('https://w3schools.com/')
        # page = r.read()
        vars = {
            # "page":templ,
            "p":page.text,
            "link":"english/dictionary/oxtems/temps_cam/ca"+f"{int(tn):03n}"
        }
        return render(request,"english/dictionary/oxtems/cam_index.html", vars)

'''Tenses'''
def pres_ind(request):

    return render(request,"english/tenses/present_indefinite.html")

''' Posts '''
def exercise_entry(request):
    datag = request.GET
    if datag.get("action") == "editexercise":
        pk = datag.get("pk")
        instance = get_object_or_404(Exercise,pk=pk)
        form = ExerciseForm(instance=instance)
    else:
        form = ExerciseForm()

    
    if request.method == "POST":
        datap = request.POST
        datap = datap.copy()
        datap.update({'author':request.user})
        form = ExerciseForm(datap)

        if form.is_valid():
            form.save()

            if datag.get("action") == "editexercise":
                messages.success(request, "The exercise was edit successfully!")
            else:
                messages.success(request, "The exercise was added successfully!")
            return redirect("posts")
        else:
            messages.error(request, "There was an error!")
            return redirect("exercise_entry")
        
    vars = {
        "form":form
    }
    return render(request, "exercise_entry.html", vars)

def post_entry(request):
    datag = request.GET
    if datag.get("action") == "editpost":
        pk = datag.get("pk")
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
    else:
        form = PostForm()
    
    if request.method == "POST":
        datap = request.POST
        datap = datap.copy()
        datap.update({
            'author':request.user,
            'published':post.published,
        })
        form = PostForm(datap, instance=post)

        if form.is_valid():
            form.save()

            if datag.get("action") == "editpost":
                messages.success(request, "The post was updated successfully!")
                return HttpResponseRedirect(f"/english/post/{post.pk}")
            else:
                messages.success(request, "The post was added successfully!")
                return redirect("post")
        else:
            messages.error(request, "There was an error!")
            return redirect("post_entry")
    vars = {
        "form":form,
        "edit":True
    }
    return render(request, "post_entry.html", vars)

def post_list(request):
    datag = request.GET
    if datag.get("action") == "myposts":
        posts = Post.objects.filter(author=request.user)
    else:
        posts = Post.objects.filter(published=True)
        
    paginator = Paginator(posts, 5)  # Show 6 contacts per page.
    page_number = datag.get("page")
    page_obj = paginator.get_page(page_number)


    vars = {
        "posts": posts,
        "page_obj": page_obj
    }
    return render(request, 'english/post_list.html', vars)

def post_detail(request, pk):
    # user_obj = User.objects.get(username=request.user.username)
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    comments = post.comments.all()
    user_in_like_set = post.like_set.filter(user__username=request.user.username).exists()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    vars = {
        # 'user_obj':user_obj,
        'post': post,
        'comments': comments,
        'form': form,
        'user_in_like_set': user_in_like_set,
        "premium":True
        }
    return render(request, 'post_detail.html', vars)

def exercise(request, pk):
    # user_obj = User.objects.get(username=request.user.username)
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    user_in_like_set = post.like_set.filter(user__username=request.user.username).exists()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    vars = {
        # 'user_obj':user_obj,
        'post': post,
        'comments': comments,
        'form': form,
        'user_in_like_set': user_in_like_set
        }
    return render(request, 'exercise.html', vars)

def post_detail_test(request):

    return render(request, 'post_detail_test.html')

'''Like and Dislike'''
@login_required
def like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(post=post, user=request.user).first()
    if like:
        like.delete()
    else:
        Like.objects.create(post=post, user=request.user)
        Dislike.objects.filter(post=post, user=request.user).delete()
    return redirect('post_detail', pk=pk)

@login_required
def dislike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    dislike = Dislike.objects.filter(post=post, user=request.user).first()
    if dislike:
        dislike.delete()
    else:
        Dislike.objects.create(post=post, user=request.user)
        Like.objects.filter(post=post, user=request.user).delete()
    return redirect('post_detail', pk=pk)

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.author:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('post_detail', pk=comment.post.pk)
        else:
            form = CommentForm(instance=comment)
        return render(request, 'edit_comment.html', {'form': form})
    else:
        return redirect('post_detail', pk=comment.post.pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_superuser or request.user == comment.author:
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)
    else:
        return redirect('post_detail', pk=comment.post.pk)

from os.path import exists


''' Creates a file with all dictiory headwords '''
def dictionary_json(request):
    get = request.GET

    if get.get("action")=="heads":
        words = Dictionary.objects.all().order_by('word')
        headwords = []
        for x in words:
            headwords.append(x.word)#headwords.append([x.pk,x.word,x.pos])
        
        with open("database/models/suggs_trm.json", mode="w") as jsondict:
            json.dump(headwords, fp=jsondict)

        # with open("database/models/pos.json", mode="w") as jsondict:
        #     json.dump(pos, fp=jsondict)
    
    elif get.get("action")=="topic":
        words = Dictionary.objects.all().order_by('word')
        for word in words:
            senses = word.senses
            for sense in senses:
                if sense.topic:
                    Topic.objects.create(name=sense.topic,cefr=sense.topic_cefr,word=word,sense=sense.sensenum)

    elif get.get("action")=="model":
        words = Word.objects.all().order_by('word')
        adv_model = serializers.serialize("json",words)
        adv_model = json.loads(adv_model)
        with open("languages/data/models/words.json", mode="w", encoding="UTF-8") as file:
            json.dump(obj=adv_model,fp=file, indent=4)
        return HttpResponse("The model was converted to JSON successfully")

    # return JsonResponse(adv_model, safe=False)
    return None

def dictionary_collocation(request):
    # file_path = f"languages/english/flashcards/data/users/{request.user.username}.txt"
    vars_get = request.GET
    search_query = vars_get.get("q","").strip()
    search_pos = vars_get.get("pos","").strip()
    search_in = vars_get.get("in","").strip()

    if search_query:
        words = Collocation.objects.filter(word__contains=f"{search_query}") | Collocation.objects.filter(pos=search_pos, definition__contains=f"{search_in}")
    else:
        words = Collocation.objects.all()
    
    paginator = Paginator(words, 10)  # Show 6 contacts per page.
    page_number = vars_get.get("page") if vars_get.get("page") else 1
    page_navi = int(page_number)-1
    page_obj = paginator.get_page(page_number)

    vars = {
        "wordscount":words.count(),
        "wordsp":page_obj,
        "pagen":page_navi,
    }
    return render(request, "english/dictionary_collocation.html", vars)

def collocation_entry(request):

    if request.method == "POST":
        datap = request.POST
        data = datap.copy()

        fields = []
        field = {}
        for x,y in data.items():
            if x.startswith("entry_pos"):
                field.update({
                    "entry_pos":y
                })
            if x.startswith("context"):
                field.update({
                    "context":y
                })
            if x.startswith("examples"):
                field.update({
                    "examples":y
                })
            if len(field) == 3:
                fields.append(field)
                field = {}

        data.update({
            "fields":fields
        })

        get_word = data.get('word')
        get_pos = data.get('pos')
        get_usage = data.get('usage')

        form = CollocationEntryForm(data)

        if form.is_valid():
            # form.save()
            messages.success(request, f'the entry of "{get_word}" was added')
            # messages.success(request, dict(data))
            messages.success(request, fields)
            
            vars = {
                "form":form,
                "word":get_word,
                "pos":get_pos,
                "usage":get_usage,
                "edit":False
            }
            
            return render(request, "english/collocation_entry.html", vars)
            # return HttpResponseRedirect('/english/flashcards/addcard')
        else:
            messages.error(request, form)

    else:
        form = CollocationEntryForm()

    vars = {
        "form":form,
        "edit":False
    }
    return render(request,"english/collocation_entry.html", vars)

def collocation_edit(request):
    data = request.GET
    word_id = data.get('word_id')
    word_obj = Collocation.objects.get(id=word_id)
    fields = word_obj.fields

    form = CollocationEntryForm(instance=word_obj)

    if request.method == "POST":
        datap = request.POST
        data = datap.copy()

        fields = []
        field = {}

        for x, y in data.items():
            
            if x.startswith("entry_pos"):
                field.update({
                    "entry_pos":y
                })
            if x.startswith("context"):
                field.update({
                    "context":y
                })
            if x.startswith("examples"):
                field.update({
                    "examples":y
                })
            if len(field) == 3:
                fields.append(field)
                field = {}

        data.update({
            "fields":fields
        })

        data_form = CollocationEntryForm(data or None, instance=word_obj)
        if data_form.is_valid():
            data_form.save()
            messages.success(request, "Great! the entry was edited!")
            return redirect("/english/collocation/"+word_id)
        else:
            messages.error(request, form.errors)

    vars = {
        "form":form,
        "fields":fields,
        "edit":True
    }
    return render(request, "english/collocation_entry.html", vars)

def collocation_view(request, id):
    word = Collocation.objects.get(id=id)
    word_entry = Word.objects.get(ref_id=word.word+"_"+("1" if word.pos == "verb" else "2" if word.pos == "noun" else "3" if word.pos == "adjective" else "4"))
    fields = word.fields
    vars = {
        "word":word,
        "pronounce":word_entry.pronounce.splitlines if word_entry else "",
        "fields":fields
    }
    return render(request,"english/collocation.html",vars)

def ipa_convert(request):
    data = request.GET.get("data")
    if data:
        data = data.split(" ")
        dobj = []
        for x in data:
            xobj = Dictionary.objects.filter(word=x).first()
            print(xobj)
            dobj.append(xobj.pronounciation["uk"]["texts"])
        return JsonResponse(dobj,safe=False)
    return render(request,"english/ipa_converter.html")

@login_required
def exercise(request):
    get = request.GET
    user = request.user
    username = user.username
    cefr = ["a1","a2","b1","b2","c1","c2"]

    today = datetime.datetime.today().date() # today.strftime("%Y-%m-%d") # string date

    # rv_set = Exercise.objects.all()
    lv_set = sorted(Exercise.objects.all(), key=lambda x: random.random())
    
    # learn = user.learnerprofile.plan[1]
    # revise = user.learnerprofile.plan[2]
    # learned = int(request.COOKIES.get("wlt","0"))

    rvp_obj = []
    # if rv_set.exists():
    #     for x in rv_set:
    #         rvdata = x.rvdata[username]
    #         for dn, d in enumerate(rvdata["dates"]):
    #             if not rvdata["mastered"][dn]:
    #                 yd = datetime.datetime.strptime(d,"%Y-%m-%d").date()
    #                 if today >= yd:
    #                     rvp_obj.append({
    #                         "pk":x.pk,
    #                         "rvsense":rvdata["senses"][dn],
    #                         "from":"Learned",
    #                         "question":x.question,
    #                         "answer":x.answer,
    #                         "choices":x.choice,
    #                         "cefr":x.cefr,
    #                         "senses":x.word.senses[rvdata["senses"][dn]],
    #                         "priority":rvdata["pr"][dn],
    #                         "actionable": False if (today==yd and rvdata["rvcounts"][dn] < 3) else True
    #                     })
    #                 if len(rvp_obj) == revise:
    #                     break
    #         if len(rvp_obj) == revise:
    #             break
    
    lv_counter = 0
    if lv_set:    
        for x in lv_set:
            rvp_obj.append({
                "pk":x.pk,
                "from":"New",
                "question":x.question,
                "answer":x.answer,
                "cefr":x.cefr,
                "choices":x.choice.split(","),
                "priority":3,
                "actionable":True
            })
            lv_counter += 1
            if lv_counter >= 10:#learn-learned
                break

    vars = {
        "objs":json.dumps(rvp_obj),
        "rv_total_count":len(lv_set),
        "rv_count":len(rvp_obj),
        "learn":10,
        "revise":15
    }
    return render(request, "english/exercise.html", vars)


@login_required
def note_edit(request,id):
    if request.method == "POST":
        note = request.POST.get("note")
        word = Revise.objects.get(word_id=id)
        
        word.note = note
        word.save()

        messages.success(request, "The note was edited")
        return HttpResponseRedirect("/english/revise")
    else:
        pass
    return HttpResponseRedirect("/english/revise")


def ex_action(request):
    if request.POST:
        datap = request.POST
        questions = json.loads(datap.get("questions"))
        errors = json.loads(datap.get("errors"))
        
        user_obj = User.objects.get(username=request.user.username)
        user_q = user_obj.profile.ex_done
        
        for q in questions:
            if q in user_q:
                pass
            else:
                user_obj.profile.ex_done += q+","
                user_obj.profile.reputation += 1
                user_obj.save()
    return JsonResponse(["successful"], safe=False)


''' Dictionary Entry '''
@login_required
def word_entry(request):
    get = request.GET
    sensen = int(get.get("sense","0"))
    edit = True if get.get("edit")=="true" else False
    add = True if get.get("add")=="true" else False
    if edit or add:
        word_obj = Dictionary.objects.get(pk=get.get("word"))
        sense = word_obj.senses[sensen]
    
    if request.method == "POST":
        post = request.POST
        data = post.copy()

        sense_count = int(data.get('sense_count'))
        word = data.get('word')
        pos = data.get('pos')
        cefr = data.get('cefr')
        ukphones = data.get('ukphones')
        usphones = data.get('usphones')
        plural = data.get('plural')
        csforms = data.get('cforms')
        other_forms = data.get('other_forms')
        word_details = data.get('word_details')
        listing = data.get('listing')
        related_post = data.get('related_post')

        fields = {
            "is_complete": data.get('complete'),
            "listing": data.get('listing'),
            "word": word,
            "pos": pos,
            "cefr": cefr,
            "pronounciation":{"uk":eval(ukphones) if ukphones else {},"us":eval(usphones) if usphones else {}} if ukphones else None,
            "plural": plural,
            "csforms": csforms,
            "other_forms": other_forms,
            "word_details": eval(word_details) if word_details else None
        }

        senses = []
        for s in range(sense_count):
            sense = []
            s = str(s)
            sense.append(sensen+1) #sensenum
            sense.append(data.get('def_head_'+s))
            sense.append(data.get('scefr_'+s))
            sense.append(eval(data.get('img_'+s)))
            sense.append(data.get('dtxt_'+s))
            sense.append(data.get('context_'+s))
            sense.append(data.get('labels_'+s))
            sense.append(data.get('variants_'+s).splitlines())
            sense.append(data.get('def_inf_'+s)) # grammar
            sense.append({
                "ar": ["",""],
                "en": [data.get('endef_'+s).splitlines(),data.get('enbdef_'+s).split(","),data.get('enexdef_'+s).splitlines()],
                "hi": [data.get('hidef_'+s).splitlines(),data.get('hibdef_'+s).split(",")],
                "ur": [data.get('urdef_'+s).splitlines(),data.get('urbdef_'+s).split(",")],
                "tr": ["",""],
                "gr": ["",""]
            })
            sense.append(data.get('examples_'+s).splitlines())
            sense.append([x.split("$") for x in data.get('usages_'+s).splitlines()])
            sense.append(data.get('synonyms_'+s).splitlines())
            sense.append(data.get('antonyms_'+s).splitlines())
            sense.append(data.get('compares_'+s).splitlines())
            sense.append(data.get('see_also_'+s).splitlines())
            sense.append(eval(data.get('topic_'+s)) if data.get('topic_'+s) else [[],[]])
            sense.append(data.get('use_'+s))
            sense.append(data.get('help_'+s))
            sense.append(eval(data.get('unbox_'+s)) if data.get('unbox_'+s) else [])
            senses.append(sense)

        fields.update({"senses":senses})
        form = DictionaryForm(fields)
        if form.is_valid():
            if add:
                senses[0][0] = len(word_obj.senses)
                word_obj.senses.append(senses[0])
                word_obj.save()
                messages.success(request, f'{word}" was updated')
                return HttpResponseRedirect(f'/english/word/{word_obj.pk}')
            elif edit:
                word_obj.is_complete = True if data.get('complete') == "on" else False
                word_obj.listing = listing
                word_obj.word = word
                word_obj.pos = pos
                word_obj.cefr = cefr
                word_obj.plural = plural
                word_obj.senses[sensen] = senses[0]
                word_obj.word_details = eval(word_details)
                if listing != 0:
                    if len(word_obj.word_details[0])==2:
                        word_obj.word_details[0].append(["","","",""])
                        match listing:
                            case "1":
                                word_obj.word_details[0][2][0] = [sensen]
                            case "2":
                                word_obj.word_details[0][2][1] = [sensen]
                            case "3":
                                word_obj.word_details[0][2][2] = [sensen]
                            case "4":
                                word_obj.word_details[0][2][3] = [sensen]
                            case "5":
                                word_obj.word_details[0][2][4] = [sensen]
                word_obj.related_post.add(related_post)
                word_obj.save()
                messages.success(request, f'sense "{sensen+1}" of "{word}" was updated')
                return HttpResponseRedirect(f'/english/word/{word_obj.pk}')
            else:
                form.save()
                messages.success(request, f'the word "{word}" was added')
            vars = {
                "form":form,
                "word":word_obj if edit else None,
                "sense":sense if edit else None
            }
            return render(request, "english/word_main_add.html", vars)
        else:
            messages.error(request,form.errors)
            vars = {
                "form":form,
                "sense":sense if edit else None
            }
            return render(request, "english/word_main_add.html", vars)
    else:
        if edit:
            form = DictionaryForm(instance=word_obj)
        else:
            form = DictionaryForm()
    vars = {
        "form":form,
        "word":word_obj if edit else None,
        "sense":sense if edit else None,
    }
    return render(request, "english/word_main_add.html", vars)

@login_required
def my_words(request):
    get = request.GET
    search_query = get.get("q","").strip()

    if search_query:
        words = Fav.objects.filter(rvdata__has_key=request.user.username, word__contains=search_query)
    else:
        words = Fav.objects.filter(rvdata__has_key=request.user.username)
    
    wordd = []
    for x in words:
        rvdata = x.rvdata[request.user.username]
        for y in range(len(rvdata["senses"])):
            rvs = rvdata["rvcounts"][y]
            wordd.append({
                "word":x.word,
                #"pos":x.pos,
                "pk":x.pk,
                "sense":rvdata["senses"][y],
                "progress":rvs*10 if rvs < 11 else 100
            })
    paginator = Paginator(wordd, 10)  # Show 6 contacts per page.
    page_number = get.get("page") if get.get("page") else 1
    page_navi = int(page_number)-1
    page_obj = paginator.get_page(page_number)

    vars = {
        "wordscount":words.count(),
        "wordsp":page_obj,
        "pagen":page_navi,
    }
    return render(request, "english/my_words.html", vars)

@login_required
def my_word(request,word):
    word = Dictionary.objects.get(pk=word)
    
    fav_obj = Fav.objects.get(pk=word.pk)
    fav = [x+1 for x in fav_obj.rvdata[request.user.username]["senses"]] if request.user.username in fav_obj.rvdata.keys() else None
        
    vars = {
        "word":word,
        "fav":fav
    }
    return render(request, "english/my_word.html", vars)

''' Dictionary '''
def dictionary(request):
    from django.db.models import Q
    get = request.GET

    url = "https://microsoft-translator-text.p.rapidapi.com/translate"
    querystring = {"to":"ur","api-version":"3.0","profanityAction":"NoAction","textType":"plain"}
    
    if get.get("action")=="trm":
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "9ea8b16349msh45b993004bb2674p10f7f1jsnc7a403c6b963",
            "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
        }

        for x in range(590,1001):
            word = Dictionary.objects.get(pk=x)
            if word.senses:
                for s in word.senses:
                    hipayload = [{"Text":s[9]["en"][0][0]}]
                    response = requests.post(url, json=hipayload, headers=headers, params=querystring)
                    s[9]["ur"][0] = [response.json()[0]["translations"][0]["text"]]
                    # s[9]["ur"][0] = [response.json()[0]["translations"][1]["text"]]
                print(x)
                word.save()
    
    search_query = get.get("q","").strip()
    filt = get.get("filter","")

    if filt:
        words = Dictionary.objects.filter(Q(word__startswith=search_query,cefr=filt) | Q(word__contains=search_query,cefr=filt))
    elif search_query:
        words = Dictionary.objects.filter(Q(word__startswith=search_query))
        if not words.exists():
            words = Dictionary.objects.filter(Q(word__contains=search_query[1:-1]) | Q(word__contains=search_query[2:-2]))
            messages.warning(request,"There were no exact match to your query, hence showing similar results")
    else:
        words = Dictionary.objects.all()

    paginator = Paginator(words, 10)  # 10 contacts per page.
    page_number = get.get("page") if get.get("page") else 1
    page_navi = int(page_number)-1
    page_obj = paginator.get_page(page_number)

    vars = {
        "wordscount":words.count(),
        "wordsp":page_obj,
        "pagen":page_navi,
        "usr":"usr"+str(request.user.pk)
        # "fav":fav
    }
    return render(request, "english/dictionary_2.html", vars)

def dictionaryTopic(request):
    topics = TopicDictionary.objects.all()
    vars = {
        "topics":topics
    }
    return render(request,"english/dictionary_topic.html",vars)

def dictionaryTopicView(request,name):
    tp = TopicDictionary.objects.get(name=name)
    words = []
    for x in tp.data:
        word = Dictionary.objects.get(pk=x[0])
        words.append([word,x[1]-1,word.senses[x[1]-1][9]["en"][0][0]])
    vars = {
        "words":words
    }
    return render(request,"english/dictionary_topic_view.html",vars)

''' Word Page'''
from django.views.decorators.clickjacking import xframe_options_exempt
def word_main(request,word):
    word = Dictionary.objects.get(pk=word)
    nw = [Dictionary.objects.get(pk=x) for x in range(word.pk-3 if word.pk > 3 else 1, word.pk+4 if word.pk<80171 else 80175)]
    
    fav_obj = Fav.objects.get(pk=word.pk)
    fav = [x+1 for x in fav_obj.rvdata[request.user.username]["senses"]] if request.user.username in fav_obj.rvdata.keys() else None
    
    # collocation = Collocation.objects.filter(word=word.word, pos=word.pos).first()
    
    vars = {
        "word":word,
        "nw":nw,
        "fav":fav
        # "collocation":collocation,
    }
    return render(request, "english/word_main.html", vars)

@xframe_options_exempt
def word_main_single(request,word,sense):
    word = Dictionary.objects.get(pk=word)
    wsense = word.senses[sense] if word.senses else None
    nw = [Dictionary.objects.get(pk=x) for x in range(word.pk-3 if word.pk > 3 else 1, word.pk+4 if word.pk<80171 else 80175)]
    
    fav_obj = Fav.objects.get(pk=word.pk)
    if request.user.username in fav_obj.rvdata.keys():
        rvdata = fav_obj.rvdata[request.user.username]
        fav = [x+1 for x in rvdata["senses"]]
        note = rvdata["notes"][rvdata["senses"].index(sense)]
    else:
        fav = None
        note = None


    vars = {
        "word":word,
        "sense":wsense,
        "nw":nw,
        "fav":fav,
        "note":note
    }
    return render(request, "english/word_main_single.html", vars)


def dict_filt(request):
    get = request.GET
    data = get.get("data","")

    if data == "common_phrasal_verbs":
        words = Dictionary.objects.filter(listing=1)
    elif data == "conversational_phrases":
        words = Dictionary.objects.filter(listing=2)
    elif data == "common_idioms":
        words = Dictionary.objects.filter(listing=3)
    elif data == "sayings":
        words = Dictionary.objects.filter(listing=4)

    paginator = Paginator(words, 50)
    page_number = get.get("page") if get.get("page") else 1
    page_navi = int(page_number)-1
    page_obj = paginator.get_page(page_number)

    vars = {
        "wordscount":words.count(),
        "wordsp":page_obj,
        "pagen":page_navi,
        "usr":"usr"+str(request.user.pk)
    }
    return render(request,"english/dictionary_filtered.html",vars)

'''Revise'''
@login_required
def revise_main(request):
    get = request.GET
    user = request.user
    username = user.username
    cefr = ["a1","a2","b1","b2","c1","c2"]

    today = datetime.datetime.today().date() # today.strftime("%Y-%m-%d") # string date

    rv_set = Fav.objects.filter(rvdata__has_key=username)
    lv_set = sorted(Dictionary.objects.filter(cefr="b1") | Dictionary.objects.filter(cefr="b2") | Dictionary.objects.filter(cefr="c1"), key=lambda x: random.random())
    lv_set = lv_set if lv_set else sorted(Dictionary.objects.filter(cefr="a2"), key=lambda x: random.random())
    
    learn = user.learnerprofile.plan[1]
    revise = user.learnerprofile.plan[2]
    learned = int(request.COOKIES.get("wlt","0"))

    rvp_obj = []
    if rv_set:
        for x in rv_set:
            rvdata = x.rvdata[username]
            for dn, d in enumerate(rvdata["dates"]):
                if not rvdata["mastered"][dn]:
                    yd = datetime.datetime.strptime(d,"%Y-%m-%d").date()
                    if today >= yd:
                        # print(x.word, x.pk)
                        rvp_obj.append({
                            "pk":x.pk,
                            "rvsense":rvdata["senses"][dn],
                            "rvcount":rvdata["rvcounts"][dn],
                            "from":"Learned",
                            "word":x.word.word,
                            "pos":x.word.pos,
                            "cefr":x.word.cefr,
                            "forms":x.word.forms,
                            "pronunciation":x.word.pronounciation,
                            "senses":x.word.senses[rvdata["senses"][dn]],
                            "word_details":x.word.word_details,
                            "note":rvdata["notes"][dn],
                            "priority":rvdata["pr"][dn],
                            "actionable": False if (today==yd and rvdata["rvcounts"][dn] < 2) else True
                        })
                    if len(rvp_obj) == revise:
                        break
            if len(rvp_obj) == revise:
                break
    
    lv_counter = 0
    if lv_set:    
        for x in lv_set:
            if x.senses:
                if lv_counter >= learn-learned:
                    break
                while True:
                    rsense = random.randrange(len(x.senses))
                    if x.senses[rsense][2] in cefr:
                        break
                if username in x.rvdata.keys():
                    rvd = x.rvdata[username]["senses"]
                    if rsense not in rvd:
                        rvp_obj.append({
                            "pk":x.pk,
                            "rvsense":rsense,
                            "from":"New Word",
                            "word":x.word,
                            "pos":x.pos,
                            "cefr":x.cefr,
                            "forms":x.forms,
                            "pronunciation":x.pronounciation,
                            "senses":x.senses[rsense],
                            "word_details":x.word_details,
                            "priority":3,
                            "actionable":True
                        })
                        lv_counter += 1
                else:
                    rvp_obj.append({
                        "pk":x.pk,
                        "rvsense":rsense,
                        "from":"New Word",
                        "word":x.word,
                        "pos":x.pos,
                        "cefr":x.cefr,
                        "forms":x.forms,
                        "pronunciation":x.pronounciation,
                        "senses":x.senses[rsense],
                        "word_details":x.word_details,
                        "priority":3,
                        "actionable":True
                    })
                    lv_counter += 1

    # randnums = random.sample(items, 3) #for more than one item, it contains 3 random objects from the model
    vars = {
        "objs":json.dumps(rvp_obj),
        "rv_total_count":len(rv_set),
        "rv_count":len(rvp_obj),
        "learn":learn,
        "revise":revise
    }
    return render(request, "english/revise_final.html", vars)

'''Revise Actions'''
def data_main(request):
    user = request.user
    username = user.username #str(user.pk)
    data = request.GET
    word = data.get('word')
    sense = int(data.get('sense'))
    word_obj = get_object_or_404(Dictionary, pk=word)
    fav_obj = get_object_or_404(Fav, pk=word)

    today = datetime.date.today()
    todaystr = today.strftime("%Y-%m-%d")

    if username in fav_obj.rvdata.keys():
        rvdata = fav_obj.rvdata[username]
        rvdate = today+datetime.timedelta(days=2);rvdate=rvdate.strftime("%Y-%m-%d")
    else:
        rvdate = todaystr
        if data.get('data')=="fav":
            usrdata = {
                username:{
                    "pr":[],
                    "mastered":[],
                    "rvcounts":[],
                    "senses":[],
                    "dates":[],
                    "notes":[]
                }
            }
        else:
            usrdata = {
                username:{
                    "pr":[3],
                    "mastered":[False],
                    "rvcounts":[0],
                    "senses":[sense],
                    "dates":[todaystr],
                    "notes":[""]
                }
            }
        fav_obj.rvdata.update(usrdata)
        rvdata = fav_obj.rvdata[username]
    
    if data.get('data') == "easy":
        if sense in rvdata["senses"]:
            seni = rvdata["senses"].index(sense)
            pr = rvdata["pr"][seni]
            rvcount = rvdata["rvcounts"][seni]
            td = datetime.timedelta(days=rvcount) if pr == 4 else datetime.timedelta(days=rvcount+pr) if pr == 6 else datetime.timedelta(days=rvcount+3)
            rvdata["dates"][seni] = (today+td).strftime("%Y-%m-%d")
            rvdata["rvcounts"][seni] += 1
            fav_obj.save()
            return HttpResponse("Done")
    
    elif data.get('data') == "hard":
        if sense in rvdata["senses"]:
            seni = rvdata["senses"].index(sense)
            rvcount = rvdata["rvcounts"][seni]
            rvdata["dates"][seni] = todaystr
            rvdata["rvcounts"][seni] -= 1 if rvcount >= 1 else 0
            fav_obj.save()
            return HttpResponse("Done")
    
    elif data.get('data') == "remove":
        seni = rvdata["senses"].index(sense-1)
        rvdata["pr"].pop(seni)
        rvdata["mastered"].pop(seni)
        rvdata["rvcounts"].pop(seni)
        rvdata["senses"].pop(seni)
        rvdata["dates"].pop(seni)
        rvdata["notes"].pop(seni)
        fav_obj.save()
        messages.warning(request, f'Sense {sense} of "{word_obj}" was removed from your Favorites!')
        return HttpResponseRedirect('/english/word/'+word)
    
    elif data.get('data') == "fav":
        if sense == 0:
            for x in range(len(word_obj.senses)):
                if x in rvdata["senses"]:
                    continue
                else:
                    rvdata["pr"].append(3)
                    rvdata["mastered"].append(False)
                    rvdata["rvcounts"].append(0)
                    rvdata["senses"].append(x)
                    rvdata["dates"].append(todaystr)
                    rvdata["notes"].append("")
            fav_obj.save() #rv.save()
            messages.success(request, f"All {len(word_obj.senses)} senses of '{word_obj.word}' were added!")
            return HttpResponseRedirect('/english/word/'+word)
        else:
            if sense-1 in rvdata["senses"]:
                messages.warning(request, "Oops! this sense of the word already exists!")
                return HttpResponseRedirect('/english/word/'+word)
            else:
                rvdata["pr"].append(3)
                rvdata["mastered"].append(False)
                rvdata["rvcounts"].append(0)
                rvdata["senses"].append(sense-1)
                rvdata["dates"].append(todaystr if not rvdate else rvdate)
                rvdata["notes"].append("")
                fav_obj.save()
                messages.success(request, f"Sense '{sense}' of '{word_obj.word}' was added!")
                return HttpResponseRedirect('/english/word/'+word)

    elif data.get('data') == "mastered":
        rvi = rvdata["senses"].index(sense)
        rvs = rvdata["mastered"][rvi]
        rvdata["mastered"][rvi] = True if rvs == False else True
        fav_obj.save()
        return HttpResponse("Done")

    elif data.get('data') == "pr1":
        if sense in rvdata["senses"]:
            seni = rvdata["senses"].index(sense)
            rvdata["pr"][seni] = 3
            fav_obj.save()
            return HttpResponse("Done")
        
    elif data.get('data') == "pr3":
        if sense in rvdata["senses"]:
            seni = rvdata["senses"].index(sense)
            rvdata["pr"][seni] = 4
            fav_obj.save()
            return HttpResponse("Done")

    elif data.get('data') == "pr6":
        if sense in rvdata["senses"]:
            seni = rvdata["senses"].index(sense)
            rvdata["pr"][seni] = 6
            fav_obj.save()
            return HttpResponse("Done")

''' Zero to Hero '''
def zero_to_hero_home(request):
    current_course = request.user.profile.learnings["courses"]["current"]
    is_current = True if current_course[0] else False

    if current_course[0]:
        objs = ZeroToHero.objects.get(pk=current_course[0])
    else:
        objs = ZeroToHero.objects.all()

    vars = {
        "course_selected":is_current,
        "course":objs,
        "courses":ZeroToHero.objects.all(),
        "lang":objs.course if is_current else False,
        "ul":current_course
    }
    return render(request,"learn_home.html", vars)

def zero_to_hero_start(request,course):
    profile = request.user.profile
    courses = profile.learnings["courses"]
    obj = ZeroToHero.objects.get(pk=course)
    courses["current"][0] = obj.pk
    if course not in courses["enrolled"]:
        courses["enrolled"].append(obj.pk)
    profile.save()

    vars = {
        "course":obj
    }
    return render(request,"learn_start.html",vars)

def zero_to_hero(request,lang,unit,lesson):
    obj = ZeroToHero.objects.get(pk=lang)
    code = obj.origin
    # with open("languages/"+lang+"/data/en.json","rt",encoding='UTF-8') as endb:
    #     endb = json.load(fp=endb)
    with open("languages/data/"+obj.course+"/db.json","rt",encoding='UTF-8') as tp:
        tp = json.load(fp=tp)

    lesson_db = []
    for x in obj.data[unit-1]["lessons"][lesson-1]: #endb["unit_"+unit]:
        et = x[0]   
        if et=="word":
            it = Dictionary.objects.get(pk=x[3])
            topic = it.senses[x[4]][16][0][0] if it.senses[x[4]][16][0] else None

            x[2] = [[it.word,it.senses[x[4]][9][code][1]],tp[topic] if topic else ""]
            lesson_db.append(x)

        elif et=="translate":
            lesson_db.append(x)

    vars = {
        "unit":unit,
        "db":json.dumps(lesson_db)
    }
    return render(request, "english/learn_main.html", vars)

def zth_entry(request):
    get = request.GET
    edit = True if get.get("edit")=="true" else False
    add = True if get.get("add")=="true" else False
    
    if edit or add:
        word_obj = ZeroToHero.objects.get(pk=get.get("course"))
        lsn = int(get.get("lesson"))
        unit = int(get.get("unit"))-1
        lesson = word_obj.data[unit]["lessons"][lsn]

    if request.method == "POST":
        post = request.POST
        data = post.copy()

        sense_count = int(data.get('page_count'))
        senses = []
        for s in range(sense_count):
            sen = []
            s = str(s)
            sen.append(data.get('type_'+s))
            sen.append(data.get('interface_'+s))
            sen.append(data.get('content_'+s))
            sen.append(data.get('word_'+s))
            sen.append(data.get('sense_'+s))
            sen.append(data.get('level_'+s))
            
            senses.append(sen)

        if edit:
            word_obj.data[unit]["unit_title"] = data.get("unit_title")
            word_obj.data[unit]["lessons"][lsn] = senses
            word_obj.save()
            messages.success(request, f'Unit {word_obj.pk} was updated')
            return HttpResponseRedirect(f'/english/zth/')
        # elif add:
        else:
            # form.save()
            ZeroToHero.objects.create(course="unit_title",data="senses")
            messages.success(request, f'the entry was added')
            vars = {
                # "form":form,
                "word":word_obj if edit else None,
                "sense":lesson if edit else None
            }
            return render(request, "english/zth_add.html", vars)
    vars = {
        # "form":form,
        "title":word_obj.data[unit]["title"],
        "word":word_obj if edit else None,
        "wsense":lesson if edit else None,
        "edit":edit
    }
    return render(request, "english/zth_add.html", vars)

def zth_view(request):
    get = request.GET
    # filt = get.get("lang","en")
    words = ZeroToHero.objects.all() #filter(data__has_key=filt)

    paginator = Paginator(words, 10)
    page_number = get.get("page") if get.get("page") else 1
    page_navi = int(page_number)-1
    page_obj = paginator.get_page(page_number)

    vars = {
        "wordscount":words.count(),
        "wordsp":page_obj,
        "pagen":page_navi,
        "usr":"usr"+str(request.user.pk)
        # "fav":fav
    }
    return render(request, "english/zth_view.html", vars)