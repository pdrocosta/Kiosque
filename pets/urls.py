from django.urls import path

urlpatterns = [
    path("pets/", PetsView.as_view()),
]