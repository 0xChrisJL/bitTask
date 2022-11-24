from django.conf import settings
from django.urls import path, include, re_path
from django.views import static

import web
from web import views, urls

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('', views.index, name='home'),

    path('', include(web.urls)),
]
