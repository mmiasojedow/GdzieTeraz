"""gdzie_teraz URL Configuration

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
from api.views import APIRestaurantView
from django.contrib import admin
from django.urls import path, re_path
from main_app.views import MainView
from my_user_auth.views import LoginView, LogoutView, TokenGeneratorView
from restaurant_app.views import (AddTableView, RestaurantAddView,
                                  RestaurantProfileView, TablesView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('generate_token/', TokenGeneratorView.as_view(), name="token_generator"),
    path('profile/', RestaurantProfileView.as_view(), name='profile'),
    re_path(r'^add_restaurant/(?P<token>([a-z0-9]){32})/$', RestaurantAddView.as_view(), name="add_restaurant"),
    path('tables/', TablesView.as_view(), name='tables'),
    path('add_tables/', AddTableView.as_view(), name='add_tables'),
    path('api-restaurant/<int:pk>/', APIRestaurantView.as_view(), name='api_restaurant'),

]
