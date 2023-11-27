from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser

ROLES = (
        (1, 'ProjectManager'),
        (2, 'collaborater'),
        (3, 'Any'),
        (4, 'Any2')
    )

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    roles = forms.ChoiceField(required=True, choices=ROLES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email','roles']

    def save(self, commit=True):
            user = super(UserRegisterForm, self).save(commit=False)
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.role = self.cleaned_data['roles']
            if commit:
                user.save()
                
            return user

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Retype Password'
        self.fields['roles'].widget.attrs['class'] = 'form-control'   
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    roles = forms.ChoiceField(choices=ROLES)
    class Meta: 
        model = CustomUser
        fields = ['username', 'email','roles']

class UserUpdateImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image']