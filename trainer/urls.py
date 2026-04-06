from django.urls import path

from .views import (
    CardCreateView,
    CardDeleteView,
    CardDetailView,
    CardListView,
    CardUpdateView,
    HomeView,
    quiz_result_view,
    quiz_view,
)

app_name = "trainer"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("cards/", CardListView.as_view(), name="card_list"),
    path("cards/add/", CardCreateView.as_view(), name="card_create"),
    path("cards/<int:pk>/", CardDetailView.as_view(), name="card_detail"),
    path("cards/<int:pk>/edit/", CardUpdateView.as_view(), name="card_edit"),
    path("cards/<int:pk>/delete/", CardDeleteView.as_view(), name="card_delete"),
    path("quiz/", quiz_view, name="quiz"),
    path("quiz/result/", quiz_result_view, name="quiz_result"),
]
