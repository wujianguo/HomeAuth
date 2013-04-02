from django import forms

class AddKeyForm(forms.Form):
    pubkey = forms.CharField(widget=forms.Textarea)
