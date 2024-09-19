from django import forms
from product.models import ContactUs, Comment


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        exclude = ("user",)
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control"})
        }
