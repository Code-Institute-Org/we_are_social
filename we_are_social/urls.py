"""we_are_social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
import contact.views
import home.views
from accounts.views import register, profile, login, logout, cancel_subscription, subscriptions_webhook

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',home.views.get_index, name='home'),
    url(r'^contact/',contact.views.contact, name='contact'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^register/$', register, name='register'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^cancel_subscription/$', cancel_subscription, name='cancel_subscription'),
    url(r'^subscriptions_webhook/$', subscriptions_webhook, name='subscriptions_webhook'),
]
