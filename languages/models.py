#User Model
from django.contrib.auth.models import User
from django.db import models
import os

''' this is to rename the image file uploaded by the user Profile Model below as dp '''
def content_file_name(instance, filename):
    ext = filename.split('.')
    filename = "%s_%s.%s" % (instance.title, ext[0], ext[-1])
    return os.path.join('uploads/posts', filename)

''' Posts and Exercises'''
class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

class Thesaurus(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    words = models.CharField(("Words"), max_length=100)

    def __str__(self):
        return self.name

class Collocation(models.Model):
    ref_id = models.BooleanField(default=False)
    word = models.CharField(max_length=50)
    pos = models.CharField(max_length=50)
    usage = models.CharField(("Usage"), max_length=50, blank=True, null=True)
    fields = models.JSONField(default=dict)
    
    def __str__(self):
        return self.word


class Dictionary(models.Model):
    is_complete = models.BooleanField(default=False)
    listing = models.IntegerField(default=0)
    word = models.CharField(max_length=100)
    plural = models.CharField(("Plural Form"), max_length=50, blank=True, null=True)
    pos = models.CharField(("Part of Speech"),max_length=50, blank=True, null=True)
    cefr = models.CharField(max_length=10, blank=True, null=True)
    pronounciation = models.JSONField(("Pronounciation"), default=dict, blank=True, null=True)
    csforms = models.CharField(("CS Forms"), max_length=50, blank=True, null=True)
    forms = models.JSONField(("Forms"), default=dict, blank=True, null=True)
    senses = models.JSONField(("Senses"))
    rvdata = models.JSONField(("Revise Data"), default=dict, blank=True, null=True)
    related_post = models.ManyToManyField("languages.Post", blank=True)
    word_details = models.JSONField(("Word Details"), blank=True, null=True)

    def __str__(self):
        return f'{self.word} {"("+self.pos+")" if self.pos else ""}'
    
    # def cefrs(self):
    #     cefrs = [x[0] if x[0] for x in self.senses]

class TopicDictionary(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cefr = models.CharField(max_length=50, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)    

    def __str__(self):
        return self.name
    
class Fav(models.Model):
    word = models.OneToOneField("languages.Dictionary", verbose_name=("Word"), null=True, on_delete=models.SET_NULL, editable=False)
    rvdata = models.JSONField(("Revise Data"), default=dict)

    def __str__(self):
        return f"{self.word}"


class ZeroToHero(models.Model):
    course = models.CharField(max_length=50)
    lang = models.CharField(choices=(('en','English'),('ru','Russian'),('tr','Turkish')),max_length=50)
    origin = models.CharField(choices=(('en','English'),('ur','Urdu'),('hi','Hindi')),max_length=50)
    data = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.course} ({self.origin})"

'''Posts'''
class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to=content_file_name, blank=True, null=True)
    fill_values = models.CharField(max_length=200, blank=True, null=True)
    views = models.IntegerField(default=0)
    level = models.CharField(choices=(('a1','Beginner'),('a2','Pre Intermediate'),('b1','Intermediate'),('b2','Upper Intermediate'),('c1','Advanced'),('c2','Proficient')), max_length=50, blank=True, null=True)

    # def is_pub(self):
    #     return f"{'published' if self.published else 'unpublished'}"
    
    def __str__(self):
        return f"{self.title} ({'published' if self.published else 'unpublished'})"

class Exercise(models.Model):
    category = models.CharField(max_length=50, choices=(('english','English'),('general_knowledge','GK')), blank=True, null=True)
    sub_category = models.CharField(max_length=50, blank=True, null=True)
    question = models.TextField()
    answer = models.TextField()
    choice = models.CharField(max_length=300, default="", blank=True, null=True)
    target_values = models.CharField(max_length=50, default="", blank=True, null=True)
    type = models.CharField(max_length=50, choices=(('fill','Blanks Filling'),('mcq','Multiple Choice')), blank=True)
    tense = models.CharField(max_length=50, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, blank=True, null=True)
    cefr = models.CharField(("CEFR Level"), max_length=50, choices=(('a1','A1 Beginner'),('a2','A2 Pre Intermediate'),('b1','B1 Intermediate'),('b2','B2 Upper Intermediate'),('c1','C1 Advanced'),('c2','C2 Proficient')), default="", blank=True, null=True)
    pos = models.CharField(choices=(('determiner','determiner'),('adverb','adverb'),('preposition','preposition'),('correct word','correct word'),('correct form','correct form'),('correct phrase','correct phrase'),('usage','usage'),('tag question','tag question'),('helping verb','helping verb')), max_length=50, default="", blank=True, null=True)
    
    def __str__(self):
        return f"{self.question} {self.cefr} ({self.type})"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

''' End Posts... '''
    
class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=100)
    pic = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.quote}"
