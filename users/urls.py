from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

'''url converter'''
from django.urls import register_converter
from . import converters
register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('', views.sign_in),
    path("userlog/", views.userlog, name="userlog"),
    path("users/", views.users, name="users"),
    path("userdetail/<int:id>/", views.user_detail, name="user_detail"),
    path('login/', views.sign_in, name='sign_in'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    # path('sessions/<yyyy:year>/', views.custom_url, name='custom_url'),
    path('profile/', views.user_profile, name='profile'),
    path('notes/', views.notes, name='notes'),
    path('changeprofile/', views.change_profile, name='change_profile'),
    path('register/', views.sign_up, name='sign_up'),
    path('logout/', views.sign_out, name='sign_out'),
    path('changepass/', views.change_password, name='changepass'),
    path('changepass2/', views.change_password2, name='changepass2'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    #contact us
    path('contactus', views.contact_us, name="contact_us"),
    path('setplan', views.plan, name="set_plan"),
    path('chat', views.chat, name="chat"),
]
