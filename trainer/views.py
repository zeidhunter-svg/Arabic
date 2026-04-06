import random

from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import CardForm
from .models import Card, Category


class HomeView(TemplateView):
    template_name = "trainer/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cards_count"] = Card.objects.count()
        context["categories_count"] = Category.objects.count()
        return context


class CardListView(ListView):
    model = Card
    template_name = "trainer/card_list.html"
    context_object_name = "cards"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Card.objects.select_related("category")
            .all()
            .order_by("category__name", "word")
        )
        query = self.request.GET.get("q", "").strip()
        category_id = self.request.GET.get("category", "").strip()

        if query:
            queryset = queryset.filter(
                Q(word__icontains=query)
                | Q(translation__icontains=query)
                | Q(example__icontains=query)
            )
        if category_id.isdigit():
            queryset = queryset.filter(category_id=int(category_id))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["active_category"] = self.request.GET.get("category", "")
        context["search_query"] = self.request.GET.get("q", "")
        return context


class CardDetailView(DetailView):
    model = Card
    template_name = "trainer/card_detail.html"
    context_object_name = "card"


class CardCreateView(CreateView):
    model = Card
    form_class = CardForm
    template_name = "trainer/card_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Карточка успешно добавлена.")
        return super().form_valid(form)


class CardUpdateView(UpdateView):
    model = Card
    form_class = CardForm
    template_name = "trainer/card_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Карточка успешно обновлена.")
        return super().form_valid(form)


class CardDeleteView(DeleteView):
    model = Card
    template_name = "trainer/card_confirm_delete.html"
    success_url = reverse_lazy("trainer:card_list")

    def form_valid(self, form):
        messages.success(self.request, "Карточка удалена.")
        return super().form_valid(form)


def _build_quiz_payload(limit: int = 5) -> list[dict]:
    cards = list(Card.objects.select_related("category").all())
    if len(cards) < 2:
        return []

    random.shuffle(cards)
    questions = cards[: min(limit, len(cards))]
    payload: list[dict] = []

    for card in questions:
        other_cards = [item for item in cards if item.pk != card.pk]
        options_pool = random.sample(other_cards, k=min(3, len(other_cards)))
        option_values = [choice.translation for choice in options_pool]
        option_values.append(card.translation)
        random.shuffle(option_values)

        payload.append(
            {
                "id": card.pk,
                "word": card.word,
                "example": card.example,
                "category": card.category.name,
                "correct_answer": card.translation,
                "options": option_values,
            }
        )
    return payload


def quiz_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        quiz_payload = _build_quiz_payload()
        request.session["quiz_payload"] = quiz_payload
        request.session.modified = True
        return render(
            request,
            "trainer/quiz.html",
            {
                "quiz_payload": quiz_payload,
                "cards_count": Card.objects.count(),
            },
        )

    quiz_payload = request.session.get("quiz_payload", [])
    if not quiz_payload:
        messages.warning(request, "Сначала сформируйте тест, затем отправьте ответы.")
        return redirect("trainer:quiz")

    results = []
    score = 0
    missing_answers = [
        question
        for question in quiz_payload
        if not request.POST.get(f"question_{question['id']}", "")
    ]
    if missing_answers:
        messages.error(
            request,
            "Ответьте на все вопросы перед отправкой теста.",
        )
        for question in quiz_payload:
            question["selected_answer"] = request.POST.get(f"question_{question['id']}", "")
        return render(
            request,
            "trainer/quiz.html",
            {
                "quiz_payload": quiz_payload,
                "cards_count": Card.objects.count(),
            },
        )

    for question in quiz_payload:
        submitted = request.POST.get(f"question_{question['id']}", "")
        is_correct = submitted == question["correct_answer"]
        if is_correct:
            score += 1
        results.append(
            {
                "word": question["word"],
                "example": question["example"],
                "category": question["category"],
                "selected_answer": submitted,
                "correct_answer": question["correct_answer"],
                "is_correct": is_correct,
            }
        )

    request.session["quiz_result"] = {
        "score": score,
        "total": len(quiz_payload),
        "results": results,
    }
    request.session.modified = True
    return redirect("trainer:quiz_result")


def quiz_result_view(request: HttpRequest) -> HttpResponse:
    quiz_result = request.session.get("quiz_result")
    if not quiz_result:
        messages.info(request, "Сначала пройдите тест, чтобы увидеть результаты.")
        return redirect("trainer:quiz")
    return render(request, "trainer/quiz_result.html", {"quiz_result": quiz_result})
