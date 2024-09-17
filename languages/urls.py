from django.urls import path, include
from . import views

urlpatterns = [
    #______________MUSLIM PRO_________________
    path("prayers", views.prayerTimes, name="prayers"),
    

    path('', views.index, name="enind"),
    path('oxtems/', views.oxtems, name="oxtems"),
    # path('urltofile/', views.urlToFile, name="url_to_file"),
    path('camtems/', views.camtems, name="cams"),
    
    # Zero to Hero & other learnings
    path('learn/', views.zero_to_hero_home, name="learn_home"),
    path('learn-start/<int:course>/', views.zero_to_hero_start, name="learn_start"),
    path('learnz/<str:lang>/<int:unit>/<int:lesson>/', views.zero_to_hero, name="learn"),
    path('learn/<int:id>', views.index, name="learn_english"),
    path('presentindefinite/', views.pres_ind, name="present_indefinite"),

    path('zthadd/', views.zth_entry, name="zth_entry"),
    path('zth/', views.zth_view, name="zth"),

    # Dictionary & all
    path('wordadd/', views.word_entry, name="word_entry"),
    path('dictionary/', views.dictionary, name="dictionary"),
    path('dictionary/topics/', views.dictionaryTopic, name="dictionary_topic"),
    path('dictionary/topics/<str:name>/', views.dictionaryTopicView, name="dictionary_topic_view"),
    path('dictcoll/', views.dictionary_collocation, name="dictionary_collocation"),
    path('dictcollentry/', views.collocation_entry, name="collocation_entry"),
    path('dictcolledit/', views.collocation_edit, name="collocation_edit"),
    path('collocation/<int:id>/', views.collocation_view, name="collocation_view"),
    path('word/<int:word>/', views.word_main, name="word"),
    path('word/<int:word>/<int:sense>/', views.word_main_single, name="words"),
    path('entries/', views.dict_filt, name="dict_filt"),

    # Headwords update for searching & model to json
    path('dictionaryjson/', views.dictionary_json, name="dictionary_json"),

    path('ipa_converter/', views.ipa_convert, name="ipa_converter"),

    # Revision
    path('revisemain/', views.revise_main, name="revisemain"),
    path('exercise/', views.exercise, name="fexercise"),
    path('note-edit/<int:id>', views.note_edit, name="note_edit"),
    path('datamain', views.data_main, name="data_main"),

    path('flashcards/', include("languages.english.flashcards.urls")),
    
    # Posts
    path('posts/', views.post_list, name="posts"),
    path('gkposts/', views.gkpost_list, name="gkposts"),
    path('post/', views.post_entry, name='post_entry'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('gkpost/<int:pk>/', views.gkpost_detail, name='gkpost_detail'),
    path('test/', views.post_detail_test, name='post_detail_test'),
    path('exercise/<int:pk>/', views.exercise, name='exercise'),
    path('exercise/', views.exercise_entry, name='exercise_entry'),
    path('exact/', views.ex_action, name="ex_action"),

    # User
    path('mywords/', views.my_words, name="my_words"),
    path('myword/<int:word>/', views.my_word, name="my_word"),
    path('myposts/', views.post_entry, name='my_posts'),

    # Comments & Voting
    path('post/<int:pk>/like/', views.like, name='like'),
    path('post/<int:pk>/dislike/', views.dislike, name='dislike'),
    path('post/<int:pk>/edit_comment/', views.edit_comment, name='edit_comment'),
    path('post/<int:pk>/delete_comment/', views.delete_comment, name='delete_comment'),

    # Games
    path('games/', views.games, name='games'),
    path('games/wordscapes/', views.game_wordscapes, name='wordscapes'),
    path('games/wordsearch/', views.game_wordsearch, name='wordsearch'),
    path('groups/', views.groups, name='groups'),
]
