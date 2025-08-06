from django import forms

class HistoryForm(forms.Form):
    text = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre texte'})
    )
