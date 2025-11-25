from django.urls import path
from .views import ResumeFileScoreView

urlpatterns = [
    path("score/", ResumeFileScoreView.as_view(), name="resume-score"),
]
