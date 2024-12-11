from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ShowProfile, Host, Photographer, CameraOperator, Dancer, Singer


class ShowCompanyRegistrationForm(UserCreationForm):
    show_name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    host = forms.ModelChoiceField(queryset=Host.objects.all(), required=False)
    photographer = forms.ModelChoiceField(queryset=Photographer.objects.all(), required=False)
    camera_operator = forms.ModelChoiceField(queryset=CameraOperator.objects.all(), required=False)
    dancer = forms.ModelChoiceField(queryset=Dancer.objects.all(), required=False)
    singer = forms.ModelChoiceField(queryset=Singer.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'show_name', 'description', 'host', 'photographer',
                  'camera_operator', 'dancer', 'singer']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            show_profile = ShowProfile.objects.create(
                user=user,
                show_name=self.cleaned_data['show_name'],
                description=self.cleaned_data['description'],
                host=self.cleaned_data['host'],
                photographer=self.cleaned_data['photographer'],
                camera_operator=self.cleaned_data['camera_operator'],
                dancer=self.cleaned_data['dancer'],
                singer=self.cleaned_data['singer']
            )
        return user


class SingerForm(forms.ModelForm):
    class Meta:
        model = Singer
        fields = ['name', 'image', 'video', 'contact_info']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Singer.objects.filter(name=name).exists():
            raise forms.ValidationError("Singer with this name already exists.")
        return name


class DancerForm(forms.ModelForm):
    class Meta:
        model = Dancer
        fields = ['name', 'image', 'video', 'contact_info']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Singer.objects.filter(name=name).exists():
            raise forms.ValidationError("Dancer with this name already exists.")
        return name


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['name', 'image', 'video', 'contact_info']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Singer.objects.filter(name=name).exists():
            raise forms.ValidationError("Host with this name already exists.")
        return name


class PhotographerForm(forms.ModelForm):
    class Meta:
        model = Photographer
        fields = ['name', 'image', 'video', 'contact_info']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Singer.objects.filter(name=name).exists():
            raise forms.ValidationError("Photographer with this name already exists.")
        return name


class CameraOperatorForm(forms.ModelForm):
    class Meta:
        model = CameraOperator
        fields = ['name', 'image', 'video', 'contact_info']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Singer.objects.filter(name=name).exists():
            raise forms.ValidationError("Operator with this name already exists.")
        return name


class ShowProfileForm(forms.ModelForm):
    class Meta:
        model = ShowProfile
        fields = [
            'show_name', 'address', 'host', 'photographer', 'camera_operator', 'dancer', 'singer'
        ]
        widgets = {
            'dancer': forms.CheckboxSelectMultiple(),
            'singer': forms.CheckboxSelectMultiple(),
        }