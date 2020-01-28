"""ProjektKoncowy URL Configuration

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
from django.urls import path

from GdzieTeraz.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('add_restaurant/', RestaurantAddView.as_view(), name='add_restaurant'),
    path('restaurant_details/<int:pk>/', RestaurantDetailsView.as_view(), name='details_restaurant'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('restaurant_profile/<int:pk>/', RestaurantProfileView.as_view(), name='profile'),
    path('tables/<int:pk>/', TablesView.as_view(), name='tables'),
    path('add_tables/<int:pk>/', AddTableView.as_view(), name='add_tables'),

]
