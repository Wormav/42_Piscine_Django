from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "synopsis", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter article title...",
                    "maxlength": 64,
                }
            ),
            "synopsis": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write a brief synopsis...",
                    "rows": 3,
                    "maxlength": 312,
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your article content...",
                    "rows": 15,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
