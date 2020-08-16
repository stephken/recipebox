from django import forms
from recipes.models import Author

# , Recipe


class RecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    # author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=80)
    instructions = forms.CharField(widget=forms.Textarea)


class StaffRecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=80)
    instructions = forms.CharField(widget=forms.Textarea)


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "bio"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)
