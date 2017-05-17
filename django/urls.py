"""feeder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import creditfeeder.views as creditfeeder_views
import creditfeeder.plugins.views as creditfeeder_plugins_views
urlpatterns = [
    url(r'^load_student$',creditfeeder_views.load_student,name='load_student'),
    url(r'^plugins/nrt/config$',creditfeeder_plugins_views.nrt_config,name='nrt_config'),
    url(r'^plugins/nrt/test$',creditfeeder_plugins_views.nrt_test,name='nrt_test'),
    url(r'^remove$',creditfeeder_views.remove,name='remove'),
    url(r'^delete$',creditfeeder_views.delete,name='delete'),
    url(r'^create$',creditfeeder_views.create,name='create'),
    url(r'^assign$',creditfeeder_views.assign,name='assign'),
    url(r'^get$',creditfeeder_views.get,name='get'),
    url(r'^logout$',creditfeeder_views.logout_view,name='logout'),
    url(r'^backdoor$',creditfeeder_views.backdoor,name='backdoor'),
    url(r'^feeder$',creditfeeder_views.home,name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^$',creditfeeder_views.home,name='home'),
]
