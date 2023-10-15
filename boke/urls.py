"""boke URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from django.conf.urls import url


from utils.upload import upload_file  # 富文本编辑器上传图片方法


from user import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('blog/', include('blog.urls')),

    path('uploads', upload_file, name='uploads') # 上传图片url
    # url(r'^login/', views.login)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "仙的管理后台"
admin.site.site_title = "仙的管理后台"

# python manage.py shell
# from django.contrib.auth.models import User
#
# user = User.objects.all()
# user
# <QuerySet [<User: admin>]>
#
# user = User.objects.get(username='admin')
# user.set_password('admin')
# user.save()
# <QuerySet [<User: 1829782089@qq.com>, <User: 3363812121@qq.com>]>

