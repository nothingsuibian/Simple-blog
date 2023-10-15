
from django.urls import path, re_path

from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('active/<active_code>', views.Actice_user, name='active_user'),
    path('forget_pwd/', views.Forget_pwd, name='forget_pwd'),
    path('forget_pwd_url/<active_code>', views.forget_pwd_url, name='forget_pwd_url'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('logout/', views.Logout, name='logout'),
    path('editor_user/', views.editor_user, name='editor_user'),
]