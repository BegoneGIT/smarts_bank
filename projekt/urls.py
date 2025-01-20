"""
URL configuration for projekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from projekt.views.SmartsBankView import SmartsBankView, SmartDisplayView, SmartCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SmartsBankView.as_view(),
         name="bank-main"),
    path('smart/<slug:slug>', SmartDisplayView.as_view(),
         name="bank-smart"),
    path('create/smart/', SmartCreateView.as_view(),
         name="smart-create"),
]