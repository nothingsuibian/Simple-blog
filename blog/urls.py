from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('category/<int:category_id>/', views.category_list, name='category_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
    path('archives/<int:year>/<int:month>', views.archives, name='archives'),

]

git config --global user.name "nothingsuibian"
git config --global user.email "ning20000520@gmail.com"
