"""MapOut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import authenticate, login
from mapout_app.views import home, index, login_view1, signup_view, logout ,help_ ,schedule ,settings_

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home,name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', login_view1),
    path('accounts/signup/',signup_view),
    path('logout/', logout),
    path('index/', index, name='index'),
    path('help/',help_, name='help'),
    path('schedule/',schedule, name='schedule'),
    path('settings/',settings_, name='settings'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
