from django.contrib import admin
from .models import Post, Comment, Like, Dislike, Exercise, Story
from .models import Quote, Thesaurus, Collocation, Dictionary, TopicDictionary, Topic, Fav, ZeroToHero, GK

# Register your models here.
@admin.register(Story)
class StoryView(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Exercise)
class ExerciseView(admin.ModelAdmin):
    list_display = ['question','category','sub_category','cefr']


@admin.register(Dictionary)
class DictionaryView(admin.ModelAdmin):
    list_display = ['word','pos','pk']


@admin.register(TopicDictionary)
class TDictionaryView(admin.ModelAdmin):
    list_display = ['name','cefr']


@admin.register(Fav)
class FavView(admin.ModelAdmin):
    list_display = ['word','pk']


@admin.register(ZeroToHero)
class ZeroToHeroView(admin.ModelAdmin):
    pass
    # list_display = ['word','pk']


@admin.register(Collocation)
class CollocationView(admin.ModelAdmin):
    list_display = ['word','pos']


@admin.register(Thesaurus)
class ThesaurusView(admin.ModelAdmin):
    list_display = ['name']

    class Media:
        js= ('/static/js/tinyinject.js',)


@admin.register(Post)
class PostView(admin.ModelAdmin):
    list_display = ('title','created_at','author')

    # class Media:
    #     js= ('/static/js/tinyinject.js',)

@admin.register(GK)
class GKView(admin.ModelAdmin):
    list_display = ('title','created_at','author')

    # class Media:
    #     js= ('/static/js/tinyinject.js',)

@admin.register(Topic)
class TopicView(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Comment)
class CommentView(admin.ModelAdmin):
    list_display = ('content','post','author')


@admin.register(Like)
class LikeView(admin.ModelAdmin):
    list_display = ('post','user','created_at')


@admin.register(Dislike)
class DislikeView(admin.ModelAdmin):
    list_display = ('post','user','created_at')


@admin.register(Quote)
class QuoteView(admin.ModelAdmin):
    list_display = ('quote','author')