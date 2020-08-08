from django.shortcuts import render
from recipes.models import Author, Recipe


def index_view(request):
    my_recipes = Recipe.objects.all()
    return render(request, 'index.html', {"recipes": my_recipes, "page_title": "Recipe Box"})


def author_view(request, author_id):
    my_author = Author.objects.filter(id=author_id).first()
    author_recipes = Recipe.objects.filter(author=my_author)
    return render(request, 'author_detail.html', {"author": my_author, "recipes": author_recipes})


def recipe_view(request, recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, 'recipe_detail.html', {"recipe": my_recipe})
