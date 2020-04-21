from django import forms

class MyForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    name = forms.CharField(max_length=20)
    bio = forms.CharField(max_length=300 , required = False)
    
    