from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        "Название категории",
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(2)],
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)


class Card(models.Model):
    word = models.CharField(
        "Арабское слово",
        max_length=120,
        validators=[MinLengthValidator(1)],
    )
    translation = models.CharField(
        "Перевод",
        max_length=180,
        validators=[MinLengthValidator(2)],
    )
    example = models.TextField(
        "Пример",
        validators=[MinLengthValidator(10)],
    )
    image = models.URLField("Ссылка на изображение", blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="cards",
        verbose_name="Категория",
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"
        ordering = ["word"]

    def __str__(self) -> str:
        return f"{self.word} — {self.translation}"

    def get_absolute_url(self) -> str:
        return reverse("trainer:card_detail", kwargs={"pk": self.pk})
