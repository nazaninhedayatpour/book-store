from django import forms
from .models import Review,Book


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            "rating",
            "comment",
        ]

        widgets = {
            "rating": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 5,
                }
            ),

            "comment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write your review..."
                }
            ),
        }

class BookForm(forms.ModelForm):
    
    class Meta:
        model = Book

        fields = [
            "title",
            "author",
            "pages",
            "price",
            "stock",
            "publication_year",
            "is_active",
            "category",
            "description",
            "cover",
        ]