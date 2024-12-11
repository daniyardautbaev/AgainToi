from django import forms

from home.models import Contact, Media


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Your Message',
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})
        self.fields['subject'].widget.attrs.update({'placeholder': 'Enter subject'})
        self.fields['message'].widget.attrs.update({'placeholder': 'Enter Your Message'})


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['photo', 'video', 'description']
        labels = {
            'photo': 'Upload a Photo',
            'video': 'Upload a Video',
            'description': 'Write a Review',
        }
        widgets = {
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a photo...',
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a video...',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review here...',
                'rows': 4,
            }),
        }
