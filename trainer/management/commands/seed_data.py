from django.core.management.base import BaseCommand

from trainer.models import Card, Category


class Command(BaseCommand):
    help = "Заполняет базу демонстрационными категориями и карточками."

    def handle(self, *args, **options):
        categories = {
            "Базовая лексика": [
                {
                    "word": "كِتَاب",
                    "translation": "Книга",
                    "example": "هَذَا كِتَابٌ مُفِيدٌ لِلطُّلَّابِ.",
                    "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794",
                },
                {
                    "word": "قَلَم",
                    "translation": "Ручка",
                    "example": "عِنْدِي قَلَمٌ جَدِيدٌ لِلكِتَابَةِ.",
                    "image": "https://images.unsplash.com/photo-1455390582262-044cdead277a",
                },
                {
                    "word": "بَيْت",
                    "translation": "Дом",
                    "example": "رَجَعَ الوَلَدُ إِلَى البَيْتِ بَعْدَ الدَّرْسِ.",
                    "image": "https://images.unsplash.com/photo-1518780664697-55e3ad937233",
                },
            ],
            "Учёба": [
                {
                    "word": "دَرْس",
                    "translation": "Урок",
                    "example": "بَدَأَ الدَّرْسُ فِي الصَّبَاحِ البَاكِرِ.",
                    "image": "https://images.unsplash.com/photo-1509062522246-3755977927d7",
                },
                {
                    "word": "مُعَلِّم",
                    "translation": "Учитель",
                    "example": "شَرَحَ المُعَلِّمُ القَاعِدَةَ بِوُضُوحٍ.",
                    "image": "https://images.unsplash.com/photo-1544717305-2782549b5136",
                },
                {
                    "word": "طَالِب",
                    "translation": "Студент",
                    "example": "يَجْلِسُ الطَّالِبُ فِي الصَّفِّ الأَوَّلِ.",
                    "image": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f",
                },
            ],
            "Религиозная лексика": [
                {
                    "word": "مَسْجِد",
                    "translation": "Мечеть",
                    "example": "ذَهَبْنَا إِلَى المَسْجِدِ لِصَلَاةِ المَغْرِبِ.",
                    "image": "https://images.unsplash.com/photo-1564769625905-50e93615e769",
                },
                {
                    "word": "صَلَاة",
                    "translation": "Молитва",
                    "example": "تَبْدَأُ الصَّلَاةُ بَعْدَ الأَذَانِ مُبَاشَرَةً.",
                    "image": "https://images.unsplash.com/photo-1743417597339-f4bc72e2a8ba",
                },
            ],
        }

        created_cards = 0
        for category_name, cards in categories.items():
            category, _ = Category.objects.get_or_create(name=category_name)
            for card_data in cards:
                _, created = Card.objects.get_or_create(
                    word=card_data["word"],
                    defaults={
                        "translation": card_data["translation"],
                        "example": card_data["example"],
                        "image": card_data["image"],
                        "category": category,
                    },
                )
                if created:
                    created_cards += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Готово: добавлено "
                f"{Category.objects.count()} категорий и {created_cards} новых карточек."
            )
        )
