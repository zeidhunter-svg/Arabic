import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100,
                        unique=True,
                        validators=[django.core.validators.MinLengthValidator(2)],
                        verbose_name="Название категории",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Card",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "word",
                    models.CharField(
                        max_length=120,
                        validators=[django.core.validators.MinLengthValidator(1)],
                        verbose_name="Арабское слово",
                    ),
                ),
                (
                    "translation",
                    models.CharField(
                        max_length=180,
                        validators=[django.core.validators.MinLengthValidator(2)],
                        verbose_name="Перевод",
                    ),
                ),
                (
                    "example",
                    models.TextField(
                        validators=[django.core.validators.MinLengthValidator(10)],
                        verbose_name="Пример",
                    ),
                ),
                (
                    "image",
                    models.URLField(blank=True, verbose_name="Ссылка на изображение"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cards",
                        to="trainer.category",
                        verbose_name="Категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Карточка",
                "verbose_name_plural": "Карточки",
                "ordering": ["word"],
            },
        ),
    ]
