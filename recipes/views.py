from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

from recipes.models import Author, Recipe
from recipes.forms import RecipeForm, StaffRecipeForm, AuthorForm, LoginForm, SignupForm


def index_view(request):
    my_recipes = Recipe.objects.all()
    return render(
        request, "index.html", {"recipes": my_recipes, "page_title": "Recipe Box"}
    )


def recipe_view(request, recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": my_recipe})


def author_view(request, author_id):
    my_author = Author.objects.filter(id=author_id).first()
    author_recipes = Recipe.objects.filter(author=my_author)
    return render(
        request, "author_detail.html", {"author": my_author, "recipes": author_recipes}
    )


@login_required
def recipe_form_view(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get("title"),
                author=request.user.author,
                description=data.get("description"),
                time_required=data.get("time_required"),
                instructions=data.get("instructions"),
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = RecipeForm()
    return render(request, "generic_form.html", {"form": form})


@staff_member_required(login_url="/login/")
def staff_recipe_form_view(request):
    if request.method == "POST":
        form = StaffRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get("title"),
                author=data.get("author"),
                description=data.get("description"),
                time_required=data.get("time_required"),
                instructions=data.get("instructions"),
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = StaffRecipeForm()
    return render(request, "staff_recipe_form.html", {"form": form})


@staff_member_required(login_url="/login/")
def author_form_view(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse("homepage"))

    form = AuthorForm()
    return render(request, "generic_form.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data.get("username"), password=data.get("password")
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get("next", reverse("homepage"))
                )

    form = LoginForm()
    return render(request, "login_form.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(
                username=data.get("username"), password=data.get("password")
            )
            Author.objects.create(name=data.get("username"), user=new_user)
            login(request, new_user)
            return HttpResponseRedirect(reverse("homepage"))

    form = SignupForm()
    return render(request, "signup_form.html", {"form": form})


@login_required
def error_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data.get("username"), password=data.get("password")
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get("next", reverse("homepage"))
                )

    form = LoginForm()
    return render(request, "error_view.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))
