"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import path
import basic_auth.views
import home.views
urlpatterns = [
    path('get_all_logs/',home.views.get_all_logs, name="get_all_logs"),
    path('login/', basic_auth.views.login, name="login"),
    path('logout/', basic_auth.views.logout, name ="logout"),
    path('register_user/', basic_auth.views.register_user, name ="register_user"),
    path('handle_log/', home.views.handle_log, name ="handle_log")
] 
