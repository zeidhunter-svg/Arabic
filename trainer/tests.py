from django.test import Client, TestCase
from django.urls import reverse

from .models import Card, Category


class TrainerViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Базовая лексика")
        self.card = Card.objects.create(
            word="كِتَاب",
            translation="Книга",
            example="هَذَا كِتَابٌ مُفِيدٌ لِلطُّلَّابِ.",
            category=self.category,
        )
        Card.objects.create(
            word="بَيْت",
            translation="Дом",
            example="ذَهَبَ الطَّالِبُ إِلَى البَيْتِ بَعْدَ الدَّرْسِ.",
            category=self.category,
        )

    def test_home_page_available(self):
        response = self.client.get(reverse("trainer:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тренажёр классического арабского языка")

    def test_card_create_form_validation(self):
        response = self.client.post(
            reverse("trainer:card_create"),
            {
                "word": "",
                "translation": "а",
                "example": "коротко",
                "category": self.category.pk,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Введите арабское слово.")

    def test_quiz_page_available(self):
        response = self.client.get(reverse("trainer:quiz"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Проверка знаний")

    def test_quiz_submission_requires_answers_for_all_questions(self):
        quiz_page = self.client.get(reverse("trainer:quiz"))
        session = self.client.session
        quiz_payload = session.get("quiz_payload", [])

        self.assertEqual(quiz_page.status_code, 200)
        self.assertTrue(quiz_payload)

        first_question = quiz_payload[0]
        response = self.client.post(
            reverse("trainer:quiz"),
            {
                f"question_{first_question['id']}": first_question["correct_answer"],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ответьте на все вопросы перед отправкой теста.")
