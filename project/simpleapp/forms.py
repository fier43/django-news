from django import forms
from django.core.exceptions import ValidationError

from .models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "description", "category", "date"]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")

        if title == description:
            raise ValidationError("Описание не должно быть идентично названию.")

        return cleaned_data
