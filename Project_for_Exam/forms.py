from django import forms
from django.forms import  ModelForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import MyUser


# Update
class UserChangeForm(ModelForm):
    password = ReadOnlyPasswordHashField
    class Meta:
        model = MyUser
        fields = "__all__"

# Create
class UserCreationForm(ModelForm):
    #It's strange system for adding two password , i think i can do it with one password, but for now I'll live it like that.
    password1 =forms.CharField(
        widget=forms.widgets.PasswordInput,
        label="Password"
    )
    password2 =forms.CharField(
        widget=forms.widgets.PasswordInput,
        label="Password Confirm"
    )

    #Cleaning password if they not same
    def clean_password(self, commit=True):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 != password2:
            self.add_error("password1", "passwords are not same")
            return None
        return password1
    
    #saving password
    def save(self, commit = True):
        user = super().save(False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    class Meta:
        model = MyUser
        fields = "__all__"

#For registation
class RegistationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email','full_name','password1','password2')