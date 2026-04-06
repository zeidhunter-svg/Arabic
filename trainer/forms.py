from django import forms

from .models import Card


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["word", "translation", "example", "image", "category"]
        labels = {
            "word": "Арабское слово",
            "translation": "Перевод",
            "example": "Пример предложения",
            "image": "Ссылка на изображение",
            "category": "Категория",
        }
        widgets = {
            "word": forms.TextInput(
                attrs={
                    "class": "form-control arabic-input",
                    "placeholder": "Например: كِتَاب",
                    "dir": "rtl",
                }
            ),
            "translation": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например: книга",
                }
            ),
            "example": forms.Textarea(
                attrs={
                    "class": "form-control arabic-input",
                    "placeholder": "Введите пример предложения",
                    "rows": 4,
                    "dir": "rtl",
                }
            ),
            "image": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com/image.jpg",
                }
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
        error_messages = {
            "word": {
                "required": "Введите арабское слово.",
                "max_length": "Слово не должно превышать 120 символов.",
            },
            "translation": {
                "required": "Введите перевод.",
                "max_length": "Перевод не должен превышать 180 символов.",
            },
            "example": {
                "required": "Введите пример использования.",
            },
            "category": {
                "required": "Выберите категорию.",
            },
        }

    def clean_word(self) -> str:
        word = (self.cleaned_data.get("word") or "").strip()
        if len(word) < 1:
            raise forms.ValidationError("Поле с арабским словом не может быть пустым.")
        return word

    def clean_translation(self) -> str:
        translation = (self.cleaned_data.get("translation") or "").strip()
        if len(translation) < 2:
            raise forms.ValidationError("Перевод должен содержать минимум 2 символа.")
        return translation

    def clean_example(self) -> str:
        example = (self.cleaned_data.get("example") or "").strip()
        if len(example) < 10:
            raise forms.ValidationError(
                "Пример предложения должен содержать минимум 10 символов."
            )
        return example

    def clean_image(self) -> str:
        image = (self.cleaned_data.get("image") or "").strip()
        return image

    def clean(self) -> dict:
        cleaned_data = super().clean()
        word = cleaned_data.get("word")
        translation = cleaned_data.get("translation")
        if word and translation and word == translation:
            raise forms.ValidationError(
                "Арабское слово и перевод не должны полностью совпадать."
            )
        return cleaned_data
