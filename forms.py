from django import forms

class EmailForm(forms.Form):
    condition = forms.CharField(label='',widget=forms.TextInput({'name':'condition','onclick':'condition_blank()'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'size':'30','name':'email','onclick':'email_blank()'}))
