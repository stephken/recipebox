"""recipebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from recipes import views


urlpatterns = [
    path('', views.index_view),
    path('author/<int:author_id>/', views.author_view),
    path('recipe/<int:recipe_id>/',views.edit_recipe_view),
    path("", views.index_view, name="homepage"),
    path("recipe/<int:recipe_id>/edit/", views.edit_recipe_view),
    path("author/<int:author_id>/favorites/", views.author_favorite),
    path("author/<int:author_id>/", views.author_view),
    path("addrecipe/", views.add_recipe, name="addrecipe"),
    path("recipe/<int:recipe_id>/favorites/", views.favorite_recipe),
    path("recipe/<int:recipe_id>/", views.edit_recipe_view, name="recipe"),
    path("addauthor/", views.add_author, name="addauthor"),
    path("login/", views.login_view, name="loginview"),
    path("logout/", views.logout_view, name="logoutview"),
    path("signup/", views.signup_view, name="signup"),
    path('admin/', admin.site.urls)
]
