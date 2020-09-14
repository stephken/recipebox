from django.shortcuts import render
from recipes.models import Author, Recipe, Favorites
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from recipes.forms import AddRecipeForm, AddAuthorForm, LoginForm, SignupForm




def index_view(request):
    my_recipes = Recipe.objects.all()
    return render(request, 'index.html', {"recipes": my_recipes, "page_title": "Recipe Box"})

@login_required
def edit_recipe_view(request, recipe_id):
    edit_recipe = Recipe.objects.get(id=recipe_id)
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            edit_recipe.title = data["title"]
            edit_recipe.description = data["description"]
            edit_recipe.time_required = data["time_required"]
            edit_recipe.instructions = data["instructions"]
            edit_recipe.save()
        return HttpResponseRedirect(reverse("recipe", args=[edit_recipe.id]))
    data = {
        "title": edit_recipe.title,
        "description": edit_recipe.description,
        "time_required": edit_recipe.time_required,
        "instructions": edit_recipe.instructions,
    }
    form = AddRecipeForm(initial=data)
    return render(request, "generic_form.html", {"form": form})


def author_view(request, author_id):
    my_author = Author.objects.filter(id=author_id).first()
    author_recipes = Recipe.objects.filter(author=my_author)
    return render(request, 'author_detail.html', {"author": my_author, "recipes": author_recipes})

def author_favorite(request, author_id):
    author = Author.objects.get(id=author)
    favorite = Favorites.objects.filter(author=author)
    return render(request, "favorites.html", {"favorite": favorite, "author": author.name})




@login_required
def favorite_recipe(request, recipe_id):
    if Favorites.objects.filter(author=Author.objects.get(user=request.user), recipe=Recipe.objects.get(id=recipe_id)):
        return HttpResponseRedirect(reverse("recipe", args=[recipe_id]))
    else:
        Favorites.objects.create(
        author=Author.objects.get(user=request.user),
        recipe=Recipe.objects.get(id=recipe_id),
    )
    return HttpResponseRedirect(reverse("recipe", args=[recipe_id]))


@staff_member_required
def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse("homepage"))

    form = AddAuthorForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        # form.save()
        if form.is_valid():
            data = form.cleaned_data
            new_article = Recipe.objects.create(
                title=data.get("title"),
                author=request.user.author,
                description=data.get("description"),
                time_required=data.get("time_required"),
                instructions=data.get("instructions")
            )
        return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get("next", reverse("homepage")))

    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get(
                "username"), password=data.get("password"))
            Author.objects.create(name=data.get("username"), user=new_user)
            login(request, new_user)
            return HttpResponseRedirect(reverse("homepage"))

    form = SignupForm()
    return render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))





#def recipe_view(request, recipe_id):
   # my_recipe = Recipe.objects.filter(id=recipe_id).first()
    #return render(request, 'recipe_detail.html', {"recipe": my_recipe})
