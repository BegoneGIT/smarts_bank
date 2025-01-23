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
from django.urls import include, path
from projekt.views.SmartsBankView import SmartsBankView, SmartDisplayView, SmartCreateView, RegisterSmartVoteView, SmartAssignTeamView
from projekt.views.UsersView import AddUserView, UserLoginView, UserLogoutView

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', SmartsBankView.as_view(),
         name="bank-main"),
    path('smart/<slug:slug>', SmartDisplayView.as_view(),
         name="bank-smart"),
    path('create/smart/', SmartCreateView.as_view(),
         name="smart-create"),
    path('create/user/', AddUserView.as_view(),
         name="user-create"),
    path('accounts/login/', UserLoginView.as_view(),
         name="login"),
    path('logout/', UserLogoutView.as_view(),
         name="logout"),
    path('smart/vote/<slug:slug>', RegisterSmartVoteView.as_view(),
         name="vote-smart"),
     path('smart/<slug:slug>/assign/<int:team>', SmartAssignTeamView.as_view(),
         name="assign-smart"),
]
