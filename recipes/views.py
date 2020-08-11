from django.shortcuts import render, HttpResponsePermanentRedirect, reverse
from recipes.models import Author, Recipe
from recipes.forms import RecipeForm, AuthorForm


def index_view(request):
    my_recipes = Recipe.objects.all()
    return render(
        request, "index.html", {"recipes": my_recipes, "page_title": "Recipe Box"}
    )


def author_view(request, author_id):
    my_author = Author.objects.filter(id=author_id).first()
    author_recipes = Recipe.objects.filter(author=my_author)
    return render(
        request, "author_detail.html", {"author": my_author, "recipes": author_recipes}
    )


def recipe_view(request, recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": my_recipe})


def recipe_form_view(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get("title"),
                author=data.get("author"),
                description=data.get("description"),
                time_required=data.get("time_required"),
                instructions=data.get("instructions"),
            )
            return HttpResponsePermanentRedirect(reverse("homepage"))

    form = RecipeForm()
    return render(request, "generic_form.html", {"form": form})


def author_form_view(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        form.save()
        return HttpResponsePermanentRedirect(reverse("homepage"))

    form = AuthorForm()
    return render(request, "generic_form.html", {"form": form})
