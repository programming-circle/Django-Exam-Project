from django import forms
from django.forms import  ModelForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import MyUser , Cars , Brand


class CarCreateForm(forms.ModelForm):
    slug = forms.SlugField(
        widget=forms.TextInput(attrs={'class': 'validate'}),
        help_text='Enter a URL-friendly identifier.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure brand field always has fresh queryset
        self.fields['brand'].queryset = Brand.objects.all()
        self.fields['brand'].widget = forms.Select(attrs={'class':'browser-default'})
        self.fields['brand'].empty_label = 'Choose a brand'

    class Meta:
        model = Cars
        fields= ['name','brand','slug','description','price','discount_price','stock','image_path']
        widgets = {
            'name': forms.TextInput(attrs={'class':'validate'}),
            'description': forms.Textarea(attrs={'class':'validate', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class':'validate', 'step':'0.01'}),
            'discount_price': forms.NumberInput(attrs={'class':'validate', 'step':'0.01'}),
            'stock': forms.NumberInput(attrs={'class':'validate', 'min':'0'}),
            'image_path': forms.ClearableFileInput(attrs={'class':'validate'}),
        }
# BrandForm = forms.inlineformset_factory(
#     Brand,
#     Cars,
#     fields=['name','slug'],
#     extra=2, #I don't know what it does on practice.. on site says it showing how many empty string show.
#     can_delete=False # This i don't understand too, it says "allow delete already existing strings
# )

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'validate', 'placeholder': 'Введіть назву бренду'}),
        }

# Update
class UserChangeForm(ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = "__all__"

# Create
class UserCreationForm(ModelForm):
    # It's strange system for adding two password , i think i can do it with one password, but for now I'll live it like that.
    password1 = forms.CharField(
        widget=forms.widgets.PasswordInput,
        label="Password"
    )
    password2 = forms.CharField(
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
    
    # Saving password
    def save(self, commit=True):
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