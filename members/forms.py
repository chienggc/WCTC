from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Award
from UserManagement.models import PointLog


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class AwardForm(ModelForm):
    award_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    award_point = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Award
        fields = ('award_name', 'award_point')

    def disabled_field(self):
        self.fields['award_name'].widget.attrs['readonly'] = True


class EditProfileForm(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_staff')


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=50,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=50,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class GiveAwardForm(forms.Form):
    award_winner = forms.CharField(max_length=50,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'd'}))
    award = forms.ModelChoiceField(queryset=Award.objects.exclude(award_name="Login Award"))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(GiveAwardForm, self).__init__(*args, **kwargs)
        self.fields['award'].widget.attrs['class'] = 'form-control'

    def set_initial(self, name):
        self.fields['award_winner'].initial = name
        self.fields['message'].initial = "Hearty thank you for your great support in WCTC tasks. Entire " \
                                         "team is working really hard and made good progress now. Thank again. Keep moving up!"
